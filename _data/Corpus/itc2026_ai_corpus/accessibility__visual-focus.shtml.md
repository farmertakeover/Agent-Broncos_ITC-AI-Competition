**Source:** https://www.cpp.edu/accessibility/visual-focus.shtml

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

# Implementing Accessible Visual Focus Indicators

## Introduction

One aspect that is often overlooked when maintaining digital accessibility is visual focus indicators, which are defined as the visual cues that indicate which element is currently active or in focus.

Focus indicators are visual cues that distinguish elements that are currently active or focused on a webpage. They help users who rely on keyboards for site navigation or other assistive technologies, ensuring they can identify and interact with elements seamlessly.

Visual focus indicators are put in use when a user uses a keyboard to navigate (often done through the 'tab' key) to a specific element or a mouse to hover over an element. These elements usually have a visual appearance change to signify the element has the current focus.

Interactive elements should have a visual indicator when they are in focus. These include items such as links, form elements, menus, and buttons. In essence, anything a user can click should have a visual focus indicator.

## Importance of Visual Focus Indicators

Visual Focus Indicators are crucial for users with motor impairments and users who rely on keyboards for site navigation. Those with attention deficits also benefit from being able to discover where the focus is located. They inform the user what element is currently active within a website or application. It also allows users to quickly determine where their keyboard focus or mouse is on the page. These visual cues help users process large amounts of information.

## Implementing Visual Focus Indicators

### Best Design Practices

**Contrast and Visibility**

To ensure users can clearly see the visual focus indicator, they must maintain sufficient color contrast against the background, so they are easily distinguishable from the focused and unfocused states. Visual focus indicators should have a contrast ratio of at least 3:1 against the background.

**Consistency in Design**

All visual focus indicators throughout your website or application should be consistent in presence and styling. This reduces confusion and improves the usability of your website or application.

### Visual Focus Indicator Example

The image below shows an example of a visual focus indicator. The blue border that appears around the Cal Poly Pomona logo in the top left corner indicates that the element is currently in focus.

![Cal Poly Pomona homepage with a blue border around the Cal Poly Pomona logo in the top left corner.](img/visualfocusexample.png)

### Testing Methods

**General Test**

1. Begin in the browser address bar, as it forces focus to start at the top of the page
2. Use the **Tab**key, navigate through all elements until you reach the bottom of the page. You can use **Shift**+ **Tab**to navigate back one element

**Verify that:**

1. All interactive elements display a visual focus indicator when in focus
2. There are no instances when focus disappears
3. Visual focus is easy to identify

## WCAG 2.1 and References

### Web Content Accessibility Guidelines (WCAG) for Keyboard

[Guideline 2.1 Keyboard Accessible: All Functionality Available From a Keyboard (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/#keyboard-accessible)

* [2.1.1 Keyboard](https://www.w3.org/WAI/WCAG21/quickref/#keyboard)
* [2.1.2 No Keyboard Trap](https://www.w3.org/WAI/WCAG21/quickref/#no-keyboard-trap)
* [2.1.3 Keyboard (No Exception)](https://www.w3.org/WAI/WCAG21/quickref/#keyboard-no-exception)
* [2.1.4 Character Key Shortcuts](https://www.w3.org/WAI/WCAG21/quickref/#character-key-shortcuts)

### Other Resources

* [Mozilla CSS: Outline](https://developer.mozilla.org/en-US/docs/Web/CSS/outline)
* [WebAIM: Keyboard Accessibility](https://webaim.org/techniques/keyboard/)
* [Nielsen Norman Group: Keyboard-Only Navigation](https://www.nngroup.com/articles/keyboard-accessibility/)

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