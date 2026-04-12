**Source:** https://www.cpp.edu/it/web-development/tutorial/instructions/getting-started/breadcrumb-setup.shtml

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

* [Back to Resources](/it/web-development/tutorial/resources.shtml)
* [Training Home Page](/it/web-development/tutorial/instructions/index.shtml)
* Getting Started

  + [Cascade Overview](/it/web-development/tutorial/instructions/getting-started/cascade-overview.shtml)
  + [Adding Content](/it/web-development/tutorial/instructions/getting-started/adding-content.shtml)
  + [Submit Content](/it/web-development/tutorial/instructions/getting-started/submit-content.shtml)
  + [Site Navigation](/it/web-development/tutorial/instructions/getting-started/navigation-instruction.shtml)
  + [Unit Signature](/it/web-development/tutorial/instructions/getting-started/unit-signature.shtml)
  + [Breadcrumb Setup](/it/web-development/tutorial/instructions/getting-started/breadcrumb-setup.shtml)
  + [Create New Organizational Chart](/it/web-development/tutorial/instructions/module-instructions/org-chart-module/create-new-org-chart.shtml)
* Templates

  + [College Landing Page](/it/web-development/tutorial/instructions/templates-instructions/college-landing-page-instruction.shtml)
  + [College Department Page](/it/web-development/tutorial/instructions/templates-instructions/college-department-page-instruction.shtml)
  + [Division Landing Page](/it/web-development/tutorial/instructions/templates-instructions/division-landing-page-instruction.shtml)
  + [Division Department Page](/it/web-development/tutorial/instructions/templates-instructions/division-department-page-instruction.shtml)
  + [Gateway Page](/it/web-development/tutorial/instructions/templates-instructions/gateway-page-instruction.shtml)
  + [Program Page](/it/web-development/tutorial/instructions/templates-instructions/program-page-instruction.shtml)
  + [Content Sub Page](/it/web-development/tutorial/instructions/templates-instructions/content-subpage-instruction.shtml)
* [Modules](/it/web-development/tutorial/instructions/module-instructions/module-list.shtml)

Menu

- [Back to Resources](/it/web-development/tutorial/resources.shtml)
- [Training Home Page](/it/web-development/tutorial/instructions/index.shtml)
- Getting Started

  [Cascade Overview](/it/web-development/tutorial/instructions/getting-started/cascade-overview.shtml)

  [Adding Content](/it/web-development/tutorial/instructions/getting-started/adding-content.shtml)

  [Submit Content](/it/web-development/tutorial/instructions/getting-started/submit-content.shtml)

  [Site Navigation](/it/web-development/tutorial/instructions/getting-started/navigation-instruction.shtml)

  [Unit Signature](/it/web-development/tutorial/instructions/getting-started/unit-signature.shtml)

  [Breadcrumb Setup](/it/web-development/tutorial/instructions/getting-started/breadcrumb-setup.shtml)

  [Create New Organizational Chart](/it/web-development/tutorial/instructions/module-instructions/org-chart-module/create-new-org-chart.shtml)
- Templates

  [College Landing Page](/it/web-development/tutorial/instructions/templates-instructions/college-landing-page-instruction.shtml)

  [College Department Page](/it/web-development/tutorial/instructions/templates-instructions/college-department-page-instruction.shtml)

  [Division Landing Page](/it/web-development/tutorial/instructions/templates-instructions/division-landing-page-instruction.shtml)

  [Division Department Page](/it/web-development/tutorial/instructions/templates-instructions/division-department-page-instruction.shtml)

  [Gateway Page](/it/web-development/tutorial/instructions/templates-instructions/gateway-page-instruction.shtml)

  [Program Page](/it/web-development/tutorial/instructions/templates-instructions/program-page-instruction.shtml)

  [Content Sub Page](/it/web-development/tutorial/instructions/templates-instructions/content-subpage-instruction.shtml)
- [Modules](/it/web-development/tutorial/instructions/module-instructions/module-list.shtml)

# Breadcrumb Setup

## Overview

Breadcrumbs allow a user to understand where they are in the hierarchy of a website and quickly navigate levels. For example, the [College of Science: Science Educational Enhancement Services (SEES)](https://www.cpp.edu/sci/sees/index.shtml) site needed to allow users to navigate back to the College of Science home page. The following is how to set up breadcrumbs for a site like SEES.

**Page View**

![](img/breadcrumb-tutorial-pageview.png)

## Enabling Breadcrumbs

Breadcrumbs display only after the page is updated, submitted, and published with Show Breadcrumb = Yes. Subpages will automatically appear in the breadcrumb trail once their settings are enabled and published.

### Adding a Custom Breadcrumb

**Cascade View (Editing Mode)**

In Cascade, navigate to the target site (root folder) and select **Edit**.

![](img/breadcrumb-tutorial-cascade1.png)

The **parent site** is defined as the site directly above your current site. Enter the **Custom Breadcrumb Title** and **Custom Breadcrumb URL** for that parent site. Enter the **Display Name** for your current site, which will appear in the breadcrumb trail.

![](img/breadcrumb-tutorial-cascade2.png)

### Enabling Breadcrumbs on Individual Pages

You must enable breadcrumbs on every page where you want them to appear.

**Cascade View (Editing Mode)**

Navigate to the page where the breadcrumb should appear and select **Edit**.

**![](img/breadcrumb-tutorial-cascade3.png)**

Activate the breadcrumb functionality by choosing **Yes**. The breadcrumb will be rendered directly below the Page Heading.

**![](img/breadcrumb-tutorial-cascade4.png)**

## Web Development

### Follow Us:

[Instagram opens a new window
![Instagram](/common/green-and-gold/assets/icons/social/insta-reverse.svg)](https://www.instagram.com/cpp.it/)
[YouTube opens a new window
![YouTube](/common/green-and-gold/assets/icons/social/yt-reverse.svg)](https://www.youtube.com/channel/UCNS5iT8xon0TdoSOLKm_JPg)
[X opens a new window
![X](/common/green-and-gold/assets/icons/social/x-reverse.svg)](https://twitter.com/cppIT)

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