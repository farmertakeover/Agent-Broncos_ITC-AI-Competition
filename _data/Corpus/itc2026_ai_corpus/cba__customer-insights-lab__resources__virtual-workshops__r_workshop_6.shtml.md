**Source:** https://www.cpp.edu/cba/customer-insights-lab/resources/virtual-workshops/r_workshop_6.shtml

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

# R Workshop #6: Data Visualization with R

## Data Visualization with R

This final workshop will deal with visualizing data, using R’s built-in functions as well as popular packages such as ggplot2 and lattice. Specifically, participants will learn how to create the most appropriate chart when data involves one variable or two variables, categorical or continuous variables. We will progress from the simplest to the most sophisticated charts, by adding layers of specification systematically, to create the kind of quality charts that may appear in WSJ or the Economist.

[If you haven't installed R or RStudio, click here to learn how!](https://www.cpp.edu/cba/customer-insights-lab/news/event/install-r.shtml)

**Learning Outcomes**

1. Describe three popular packages that allow one to visualize data.
2. Explain the concept of the grammar of graphics when visualizing data with the ggplot2 package.
3. Create a chart when there is only one continuous variable or one categorical variable.
4. Create a chart when there are two variables where the dependent variable is continuous and the independent variable is either categorical or continuous.
5. Create a chart by adding a categorical moderator to the chart involving one variable or two variables.
6. Create a chart after filtering data using tidyverse functions.

**Check below to view the video!**

![](../../img/training-images/workshop-6-verti.png)

### Relevant Links and Code:

Workshop #6 GitHub: <https://github.com/jsgriffin96/r_workshop_6>
install.packages('tidyverse')
install.packages('ggrepel')
install.packages('ggthemes')
install.packages('scales')
install.packages('plotly')
install.packages('lattice')
install.packages('GGally')
library(tidyverse)
library(ggrepel)
library(ggthemes)
library(scales)
library(plotly)
library(lattice)
library(GGally)

cars <- mtcars %>%
  as\_tibble() %>%
  add\_column(rownames(mtcars))
colnames(cars)[12] <- 'model'
<https://www.r-graph-gallery.com/index.html>
<https://rstudio.com/resources/cheatsheets/>
<https://r4ds.had.co.nz/data-visualisation.html>

---

Supplementary Video on How to Install R and RStudio:
<https://www.cpp.edu/cba/customer-insights-lab/news/event/install-r.shtml>
Supplementary Video on How to Link RStudio and Github:
<https://www.youtube.com/watch?v=ssEYd8T07y4&feature=youtu.be>

---

* [LinkedIn](https://www.linkedin.com/company/cpp-ccidm/)
* [Twitter](https://twitter.com/CPP_CCIDM)
* [YouTube](https://www.youtube.com/channel/UCNUbQ4K9q9UScG2hkIC-eoQ)

![](/cba/customer-insights-lab/img/home/ccdm-logo-banner.png)

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