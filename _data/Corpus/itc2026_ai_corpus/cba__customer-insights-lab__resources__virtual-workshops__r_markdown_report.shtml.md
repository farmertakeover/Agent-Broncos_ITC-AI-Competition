**Source:** https://www.cpp.edu/cba/customer-insights-lab/resources/virtual-workshops/r_markdown_report.shtml

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

Center for Customer Insights and Digital Marketing

* [Home](/cba/customer-insights-lab/index.shtml)
* [About](/cba/customer-insights-lab/about/index.shtml)
* [News](/cba/customer-insights-lab/news/index.shtml)
* [Student Success Programs](/cba/customer-insights-lab/student-success/index.shtml)
* [Research](/cba/customer-insights-lab/research/index.shtml)
* [Degree/Certificate Programs](/cba/customer-insights-lab/curriculum/index.shtml)
* Industry Partnership

  [Industry Partnership](/cba/customer-insights-lab/industry-partnership/services-to-business-community.shtml)
* [Resources](/cba/customer-insights-lab/resources/index.shtml)
* [Contact Us](/cba/customer-insights-lab/contact-us/index.shtml)

# Create an Analytics Report Directly from R

## Create a Great Report with R Markdown

The Center for Customer Insights and Digital Marketing presents a workshop on how to create a great report directly from R using the R Markdown package featuring Matheus Cordeiro, the junior data scientist. In this video, he provides live tutorials on what R markdown exactly is, what the benefits of using R markdown are, creating and comparing various types of reports (i.e., HTML, PDF, Word), and other important details that will allow you to create a successful report with R Markdown.

[If you haven’t installed R or R Studio yet, click here to learn how!](https://www.cpp.edu/cba/customer-insights-lab/news/event/install-r.shtml)

**Learning Outcomes**

1. Describe the R Markdown Structure
2. Explain capabilities and benefits of using R markdown
3. Compare and contrast creating PDF and HTML reports
4. Create output header appropriate for desired output file type
5. Explain R Markdown code structure
6. Create a report in desired file format (i.e., HTML, PDF, and Word) using R Markdown

**Check below to view the video!**

![](../../img/resources/matheus-workshop.png)

### Relevant Links and Code:

install.packages('tinytex')

tinytex::install\_tinytex()

install.packages()

<https://1.bp.blogspot.com/-Zc0T3aW4dNQ/Xa0i7XZFxYI/AAAAAAABXtk/LqZeCUGelnEFYYBAMah9aVjKTlDqpnahgCLcBGAsYHQ/s1600/98e23a08a6efb8d2de098595b156fcb61306eb19.jpg>

df\_corr <- round(cor(mtcars),2)

library(reshape)

melted\_corr <- melt(df\_corr)

library(ggplot2)

ggplot(data = melted\_corr, aes(x=X1, y=X2, fill=value)) +

  geom\_tile(color = "white")+

 scale\_fill\_gradient2(low = "blue", high = "red", mid = "white",

   midpoint = 0, limit = c(-1,1), space = "Lab",

   name="Correlation Scale") +

geom\_text(aes(X1, X2, label = value), color = "black", size = 4)

ggplot(mtcars, aes(x=wt, y=mpg)) +

  geom\_point() +  geom\_smooth(method=lm, se=FALSE)

ggplot(mtcars, aes(x=disp, y=wt)) +

  geom\_point() +  geom\_smooth(method=lm, se=FALSE)

{.tabset .tabset-dropdown}

[**https://rmarkdown.rstudio.com/**](https://rmarkdown.rstudio.com/)

[**https://www.linkedin.com/in/matheus-cordeiro-garcia/**](https://www.linkedin.com/in/matheus-cordeiro-garcia/)

[**https://www.rstudio.com/**](https://www.rstudio.com/)

Supplementary Video on How to Install R and RStudio:

<https://www.cpp.edu/cba/customer-insights-lab/news/event/install-r.shtml>

* [LinkedIn](https://www.linkedin.com/company/cpp-ccidm/)
* [Twitter](https://twitter.com/CPP_CCIDM)
* [YouTube](https://www.youtube.com/channel/UCNUbQ4K9q9UScG2hkIC-eoQ)

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