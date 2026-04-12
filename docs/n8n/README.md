# n8n → Campus pulse

The Flask app exposes:

- `GET /api/student-pulse` — JSON digest for the UI and (optionally) the LLM tool `get_student_pulse`.
- `POST /api/student-pulse/ingest` — push JSON matching [`integrations/pulse_schema.json`](../../integrations/pulse_schema.json).

## Ingest from n8n

1. Set `CPP_PULSE_INGEST_SECRET` in the Flask environment (long random string).
2. In n8n, use an **HTTP Request** node:
   - Method: `POST`
   - URL: `https://your-host/api/student-pulse/ingest`
   - Authentication: Header `Authorization` = `Bearer <same secret>`  
     or header `X-CPP-Pulse-Secret` = `<same secret>`
   - Body: JSON built from prior nodes (weather API, RSS, etc.)

3. Enable the chat tool with `CPP_ENABLE_PULSE_TOOL=true` so the model can call `get_student_pulse` for “what’s happening” style questions. Official CPP answers should still use corpus search.

## Alternative: hosted JSON

If n8n (or another job) writes a public JSON file, set `CPP_PULSE_URL` to that URL. The app will merge it when no local `_data/pulse/latest.json` exists.

## Safety

Do not send portal passwords or FERPA-protected data through this pipeline. Keep the digest to public sources and link-outs.
