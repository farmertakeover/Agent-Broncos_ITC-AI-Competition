**Source:** https://www.cpp.edu/accessibility/tab-order.shtml

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

# Accessible Tab Order

## Why is Tab Order Important?

While many users are accustomed to using a mouse for site navigation, it is important to consider those who rely on a keyboard as their main way of interacting with digital content.

Tab order refers to the sequence in which focusable elements, such as links, buttons, and form fields, are selected when a user moves through a digital interface using the Tab key on their keyboard. These elements need to receive focus in order that preserves meaning and operability, so users can understand the page and use its features easily.

This seemingly small detail plays a critical role in ensuring digital materials are accessible, navigable, and usable for everyone. This is particularly important for users who rely on keyboard navigation instead of a mouse, which include:

* People with motor impairments who rely on keyboard access for operating a page
* Blind or low-vision users using screen readers
* Users with temporary impairments

If tab order is not properly implemented:

* People with disabilities that make reading difficult or visual impairments can become disoriented. Jumping around the page makes it hard to understand content relationships or perform actions
* Important elements may be missed. If an interactive element is not reachable by keyboard, it is essentially unusable to someone who can't use a mouse
* Only a small portion of the page may be visible to an individual using a screen magnifier at a high level of magnification

Good tab order:

* Follows a logical, intuitive flow. Typically top to bottom, left to right, like how content is visually laid out
* Matches the visual layout so users can predict where the next focus will go
* Prioritizes interactive elements in the order they're meant to be read
* Avoids "focus traps", which happen when a user gets stuck on a page element and can't navigate to another element using a keyboard

## Implementing Accessible Tab Order

### How 'tabindex' Controls Keyboard Navigation

The **tabindex**attribute in HTML determines the focus order of elements when navigating with the Tab key. It allows developers to specify which elements receive focus and the order in which they receive focus.

* tabindex = "0" allows elements beside links and form elements to receive keyboard focus. It does not change the tab order, but places the element in the logical navigation flow, as if it were a link on the page
* tabindex = "-1" removes the element from the navigation sequence, but can be made focusable using javascript

A tabindex = "1" or higher should be avoided as it is considered a bad practice for web accessibility because:

* Normal flow in the keyboard tab order will be broken when tabbing through the interactive elements
* If the content is dynamically added in between elements with positive tabindex, it will interfere with the normal flow of tabbing

### Examples of Accessible Tab Order

**Example 1: Tab Order Structure**

the image below shows the correct reading order on a page that has multiple navigation links on the side panels.

![Tab Order Structure Example](img/web-accessibility-img/tab_order_example.jpg)

**Example 2: Tab Order Video**

The video demonstrates what keyboard focus and a correct tab order look like.

[Accessible Tab Order Demonstration](https://youtu.be/_eWcRT3HacA)

### Tab Order Testing Methods

Testing the tab order requires a keyboard accessibility evaluation. The basic functions to use for keyboard accessibility evaluation are:

* **Tab key**to navigate through links and form controls
* **Enter**(and /or **Spacebar**) to select an element
* **Arrow keys**are sometimes used for other navigation

In addition to these functions, there are several other standard keyboard shortcuts to be familiar with in order to conduct a keyboard test. Review [WebAIM's shortcuts table](https://webaim.org/techniques/keyboard/#testing) to understand how to navigate through a webpage with the keyboard.

**General Test**

1. Start from the browser address bar (This forces focus to start at the top of the page)
2. Take your hand off your mouse and use only your keyboard
3. Using the **Tab**button, navigate until you reach the bottom of the page (**Shift**+ **Tab**can be used to navigate back one element)

**While using the Tab button, verify that**

1. All interactive elements are accessible with the **Tab**key
2. The tab order coordinates with the structure of the page (left to right, top to bottom - header first, then main navigation, then page navigation (if present), and finally the footer)
3. An easy to follow keyboard focus is present that clearly indicates where you have tabbed to

If your page does not meet the requirements above, review the best practices and examples

## WebAIM Standard Keyboard Shortcuts Table

Standard shortcuts used to interact with a website via the keyboard

| **Interaction** | **Keystrokes** | **Notes for Accessibility** |
| --- | --- | --- |
| **Navigate to interactive elements** | **Tab** - Navigate forward **Shift** + **Tab** - Navigate backward | Visual focus indicators must be present  Navigation order should be logical and intuitive |
| **Link** | **Enter** | Must activate the element |
| **Button** | **Enter**or **Spacebar** | If an element has the **ARIA role="button"**, ensure the element can be activated with both key commands |
| **Checkbox** | **Tab -** move to the next element  **Spacebar**- check/unbox a checkbox | Checkboxes should be used when one or more option can be selected |
| **Radio buttons** | ↑/↓ or ←/→ - select an option  **Tab**- move to the next element | Radio buttons should only be used when only one option from a group can be selected |
| **Select (dropdown) menu** | ↑/↓ - navigate between menu options  **Spacebar -**expand  **Esc -**collapse |  |

## WCAG 2.1 and References

### Web Content Accessibility Guidelines (WCAG 2.1)

[Web Content Accessibility Guidelines (WCAG 2.1)](https://www.w3.org/WAI/WCAG21/quickref/#keyboard-accessible)

* [2.1.1 Keyboard](https://www.w3.org/WAI/WCAG21/quickref/#keyboard)
* [2.1.2 No Keyboard Trap](https://www.w3.org/WAI/WCAG21/quickref/#no-keyboard-trap)
* [2.1.3 Keyboard (No Exception)](https://www.w3.org/WAI/WCAG21/quickref/#keyboard-no-exception)
* [2.1.4 Character Key Shortcuts](https://www.w3.org/WAI/WCAG21/quickref/#character-key-shortcuts)

### Other Resources

* [WebAIM: Keyboard Accessibility](https://webaim.org/techniques/keyboard/)
* [Social Security Common Keyboard Shortcuts Guide](https://www.ssa.gov/accessibility/keyboard_nav.html)
* [WebAIM: Tabindex](https://webaim.org/techniques/keyboard/tabindex)
* [Mozilla Developer: Tabindex Guide](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/tabindex)

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