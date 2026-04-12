**Source:** https://www.cpp.edu/accessibility/heading-structure.shtml

---

[Skip to content](#main)

[![Cal Poly Pomona Logo](/common/green-and-gold/assets/logos/cpp_horizontal_2c_green_rgb.png)](/)

[![Cal Poly Pomona Logo](/common/green-and-gold/assets/logos/cpp_primary_2c_green_cmyk.png)](/)

[apply](/apply/)
[visit](/outreach/tours.shtml)
[info](https://engage.cpp.edu/register/ask_us_a_question)
[give](/giving/)
[mycpp](https://my.cpp.edu)

![Open search box](/common/green-and-gold/assets/icons/nav/search-dark-green.svg)

![menu](/common/green-and-gold/assets/icons/nav/menu.svg)

Search

![Close search menu](/common/green-and-gold/assets/icons/nav/close.svg)

[![Cal Poly Pomona Logo](/common/green-and-gold/assets/logos/cpp_horizontal_1c_gold_rgb.png)](/)

[apply](/apply/)
[visit](/outreach/tours.shtml)
[info](https://engage.cpp.edu/register/ask_us_a_question)
[give](/giving/)
[mycpp](https://my.cpp.edu)

![Open search box](/common/green-and-gold/assets/icons/nav/search-white.svg)

![Close menu](/common/green-and-gold/assets/icons/nav/close.svg)

[Commencement](/commencement/)
[apply](/apply/)
[visit](/outreach/tours.shtml)
[info](https://engage.cpp.edu/register/ask_us_a_question)
[give](/giving/)
[mycpp](https://my.cpp.edu)

* [Home](/)
* about
* admissions & aid
* academics
* life at CPP

* [athletics](https://broncoathletics.com/)
* [alumni](/alumni/)
* [news & events](/news/)

* [future students](/prospective-student-gateway/)
  |
* [current students](/student-gateway/)
  |
* [families](/family/)
  |
* [faculty & staff](/faculty-staff-gateway/)

* [![Instagram](/common/green-and-gold/assets/icons/social/insta.svg)](https://www.instagram.com/calpolypomona/)
* [![LinkedIn](/common/green-and-gold/assets/icons/social/li.svg)](https://www.linkedin.com/school/cal-poly-pomona/)
* [![Youtube](/common/green-and-gold/assets/icons/social/yt.svg)](https://www.youtube.com/user/calpolypomona)
* [![Facebook](/common/green-and-gold/assets/icons/social/fb.svg)](https://www.facebook.com/calpolypomona)
* [![X](/common/green-and-gold/assets/icons/social/x.svg)](https://twitter.com/calpolypomona)

* [IT Home](/it/)
* [Accessibility Home](/accessibility/index.shtml)
* About ATI

  + [ATI Working Group](/it/governance.shtml)
  + [ATI Regulations & Standards](/accessibility/regulations-and-standards.shtml)
  + [Universal Design](/accessibility/universal-design.shtml)
  + [Impact of Accessibility](/accessibility/impact-accessibility.shtml)
  + [Contact ATI](/accessibility/contact-us.shtml)
* ATI/IT Procurement Review

  + [ATI/IT Procurement Review Process](/accessibility/procurement.shtml)
  + [Submit ATI/IT Review Request (eHelp)](https://cpp.service-now.com/ehelp?id=sc_cat_item&sys_id=bc4674596f0d43007996073aea3ee428&sysparm_category=10fabc8a0f1417407a6046ace1050e93&catalog_id=-1)
* Web and Document Accessibility

  + [Web Accessibility](/accessibility/web-accessibility.shtml)
  + [Digital Media Accessibility](/accessibility/digital-media-accessibility.shtml)
  + [Submit Accessibility/ATI Test Request (eHelp)](https://cpp.service-now.com/ehelp?id=sc_cat_item&sys_id=c70d670f0f489f007a6046ace1050eac&sysparm_category=10fabc8a0f1417407a6046ace1050e93&catalog_id=-1)
* [Training](/accessibility/training.shtml)
* [Resources](/accessibility/resources.shtml)
* [Report a Barrier](/accessibility.shtml)

Menu

- [IT Home](/it/)
- [Accessibility Home](/accessibility/index.shtml)
- About ATI

  [ATI Working Group](/it/governance.shtml)

  [ATI Regulations & Standards](/accessibility/regulations-and-standards.shtml)

  [Universal Design](/accessibility/universal-design.shtml)

  [Impact of Accessibility](/accessibility/impact-accessibility.shtml)

  [Contact ATI](/accessibility/contact-us.shtml)
- ATI/IT Procurement Review

  [ATI/IT Procurement Review Process](/accessibility/procurement.shtml)

  [Submit ATI/IT Review Request (eHelp)](https://cpp.service-now.com/ehelp?id=sc_cat_item&sys_id=bc4674596f0d43007996073aea3ee428&sysparm_category=10fabc8a0f1417407a6046ace1050e93&catalog_id=-1)
- Web and Document Accessibility

  [Web Accessibility](/accessibility/web-accessibility.shtml)

  [Digital Media Accessibility](/accessibility/digital-media-accessibility.shtml)

  [Submit Accessibility/ATI Test Request (eHelp)](https://cpp.service-now.com/ehelp?id=sc_cat_item&sys_id=c70d670f0f489f007a6046ace1050eac&sysparm_category=10fabc8a0f1417407a6046ace1050e93&catalog_id=-1)
- [Training](/accessibility/training.shtml)
- [Resources](/accessibility/resources.shtml)
- [Report a Barrier](/accessibility.shtml)

# Heading Structure

## What is a heading?

A heading is an HTML element used to label the beginning of a section of content, like the title of this page! Using headings allows assistive technology users to quickly navigate to each section and know its relationship with other content on the page. Headings range from <h1> (the highest) to <h6> (the lowest).

## Implementing Accessible Headings

### How do I use headings?

In general, you should use a heading whenever you start a new section (or subsection) of content. Take the following example.

 ![Text: Heading 1 Cal Poly Pomona, Heading 2 Campus, Heading 3 Dining Locations, Heading 3 Housing, Heading 2 Students, Heading 2 Faculty.](img/web-accessibility-img/headings-how-do-i-use-headings-1.png)

Would it make sense to include the “Students” heading as a heading level 3 under “Campus”? Probably not. If you come across information on your website that seems like either a new topic or a specific part of the current topic, it is best to create a new heading to organize the page.

### Heading "Do"s and "Don't"s

DO use descriptive heading text. While some heading text may make sense in the context of your page, users of assistive technology often navigate using just the headings outside of context. Having non-descriptive heading text (or sentence fragments such as “Here you can”) makes the page less accessible for everyone.

DON’T skip heading levels. While it may be tempting to skip heading levels because a topic seems much less important than its parent section, this can cause confusion for screen reader users who may think that they have missed a section. In the example below, heading level 3 is skipped between “Campus” and “Dining Locations”. This creates an illogical structure that may lead to difficulty in navigating the page.
![Text: Heading 1 Cal Poly Pomona, Heading 2 Campus, Heading 4 Dining Locations, Heading 4 Housing, Heading 2 Students, Heading 2 Faculty.](img/web-accessibility-img/headings-heading-dos-and-donts-1.png)
Is it ever okay to skip heading levels? Only if there is content that is repeated on multiple pages. There, continuity is more important than heading organization.

## Accessible Technology

![Ripped green paper.](/common/green-and-gold/assets/images/green-rip.svg)

[![Cal Poly Pomona logo, building with a palm tree.](/common/green-and-gold/assets/logos/cpp_primary_1c_gold_rgb.png)](https://www.cpp.edu/)

[Apply](https://www.cpp.edu/apply/)
[Maps](https://maps.cpp.edu/)
[Visit](https://www.cpp.edu/outreach/tours.shtml)
[Contact Us](https://www.cpp.edu/contact.shtml)

[![Instagram opens a new window](/common/green-and-gold/assets/icons/social/insta.svg)](https://www.instagram.com/calpolypomona/)
[![LinkedIn opens a new window](/common/green-and-gold/assets/icons/social/li.svg)](https://www.linkedin.com/school/cal-poly-pomona/)
[![YouTube opens a new window](/common/green-and-gold/assets/icons/social/yt.svg)](https://www.youtube.com/user/calpolypomona)
[![Facebook opens a new window](/common/green-and-gold/assets/icons/social/fb.svg)](https://www.facebook.com/calpolypomona)
[![X opens a new window](/common/green-and-gold/assets/icons/social/x.svg)](https://twitter.com/calpolypomona)

Copyright ©2026 California State Polytechnic University, Pomona. All Rights Reserved

A campus of
[The California State University](https://www.calstate.edu/).

[Feedback](https://www.cpp.edu/website-feedback.shtml)
[Privacy](https://calstate.policystat.com/policy/18808065/latest/#autoid-z2p98)
[Accessibility](https://www.cpp.edu/accessibility.shtml)
[Document Readers](https://www.cpp.edu/file-viewers.shtml)