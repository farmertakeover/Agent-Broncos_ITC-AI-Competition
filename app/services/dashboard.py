"""
Unified campus dashboard aggregator: official RSS/ICS feeds and Student Pulse.

Source priority (see integrations/dashboard_api_schema.json):
  official_rss → pulse
"""
from __future__ import annotations

import hashlib
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import urlparse
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

import httpx

from retrieval import config

from app.services import pulse as pulse_service

DASHBOARD_SCHEMA_VERSION = 1

# Lower number = higher priority when sorting within a section.
PRIORITY_OFFICIAL_RSS = 10
PRIORITY_PULSE = 30

SOURCE_PRIORITY_ORDER = ("official_rss", "pulse")


def _strip_html(text: str | None) -> str:
    if not text:
        return ""
    t = re.sub(r"<[^>]+>", " ", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:500] if len(t) > 500 else t


def _card_id(parts: str) -> str:
    return hashlib.sha256(parts.encode("utf-8", errors="replace")).hexdigest()[:20]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_http_date(s: str | None) -> datetime | None:
    if not s or not isinstance(s, str):
        return None
    try:
        dt = parsedate_to_datetime(s.strip())
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        return None


def _parse_isoish(s: str | None) -> datetime | None:
    if not s or not isinstance(s, str):
        return None
    raw = s.strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def make_card(
    *,
    type_: str,
    title: str,
    summary: str | None,
    start_at: datetime | None,
    end_at: datetime | None,
    source: str,
    url: str | None,
    priority: int,
    audience: str = "all",
    freshness: str = "unknown",
    feed_role: str | None = None,
    dedupe_key: str | None = None,
    repeat_label: str | None = None,
) -> dict[str, Any]:
    dk = dedupe_key or f"{source}|{url or ''}|{title}"
    card: dict[str, Any] = {
        "id": _card_id(dk),
        "type": type_,
        "title": (title or "Untitled")[:300],
        "summary": (summary or None),
        "start_at": start_at.isoformat() if start_at else None,
        "end_at": end_at.isoformat() if end_at else None,
        "source": source,
        "url": url,
        "priority": priority,
        "audience": audience,
        "freshness": freshness,
    }
    if feed_role:
        card["feed_role"] = feed_role
    if repeat_label:
        card["repeat_label"] = repeat_label[:400]
    return card


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def _child_by_local(parent: Any, local: str) -> Any:
    want = local.lower()
    for el in list(parent):
        if _local_name(el.tag).lower() == want:
            return el
    return None


def _rss_fetch(url: str, timeout: float) -> tuple[str | None, str | None]:
    if not url.strip():
        return None, "empty_url"
    if os.getenv("CPP_DASHBOARD_SKIP_REMOTE", "").lower() in ("1", "true", "yes"):
        return None, "skip_remote"
    try:
        headers = {"User-Agent": "AgentBroncos-Dashboard/1.0"}
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            r = client.get(url, headers=headers)
        if r.status_code != 200:
            return None, f"http_{r.status_code}"
        return r.text, None
    except httpx.TimeoutException:
        return None, "timeout"
    except httpx.HTTPError as e:
        return None, str(e)


def _parse_ics_value(raw: str) -> str:
    return raw.strip().replace("\\,", ",").replace("\\n", " ").replace("\\N", " ").strip()


