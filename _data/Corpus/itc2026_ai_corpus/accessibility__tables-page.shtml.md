**Source:** https://www.cpp.edu/accessibility/tables-page.shtml

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

# Implementing Accessible Tables

## Introduction

Tables are used to present information in an organized format. When adding tables to a webpage, it is important to understand the type of table that should be used. There are two type of tables: data tables and layout tables.

### Data Tables

Data tables are used to organize data with a logical relationship in grids. To ensure users that rely on assistive technology can perceive information presented, tables must indicate header cells and data cells that define their relationships.

Tables must be marked with the <table> HTML tag to ensure data is structured, meaningful, and accessible to all users.

Each row within the table must be marked with the <tr> HTML tag to structure the table into rows.

Header cells within tables must be marked with table header <th> HTML tag to provide context for the data. The tag informs screen readers and other accessibility tools that a particular cell serves as a label for a row or column. This allows users to understand the relationship between data points and their corresponding headers.

Data cells within tables are identified as the table data <td> HTML tag. The tag informs screen readers and other assistive technologies that a cell holds information related to a corresponding row or column header. This is imperative because it allows assistive technologies to link each data cell with the right header and present the information in full context.

Document formats other than HTML, including PDFs, have mechanisms to markup table structures. Word processing apps such as Microsoft Word may also provide similar mechanisms to markup tables. Table markup is often lost when converting from one format to another; however, some applications may be able to convert table markup.

### Layout Tables

Layout tables are used to arrange information on a webpage, and do not have headers or data cells. It is recommended to **avoid** the use of layout tables because they can disrupt the reading order for users who rely on assistive technology (such as screen readers) to navigate a webpage. **Instead****, use a CSS based layout (such as Divs), which provide more control over the visual display without compromising the structure.**If layout tables are used, the following steps must be taken:

* The content should remain in a clear and logical reading order, even when it is not shown in a table
* Layout tables should not be used if the information in the table presents data
* Review the layout table and determine whether if a CSS based layout can be used

## Implementing Accessible Tables

### Simple Data Table Example

The table purposely displays the HTML table markups. In the example, the table headers "First Name", "Last Name", and "GPA" are marked with the <th> tag. The table data associated with the headers such as "Billy", "Bronco", and "4.0" are marked withe the <td> tag.

Student GPA (with Table Markups)

| **<th>First Name</th>** | **<th>Last Name</th>** | **<th>GPA</th>** |
| --- | --- | --- |
| **<td>**Billy**</td>** | **<td>**Bronco**</td>** | **<td>**4.0**</td>** |
| **<td>**Jane**</td>** | **<td>**Doe**</td>** | **<td>**2.0**</td>** |

How the table is presented to the user:

Student GPA

| **First Name** | **Last Name** | **GPA** |
| --- | --- | --- |
| Billy | Bronco | 4.0 |
| Jane | Doe | 2.0 |

### Complex Table Example

The table purposely displays HTML table markups. Complex tables have headers that span across multiple data table columns, or data tables that span multiple rows. While visual users may be able to easily understand the information presented, users who rely on assistive technology (such as screen readers) may experience difficulty perceiving the same information. Therefore, cells must be appropriately associated.

Student GPA (with Table Markups)

| **<th colspan="2">Name</th>** | | **<th>GPA</th>** |
| --- | --- | --- |
| **<td>**Billy**</td>** | **<td>**Bronco**</td>** | **<td>**A**</td>** |
| **<td>**Jane**</td>** | **<td>**Doe**</td>** | **<td>**B**</td>** |

How the table is presented to the user:

Student GPA

| Name | | Grade |
| --- | --- | --- |
| Billy | Bronco | A |
| Jane | Doe | B |

### Caption and Summary

A caption identifies the main topic of a table and is useful in most situations. A summary provides orientation or navigation guidance in complex tables.

### Testing Methods

**Manual Testing Procedures**

**Data Table**

1. Review the source code and manually verify if the table is marked up correctly. Source code can be inspected on most web browsers by using the **Ctrl**+ **Shift** + **I**key combination or the **F12**key.
2. Look for the following attributes:
   - <Table>
   - <Tr>
   - <Th>
   - <Td>
   - <Header>

**Layout Table**

Visually inspect the layout table and determine whether if the table is better presented as a data table or a CSS based layout.

**Assistive Technology testing**

Screen readers, such as NVDA, can be used to determine the accessibility of a table. Navigate the screen reader towards the beginning of a table, and verify if the screen reader recognizes that there is a table present. Test if the information is presented in a way that is contextual, logical and understandable to a user.

## WCAG 2.1 and References

### Web Content Accessibility Guidelines (WCAG 2.1)

* [Guideline 1.3 - Adaptable](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_overview&tags=tables#adaptable)
  + [Success Criterion 1.3.1 - Info and Relationships](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_overview&tags=tables#info-and-relationships)
  + [Success Criterion 1.3.2 - Meaningful Sequence](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_overview&tags=tables#meaningful-sequence)
* [Guideline 2.4 - Navigable](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_overview&tags=tables#navigable)
  + [Success Criterion 2.4.6 - Headings and Labels](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_overview&tags=tables#headings-and-labels)

### Other Resources

* [WebAIM: Creating Accessible Tables](http://webaim.org/techniques/tables/data)

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