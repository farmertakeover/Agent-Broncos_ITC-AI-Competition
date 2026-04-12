**Source:** http://www.cpp.edu/cafe/teaching-and-learning/accessibility-tutorials/websites.shtml

---

* [![Cal Poly Pomona Logo](/common/green-and-gold/assets/logos/cpp_horizontal_2c_green_rgb.png)](https://www.cpp.edu/)
* [apply](https://www.cpp.edu/apply/)
  [visit](https://www.cpp.edu/outreach/tours.shtml)
  [info](https://engage.cpp.edu/register/ask_us_a_question)
  [give](https://www.cpp.edu/giving/)
  [mycpp](https://my.cpp.edu)

  ![Open search box](/common/green-and-gold/assets/icons/nav/search-dark-green.svg)

  ![menu](/common/green-and-gold/assets/icons/nav/menu.svg)

Search

![Close icon](/common/green-and-gold/assets/icons/nav/close.svg)

* [![Cal Poly Pomona Logo](/common/green-and-gold/assets/logos/cpp_horizontal_1c_gold_rgb.png)](https://www.cpp.edu/)

* [apply](https://www.cpp.edu/apply/)
  [visit](https://www.cpp.edu/outreach/tours.shtml)
  [info](https://engage.cpp.edu/register/ask_us_a_question)
  [give](https://www.cpp.edu/giving/)
  [mycpp](https://my.cpp.edu)
* ![Open search box](/common/green-and-gold/assets/icons/nav/search-white.svg)

  ![Close menu](/common/green-and-gold/assets/icons/nav/close.svg)

[apply](https://www.cpp.edu/apply/)
[visit](https://www.cpp.edu/outreach/tours.shtml)
[info](https://engage.cpp.edu/register/ask_us_a_question)
[give](https://www.cpp.edu/giving/)
[mycpp](https://my.cpp.edu)

* [Home](https://www.cpp.edu/)
* about
* admissions & aid
* academics
* life at CPP

* [athletics](https://broncoathletics.com/)
* [alumni](https://www.cpp.edu/alumni/)
* [news & events](https://www.cpp.edu/news/)

* [future students](https://www.cpp.edu/prospective-student-gateway/)
  |
* [current students](https://www.cpp.edu/student-gateway/)
  |
* [families](https://www.cpp.edu/family/)
  |
* [faculty & staff](https://www.cpp.edu/faculty-staff-gateway/)

* [![Instagram](/common/green-and-gold/assets/icons/social/insta.svg)](https://www.instagram.com/calpolypomona/)
* [![LinkedIn](/common/green-and-gold/assets/icons/social/li.svg)](https://www.linkedin.com/school/cal-poly-pomona/)
* [![Youtube](/common/green-and-gold/assets/icons/social/yt.svg)](https://www.youtube.com/user/calpolypomona)
* [![Facebook](/common/green-and-gold/assets/icons/social/fb.svg)](https://www.facebook.com/calpolypomona)
* [![X](/common/green-and-gold/assets/icons/social/x.svg)](https://twitter.com/calpolypomona)

Center for the Advancement of Faculty Excellence (CAFE)

* [Home](/cafe/index.shtml)
* About Us

  [Who We Are](/cafe/about-us/who-we-are.shtml)
  [Request Services](/cafe/about-us/request-services.shtml)
  [Studio 6](/cafe/about-us/studio-6.shtml)
  [Faculty Affairs](https://www.cpp.edu/faculty-affairs)
  [Newsletter](/cafe/about-us/newsletter.shtml)
  [Weekly Emails](/cafe/about-us/weekly-emails.shtml)
* Programs & Events

  [Upcoming Programs & Events](/cafe/programs-and-events/upcoming-programs.shtml)
  [Past Events and Workshops](/cafe/programs-and-events/past-events-and-workshop.shtml)
  [CAFE Winter Institute](/cafe/programs-and-events/winter-institute-2026.shtml)
* Teaching & Learning

  [Best Practices in Teaching](/cafe/teaching-and-learning/index.shtml)
  [AI in the Classroom](https://www.cpp.edu/cafe/teaching-and-learning/ai/index.shtml)
  [Learning Technologies](/cafe/teaching-and-learning/learning-technologies.shtml)
  [Technology QuickStart Tutorials](/cafe/teaching-and-learning/quickstart-tutorials.shtml)
  [Canvas Support](https://www.cpp.edu/cafe/teaching-and-learning/lms-support/index.shtml)
  [Multimedia Learning Objects](https://www.cpp.edu/cafe/learning-objects)
* Faculty Resources

  [Lifecycle of the Professoriate](https://www.cpp.edu/cafe/faculty-resources/lifecycle-of-professoriate/index.shtml)
  [Internal Funding Opportunities](/cafe/faculty-resources/internal-funding.shtml)
  [Faculty Directory](https://www.cpp.edu/faculty/index.shtml)
* Faculty Recognition

  [Wall of COOL](https://www.cpp.edu/cafe/cool)
  [Wall of COOL Speaker Series](https://www.cpp.edu/cafe/cool/speaker-series.shtml)
  [Champions for Accessibility and Inclusivity (CHAI)](/cafe/faculty-recognition/chai.shtml)
  [Faculty Photo Consultations](/cafe/faculty-recognition/photo-consultations.shtml)

# Website Accessibility

## ![HTML icon of a webpage](../../img/accessibility/html.png)Website Accessibility

Discover techniques that can be used to make accessible websites. Because this page uses basic HTML, these code snippets can be applied to nearly any HTML editor or website builder, including popular programs such as Adobe Dreamweaver and WordPress.

Expand/Collapse All for faq number 1

## Headings

Heading structure benefits both sighted users and visually impaired users. Sighted users can scroll through a page and quickly pick out the big, bold text (headings) to get an idea of the document structure and content. Similarly, visually impaired users who use screen readers have the ability to quickly jump between headings on a page. It is important to always use heading tags (*<h1> - <h6>*) for all headings. While simply bolding or enlarging text will provide visual structure, it will not provide the back-end structure to benefit visually impaired users.

Headings are to be used in a hierarchical manner. Level 1 is the highest level of heading. Level 2 headings are sub-headings of level 1 headings. Level 3 headings are sub-headings of level 2 headings and so on.

*<h1>Heading using H1</h1>*

*<h2>Heading using H2</h2>*

*<h3>Heading using H3</h3>…*

## Hyperlinks

Every hyperlink should have a clear description of its destination and the description should make sense even when taken out of context. Hyperlink descriptions tell users exactly where the hyperlink will be taking them before even clicking on it. While surrounding text may be helpful for sighted users, it will not benefit visually impaired users who choose to navigate a list of hyperlinks taken out context.

*<a href=”http://www.cpp.edu">Cal Poly Pomona</a>*

### Examples of hyperlink descriptions

* Correct:
  + To learn more about Canvas, visit our [Canvas eHelp Tutorials](https://cpp.service-now.com/ehelp?sys_kb_id=e6c53eb087dfa5904f5098e73cbb3566&id=kb_article_view).
* Incorrect:
  + Canvas eHelp Tutorials: <https://cpp.service-now.com/ehelp?sys_kb_id=e6c53eb087dfa5904f5098e73cbb3566&id=kb_article_view>
  + For more information about Canvas eHelp Tutorials, [click here](https://cpp.service-now.com/ehelp?sys_kb_id=e6c53eb087dfa5904f5098e73cbb3566&id=kb_article_view).

## Images

Images should be given alternative text, also called alt text, serving as a description of what is happening in the image. This description allows visually impaired users, through the use of a screen reader, the opportunity to receive the same content from an image that a sighted user would receive.

*<img src="calpolylogo.gif" alt="Cal Poly logo">*

Purely decorative images, or images that don’t help with the understanding of the content, should include an alt attribute with an empty description.

*<img src=”imagename.gif” alt=” ">*

Images that are used for navigational purposes should include an alt attribute that describes the hyperlink destination.

*<a href="http://www.cpp.edu"><img src=”calpolyimage.gif” alt=”Cal Poly Pomona home page”></a>*

### Alternative text tips

* Don't describe every detail of an image, just describe the main idea you are trying to convey to users.
* Be as concise as possible. If the image conveys a main idea that is already discussed in detail in the surrounding text, one sentence may be all the alt text that's needed.
* Don't begin alt text with "Image of..." because images are already identified to the user as images by the screen reader.
* Alt text should be left blank for purely decorative images, or images that don’t help with the understanding of content.

## Lists

Being able to read content in the order that it was intended is essential in a user's understanding. When it comes to listing content, there are two popular methods: numbers and bullet points. An ordered list (numbers) (*<ol>*) should be used when the order matters, otherwise use an unordered list (bullet points) (*<ul>*).

| HTML Code | Result |
| --- | --- |
| *<p>How to tie your shoes</p>*  *<ol><li>Loop</li>*  *<li>Swoop</li>*  *<li>Pull</li></ol>* | How to tie your shoes   1. Loop 2. Swoop 3. Pull |
| *<p>Shopping list</p>*  *<ul><li>Eggs</li>*  *<li>Milk</li>*  *<li>Bread</li></ul>* | Shopping List   * Eggs * Milk * Bread |

## More Help

For more help with creating accessible websites, please contact [Accessibility Technology Initiative (ATI)](https://www.cpp.edu/~accessibility/index.shtml).

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