def _unfold_ics_text(text: str) -> str:
    """RFC 5545 line folding: continuation lines begin with space or tab."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    acc: list[str] = []
    for raw_line in text.split("\n"):
        if raw_line.startswith((" ", "\t")) and acc:
            acc[-1] += raw_line[1:] if raw_line.startswith(" ") else raw_line.lstrip()
        else:
            acc.append(raw_line)
    return "\n".join(acc)


def _parse_ics_dt(raw: str) -> datetime | None:
    s = (raw or "").strip()
    if not s:
        return None
    if s.endswith("Z") and len(s) >= 16:
        try:
            return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    if "T" in s:
        try:
            dt = datetime.strptime(s[:15], "%Y%m%dT%H%M%S")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    try:
        dt = datetime.strptime(s[:8], "%Y%m%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _parse_ics_duration_to_timedelta(raw: str) -> timedelta | None:
    """Parse common RFC 5545 DURATION forms (PT2H, P1D, P1DT3H, PT90M) for inferred end times."""
    u = (raw or "").strip().upper()
    if not u.startswith("P"):
        return None
    if "T" in u:
        pre, post = u.split("T", 1)
        days = 0
        dm = re.match(r"^P(\d+)D$", pre)
        if dm:
            days = int(dm.group(1))
        h = mn = sec = 0
        hm = re.search(r"(\d+)H", post)
        if hm:
            h = int(hm.group(1))
        mm = re.search(r"(\d+)M", post)
        if mm:
            mn = int(mm.group(1))
        sm = re.search(r"(\d+)S", post)
        if sm:
            sec = int(sm.group(1))
        td = timedelta(days=days, hours=h, minutes=mn, seconds=sec)
        return td if td.total_seconds() else None
    m2 = re.fullmatch(r"P(\d+)D", u)
    if m2:
        return timedelta(days=int(m2.group(1)))
    return None


def _rrule_display(raw: str) -> str | None:
    if not (raw or "").strip():
        return None
    u = raw.strip().upper()
    bits: list[str] = []
    if "FREQ=WEEKLY" in u:
        bits.append("Weekly")
    elif "FREQ=DAILY" in u:
        bits.append("Daily")
    elif "FREQ=MONTHLY" in u:
        bits.append("Monthly")
    elif "FREQ=YEARLY" in u:
        bits.append("Yearly")
    by = re.search(r"BYDAY=([^;]+)", u)
    if by and bits:
        bits.append(f"on {by.group(1)[:40]}")
    return " · ".join(bits) if bits else None


def _parse_ics_datetime_property(prop_header: str, value: str) -> datetime | None:
    """
    Parse DTSTART/DTEND honoring VALUE=DATE and TZID= (common on MyBar/Campus Labs feeds).
    ``prop_header`` is the full left-hand side, e.g. ``DTSTART;TZID=America/Los_Angeles``.
    """
    v = (value or "").strip()
    if not v:
        return None
    hdr = (prop_header or "").strip()
    hdr_l = hdr.lower()
    if "value=date" in hdr_l or (len(v) == 8 and "t" not in v.lower()):
        try:
            dt = datetime.strptime(v[:8], "%Y%m%d")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    tzid: str | None = None
    for piece in hdr.split(";")[1:]:
        pl = piece.strip()
        if pl.upper().startswith("TZID="):
            tzid = pl.split("=", 1)[1].strip().strip('"')
            break
    if v.endswith("Z") and len(v) >= 15:
        return _parse_ics_dt(v)
    if "T" in v:
        try:
            core = v.replace("Z", "")[:15]
            dt_naive = datetime.strptime(core, "%Y%m%dT%H%M%S")
        except ValueError:
            return None
        if tzid:
            try:
                zi = ZoneInfo(tzid)
                return dt_naive.replace(tzinfo=zi).astimezone(timezone.utc)
            except Exception:
                return dt_naive.replace(tzinfo=timezone.utc)
        return dt_naive.replace(tzinfo=timezone.utc)
    try:
        dt = datetime.strptime(v[:8], "%Y%m%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def parse_ics_events(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not text:
        return events
    text = _unfold_ics_text(text)
    current: dict[str, str] | None = None
    for line in text.splitlines():
        ln = line.strip()
        if ln == "BEGIN:VEVENT":
            current = {}
            continue
        if ln == "END:VEVENT":
            if current:
                title = _parse_ics_value(current.get("SUMMARY", "")) or "Event"
                sh = current.get("__hdr_DTSTART", "DTSTART")
                eh = current.get("__hdr_DTEND", "DTEND")
                start = _parse_ics_datetime_property(sh, current.get("DTSTART", ""))
                end = _parse_ics_datetime_property(eh, current.get("DTEND", ""))
                if end is None and start is not None:
                    dur_raw = _parse_ics_value(current.get("DURATION", ""))
                    delta = _parse_ics_duration_to_timedelta(dur_raw)
                    if delta is not None:
                        end = start + delta
                desc = _parse_ics_value(current.get("DESCRIPTION", "")) or None
                url = _parse_ics_value(current.get("URL", "")) or None
                rrule_raw = _parse_ics_value(current.get("RRULE", ""))
                rlab = _rrule_display(rrule_raw)
                events.append(
                    make_card(
                        type_="event",
                        title=title,
                        summary=desc,
                        start_at=start,
                        end_at=end,
                        source="official_rss",
                        url=url,
                        priority=PRIORITY_OFFICIAL_RSS + 2,
                        freshness="live",
                        feed_role="mybar",
                        dedupe_key=f"mybar|{title}|{current.get('DTSTART', '')}",
                        repeat_label=rlab,
                    )
                )
            current = None
            continue
        if current is None or ":" not in ln:
            continue
        pre, val = ln.split(":", 1)
        name = pre.split(";", 1)[0].strip().upper()
        val_s = val.strip()
        current[name] = val_s
        if name in ("DTSTART", "DTEND", "RECURRENCE-ID"):
            current[f"__hdr_{name}"] = pre.strip()
    return events


def parse_rss_or_atom(xml_text: str, *, source_name: str, feed_role: str) -> list[dict[str, Any]]:
    """Parse RSS 2.0 or Atom into dashboard cards (official_rss)."""
    cards: list[dict[str, Any]] = []
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return cards
    root_tag = _local_name(root.tag).lower()
    if root_tag == "rss":
        channel = root.find("channel")
        if channel is None:
            return cards
        for item in channel.findall("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            pub_el = item.find("pubDate")
            title = _strip_html(title_el.text if title_el is not None else "") or "Item"
            link = (link_el.text or "").strip() if link_el is not None else ""
            summary = _strip_html(desc_el.text if desc_el is not None else "")
            pub = _parse_http_date(pub_el.text if pub_el is not None else None)
            type_ = "event" if feed_role == "events" else "news"
            if feed_role == "announcements":
                type_ = "announcement"
            cards.append(
                make_card(
                    type_=type_,
                    title=title,
                    summary=summary or None,
                    start_at=pub,
                    end_at=None,
                    source="official_rss",
                    url=link or None,
                    priority=PRIORITY_OFFICIAL_RSS,
                    freshness="live",
                    feed_role=feed_role,
                    dedupe_key=f"rss|{source_name}|{link}|{title}",
                )
            )
    elif root_tag == "feed":
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        if not entries:
            entries = [el for el in list(root) if _local_name(el.tag).lower() == "entry"]
        for entry in entries:
            title_el = entry.find("atom:title", ns) or _child_by_local(entry, "title")
            summary_el = (
                entry.find("atom:summary", ns)
                or entry.find("atom:content", ns)
                or _child_by_local(entry, "summary")
                or _child_by_local(entry, "content")
            )
            updated_el = entry.find("atom:updated", ns) or _child_by_local(entry, "updated")
            published_el = entry.find("atom:published", ns) or _child_by_local(entry, "published")
            link_el = None
            for link in entry.findall("atom:link", ns) + [_c for _c in list(entry) if _local_name(_c.tag).lower() == "link"]:
                rel = (link.get("rel") or "alternate").lower()
                if rel == "alternate":
                    link_el = link
                    break
            href = (link_el.get("href") or "").strip() if link_el is not None else ""
            title = _strip_html(title_el.text if title_el is not None else "") or "Item"
            summary = _strip_html(summary_el.text if summary_el is not None else "")
            dt = _parse_isoish(updated_el.text if updated_el is not None else None)
            if not dt:
                dt = _parse_isoish(published_el.text if published_el is not None else None)
            type_ = "event" if feed_role == "events" else "news"
            if feed_role == "announcements":
                type_ = "announcement"
            cards.append(
                make_card(
                    type_=type_,
                    title=title,
                    summary=summary or None,
                    start_at=dt,
                    end_at=None,
                    source="official_rss",
                    url=href or None,
                    priority=PRIORITY_OFFICIAL_RSS,
                    freshness="live",
                    feed_role=feed_role,
                    dedupe_key=f"atom|{source_name}|{href}|{title}",
                )
            )
    return cards


def _pulse_cards(pulse: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Split pulse payload into announcement-ish, event-ish, news-ish cards."""
    announcements: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    news: list[dict[str, Any]] = []

    ad = pulse.get("academic_dates")
    if isinstance(ad, dict):
        for it in ad.get("items") or []:
            if not isinstance(it, dict):
                continue
            title = str(it.get("title") or it.get("name") or "Academic date").strip()
            when = str(it.get("date") or it.get("when") or "").strip()
            summary = str(it.get("note") or it.get("description") or "").strip() or None
            start = _parse_isoish(when) or None
            if not start and when:
                summary = f"{when}. {summary or ''}".strip() or when
            events.append(
                make_card(
                    type_="event",
                    title=title,
                    summary=summary,
                    start_at=start,
                    end_at=None,
                    source="pulse",
                    url=it.get("url") if isinstance(it.get("url"), str) else None,
                    priority=PRIORITY_PULSE,
                    audience="students",
                    freshness="stale",
                    dedupe_key=f"pulse_ad|{title}|{when}",
                )
            )

    reddit = pulse.get("reddit_cpp")
    if isinstance(reddit, dict):
        for it in reddit.get("items") or []:
            if not isinstance(it, dict):
                continue
            title = str(it.get("title") or "Thread").strip()
            url = it.get("url") if isinstance(it.get("url"), str) else None
            sub = str(it.get("subreddit") or "reddit")
            news.append(
                make_card(
                    type_="news",
                    title=title,
                    summary=f"r/{sub}" if sub else None,
                    start_at=None,
                    end_at=None,
                    source="pulse",
                    url=url,
                    priority=PRIORITY_PULSE,
                    audience="students",
                    freshness="live",
                    dedupe_key=f"pulse_reddit|{url or title}",
                )
            )

    for disc in pulse.get("disclaimers") or []:
        if isinstance(disc, str) and disc.strip():
            announcements.append(
                make_card(
                    type_="announcement",
                    title="Campus pulse note",
                    summary=disc.strip()[:400],
                    start_at=None,
                    end_at=None,
                    source="pulse",
                    url=None,
                    priority=PRIORITY_PULSE + 5,
                    freshness="stale",
                    dedupe_key=f"pulse_disc|{disc[:80]}",
                )
            )

    return announcements, events, news


