**Source:** https://www.cpp.edu/cba/customer-insights-lab/resources/virtual-workshops/interactive-shiny-r-apps.shtml

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

# Bring Data to Life: Create Interactive Apps with Shiny in R

## Bring Data to Life: Create Interactive Apps with Shiny in R

Discover how to transform your data into interactive web applications with Shiny, a powerful R package designed for creating dynamic user interfaces. In this hands-on workshop, you'll learn how to build and customize Shiny apps, create reactive data visualizations using packages like ggplot2 and plotly, and deploy your apps online. Whether you're new to programming or an R user looking to expand your skills, this workshop will guide you step-by-step through the process of turning static data into engaging, interactive experiences. The workshop will be led by CCIDM’s Marketing Analytics specialist, Jarrod Griffin, who is also a student in the [Master of Science in Digital Marketing](https://www.cpp.edu/cba/graduate-business-programs/programs/master-degree-in-digital-marketing-and-marketing-analytics.shtml).

**Learning Outcomes**

1. **Understand Shiny App Structure:** Participants will learn the fundamental architecture of Shiny apps and how to structure code using ui.R/server.R or app.R.
2. **Implement Reactive Programming:** Attendees will gain the skills to create dynamic, interactive Shiny applications using reactive values and expressions.
3. **Build Interactive Data Visualizations:** Participants will learn to incorporate and customize interactive plots with packages like ggplot2 and plotly for responsive data visualization.
4. **Deploy Shiny Apps on Various Platforms:** Attendees will be able to deploy Shiny apps to platforms such as shinyapps.io and shinylive, making the apps accessible online.
5. **Secure Shiny Applications:** Participants will learn about securing Shiny apps, including implementing authentication and understanding best practices for protecting sensitive data.

![](../../img/resources/shiny-workshop-flyer.png)

## Workshop Preparation:

### Accessing R and RStudio

To get the most out of this workshop, please ensure you have access to both R and RStudio. You can do this by either downloading and installing them to your computer or by setting up a free Posit Cloud account.

#### Options for Accessing R & RStudio:

* Posit Cloud (online option) - [Get started here](https://posit.cloud/)
* Install R & RStudio on Windows - [Watch this tutorial](https://www.youtube.com/watch?v=7nY1jafrfiw)
* Install R & RStudio on macOS - [Watch this tutorial](https://www.youtube.com/watch?v=URqrA8hzCCg)

### Introduction to R & RStudio (Optional)

While not required, we encourage you to watch the following workshop beforehand if you can set aside an hour.

* [Introduction to R and RStudio](https://www.cpp.edu/cba/customer-insights-lab/resources/virtual-workshops/r_workshop_1.shtml)

## During the Workshop:

```
5:50: https://posit.cloud/

8:42:
packages <- c("shiny",
              "tidyverse",
              "shinydashboard",
              "plotly",
              "DT")

missing_packages <- packages[!packages %in% installed.packages()[, "Package"]]
if (length(missing_packages) > 0) {
  install.packages(missing_packages)
}

14:45:
library(shiny)

ui <-

server <- function(input, output) {

}

# Run the application
shinyApp(ui = ui, server = server)

23:15:
library(shiny)
library(tidyverse)
library(shinydashboard)
library(plotly)
library(DT)

post_data.df <- read_csv("https://raw.githubusercontent.com/jsgriffin96/shiny_r_workshop/refs/heads/main/data/Post%20Data.csv") %>%
  mutate(across(c("Date", "Revenue"), ~ str_extract(.x, "\\d+"))) %>%
  mutate(across(c("Date", "Revenue"), as.numeric)) %>%
  mutate(Post_Type = factor(Post_Type, levels = c("Featured Product", "Announcement", "Event Showcase", "Employee of the Week"))) %>%
  arrange(Date)

30:25:
selectInput("post_type", "Post Type:", choices = unique(post_data.df$Post_Type), multiple = TRUE),

35:07:
box(title = "Total Conversions per Day",
    status = "primary",
    solidHeader = TRUE,
    collapsible = TRUE,
    width = 12,
    plotlyOutput("conversionsTimeSeries"))

41:49:
filtered_df <- reactive({
  req(input$post_type)

  post_data.df %>%
    filter(Post_Type %in% input$post_type)
})
```

## Complete Code and Presentation:

<https://github.com/jsgriffin96/shiny_r_workshop>

---

[Click here to see all of our workshops that cover topics like: SQL](https://www.cpp.edu/cba/customer-insights-lab/resources/virtual-workshops/index.shtml)

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