def _dedupe_cards(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for c in cards:
        key = f"{c.get('type')}|{c.get('url') or ''}|{c.get('title') or ''}"
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def _sort_section(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(c: dict[str, Any]) -> tuple:
        pr = c.get("priority")
        try:
            p = int(pr) if pr is not None else 99
        except (TypeError, ValueError):
            p = 99
        st = c.get("start_at") or ""
        return (p, st)

    return sorted(cards, key=key)


def _event_still_relevant(card: dict[str, Any], now_utc: datetime) -> bool:
    """Hide ended events so old ICS rows (e.g. January) do not crowd out upcoming ones."""
    if card.get("type") != "event":
        return True
    st = _parse_isoish(str(card["start_at"])) if card.get("start_at") else None
    en = _parse_isoish(str(card["end_at"])) if card.get("end_at") else None
    if en is not None:
        return en >= now_utc
    if st is not None:
        return st >= now_utc - timedelta(hours=2)
    return True


def _sort_events_chronologically(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Soonest upcoming first; events without ``start_at`` sort last."""

    def sort_key(c: dict[str, Any]) -> tuple:
        pr = c.get("priority")
        try:
            p = int(pr) if pr is not None else 99
        except (TypeError, ValueError):
            p = 99
        st = str(c.get("start_at") or "").strip()
        return (p, st or "9999-12-31T23:59:59+00:00")

    return sorted(cards, key=sort_key)


def _campus_link_icon_url(href: str) -> str:
    """Site icon for link tiles (DuckDuckGo static host; no API key)."""
    try:
        host = urlparse(href).netloc.lower()
        if not host:
            return ""
        if host.endswith("reddit.com") or host == "reddit.com":
            return "https://www.redditstatic.com/desktop2x/img/favicon/favicon-32x32.png"
    except ValueError:
        return ""
    return f"https://icons.duckduckgo.com/ip3/{host}.ico"


def _campus_url_dedupe_key(href: str) -> str:
    """Normalize URL so http/https, trailing slashes, and case do not create duplicates."""
    try:
        p = urlparse(href.strip())
        if not p.netloc:
            return href.strip().lower()
        netloc = p.netloc.lower()
        path = (p.path or "").rstrip("/")
        return f"{netloc}{path}"
    except Exception:
        return href.strip().lower()


def _campus_url_reachable(url: str, timeout: float = 2.5) -> bool:
    """HEAD/GET probe; skip checks for hosts that often block datacenter probes (403/timeouts)."""
    try:
        host = urlparse(url).netloc.lower()
        if host.endswith("reddit.com") or host == "reddit.com":
            return True
        # ASI, MyBar, Bronco Direct, etc. frequently fail HEAD from cloud IPs but are official tiles.
        if host == "cpp.edu" or host.endswith(".cpp.edu"):
            return True
    except Exception:
        pass
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            r = client.head(url)
            if r.status_code == 405:
                r = client.get(url, headers={"Range": "bytes=0-0"})
            code = r.status_code
            return 200 <= code < 400
    except Exception:
        return False


def _filter_campus_rows_by_reachability(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Drop links that return 4xx/5xx or fail to connect; keep all rows if every check fails."""
    if not rows:
        return rows
    if os.getenv("CPP_DASHBOARD_SKIP_REMOTE", "").lower() in ("1", "true", "yes"):
        return rows
    if os.getenv("CPP_DASHBOARD_LINK_CHECK", "true").lower() in ("0", "false", "no", "off", "skip"):
        return rows
    urls = [r["url"] for r in rows if r.get("url")]
    if not urls:
        return rows
    ok: set[str] = set()
    workers = min(8, len(urls))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(_campus_url_reachable, u): u for u in urls}
        for fut in as_completed(futs):
            u = futs[fut]
            try:
                if fut.result():
                    ok.add(u)
            except Exception:
                pass
    filtered = [r for r in rows if r.get("url") in ok]
    return filtered if filtered else rows


def _polycentric_site_url() -> str:
    u = (config.DEFAULT_DASHBOARD_RSS_NEWS or "").strip()
    if "/feed/" in u:
        return u.split("/feed/", 1)[0].rstrip("/") + "/"
    return "https://polycentric.cpp.edu/"


def _link_fallback_news_cards() -> list[dict[str, Any]]:
    """Official CPP destinations when RSS/live items are empty (no invented dates)."""
    return [
        make_card(
            type_="news",
            title="Polycentric — CPP news",
            summary="Official campus news. Open the site for current stories and publication dates.",
            start_at=None,
            end_at=None,
            source="link_fallback",
            url=_polycentric_site_url(),
            priority=PRIORITY_OFFICIAL_RSS + 40,
            freshness="stale",
            dedupe_key="fallback|polycentric_site",
        ),
        make_card(
            type_="news",
            title="Getting news at CPP",
            summary="How the university shares news, alerts, and channels (official Student Affairs / StratComm hub).",
            start_at=None,
            end_at=None,
            source="link_fallback",
            url="https://www.cpp.edu/stratcomm/getting-news.shtml",
            priority=PRIORITY_OFFICIAL_RSS + 41,
            freshness="stale",
            dedupe_key="fallback|getting_news",
        ),
    ]


def _link_fallback_announcement_cards() -> list[dict[str, Any]]:
    """Registrar / student-success hubs when no announcement feed items (no invented dates)."""
    return [
        make_card(
            type_="announcement",
            title="Registrar — academic calendars",
            summary="Official term calendars, registration periods, and academic deadlines.",
            start_at=None,
            end_at=None,
            source="link_fallback",
            url="https://www.cpp.edu/registrar/calendars/index.shtml",
            priority=PRIORITY_OFFICIAL_RSS + 42,
            freshness="stale",
            dedupe_key="fallback|registrar_calendars",
        ),
        make_card(
            type_="announcement",
            title="Student success — calendars & dates",
            summary="Official student-success calendar hub. Confirm any date on the linked page.",
            start_at=None,
            end_at=None,
            source="link_fallback",
            url="https://www.cpp.edu/studentsuccess/calendar/index.shtml",
            priority=PRIORITY_OFFICIAL_RSS + 43,
            freshness="stale",
            dedupe_key="fallback|student_success_cal",
        ),
    ]


def _campus_links_from_pulse(pulse: dict[str, Any]) -> list[dict[str, str]]:
    """Turn pulse ``links`` into rows for the dashboard with optional ``icon`` URLs."""
    raw = pulse.get("links")
    if not isinstance(raw, dict):
        return []
    seen_keys: set[str] = set()
    out: list[dict[str, str]] = []
    for title, href in sorted(raw.items(), key=lambda kv: str(kv[0]).lower()):
        if not isinstance(title, str) or not isinstance(href, str):
            continue
        u = href.strip()
        if not u.startswith(("http://", "https://")):
            continue
        key = _campus_url_dedupe_key(u)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        icon = _campus_link_icon_url(u)
        row: dict[str, str] = {"title": title.strip(), "url": u}
        if icon:
            row["icon"] = icon
        out.append(row)
    return _filter_campus_rows_by_reachability(out)


def build_dashboard(
    *,
    prefs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Aggregate official RSS/ICS feeds and pulse enrichment."""
    t0 = time.perf_counter()
    timeout = float(os.getenv("CPP_DASHBOARD_FETCH_TIMEOUT", "6"))
    news_url = (os.getenv("CPP_DASHBOARD_RSS_NEWS") or config.DEFAULT_DASHBOARD_RSS_NEWS).strip()
    events_url = (os.getenv("CPP_DASHBOARD_RSS_EVENTS") or "").strip()
    announce_url = (os.getenv("CPP_DASHBOARD_RSS_ANNOUNCE") or "").strip()
    _mybar_env = os.getenv("CPP_DASHBOARD_MYBAR_ICS")
    if _mybar_env is not None:
        mybar_ics_url = str(_mybar_env).strip()
    else:
        mybar_ics_url = (getattr(config, "DEFAULT_DASHBOARD_MYBAR_ICS", "") or "").strip()

    sources: dict[str, dict[str, Any]] = {}

    def run_rss(name: str, url: str, role: str) -> list[dict[str, Any]]:
        t_r = time.perf_counter()
        xml, err = _rss_fetch(url, timeout)
        ms = int((time.perf_counter() - t_r) * 1000)
        if err:
            sources[name] = {"ok": False, "ms": ms, "error": err}
            return []
        cards = parse_rss_or_atom(xml or "", source_name=name, feed_role=role)
        sources[name] = {"ok": True, "ms": ms, "error": None, "items": len(cards)}
        return cards

    rss_news: list[dict[str, Any]] = []
    rss_events: list[dict[str, Any]] = []
    rss_announce: list[dict[str, Any]] = []
    if news_url:
        rss_news = run_rss("rss_news", news_url, "news")
    else:
        sources["rss_news"] = {"ok": False, "ms": 0, "error": "not_configured"}
    if events_url:
        rss_events = run_rss("rss_events", events_url, "events")
    else:
        sources["rss_events"] = {"ok": False, "ms": 0, "error": "not_configured"}
    if announce_url:
        rss_announce = run_rss("rss_announce", announce_url, "announcements")
    else:
        sources["rss_announce"] = {"ok": False, "ms": 0, "error": "not_configured"}

    mybar_events: list[dict[str, Any]] = []
    if mybar_ics_url:
        t_mb = time.perf_counter()
        ics_text, mb_err = _rss_fetch(mybar_ics_url, timeout)
        mb_ms = int((time.perf_counter() - t_mb) * 1000)
        if mb_err:
            sources["mybar_ics"] = {"ok": False, "ms": mb_ms, "error": mb_err}
        else:
            mybar_events = parse_ics_events(ics_text or "")
            sources["mybar_ics"] = {"ok": True, "ms": mb_ms, "error": None, "items": len(mybar_events)}
    else:
        sources["mybar_ics"] = {"ok": False, "ms": 0, "error": "not_configured"}

    t_p = time.perf_counter()
    pulse = pulse_service.get_pulse_for_api()
    p_ms = int((time.perf_counter() - t_p) * 1000)
    sources["pulse"] = {"ok": True, "ms": p_ms, "error": None, "pulse_source": pulse.get("pulse_source")}

    p_ann, p_events, p_news = _pulse_cards(pulse)

    # Announcements: dedicated RSS, else first 2 news RSS items promoted.
    announcements = list(rss_announce)
    if not announcements and rss_news:
        for c in rss_news[:2]:
            announcements.append(
                make_card(
                    type_="announcement",
                    title=str(c.get("title") or "Announcement"),
                    summary=c.get("summary") if isinstance(c.get("summary"), str) else None,
                    start_at=_parse_isoish(str(c["start_at"])) if c.get("start_at") else None,
                    end_at=_parse_isoish(str(c["end_at"])) if c.get("end_at") else None,
                    source="official_rss",
                    url=c.get("url") if isinstance(c.get("url"), str) else None,
                    priority=PRIORITY_OFFICIAL_RSS + 1,
                    freshness="live",
                    feed_role="announcements",
                    dedupe_key=f"promo_ann|{c.get('id')}",
                )
            )

    events = _dedupe_cards(list(rss_events) + mybar_events + p_events)
    now_utc = datetime.now(timezone.utc)
    events = [c for c in events if _event_still_relevant(c, now_utc)]
    events = _sort_events_chronologically(events)[:24]
    news = _dedupe_cards(list(rss_news) + p_news)

    sections = {
        "announcements": _sort_section(_dedupe_cards(announcements)),
        "events": events,
        "news": _sort_section(news)[:24],
    }
    if not sections["news"]:
        sections["news"] = _sort_section(_link_fallback_news_cards())
    if not sections["announcements"]:
        sections["announcements"] = _sort_section(_link_fallback_announcement_cards())

    ignorable = {"not_configured", "not_connected", "skip_remote"}
    partial = any(
        not v.get("ok") and (v.get("error") not in ignorable)
        for v in sources.values()
    )

    weather_snap = pulse.get("weather") if isinstance(pulse.get("weather"), dict) else {}
    campus_links = _campus_links_from_pulse(pulse)

    out: dict[str, Any] = {
        "schema_version": DASHBOARD_SCHEMA_VERSION,
        "generated_at": _now_iso(),
        "ok": True,
        "partial": partial,
        "source_priority_order": list(SOURCE_PRIORITY_ORDER),
        "sources": sources,
        "sections": sections,
        "pulse_weather": weather_snap,
        "campus_links": campus_links,
        "metrics": {"total_ms": int((time.perf_counter() - t0) * 1000)},
    }
    if prefs:
        out["preferences"] = prefs
    return out
