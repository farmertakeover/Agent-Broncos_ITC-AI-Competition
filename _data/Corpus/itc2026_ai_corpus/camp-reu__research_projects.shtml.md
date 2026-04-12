**Source:** https://www.cpp.edu/camp-reu/research_projects.shtml

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

NSF REU: Computational and Applied Mathematics Program

* [Home](/camp-reu/index.shtml)
* [Application Instructions](/camp-reu/application_instructions.shtml)
* [Research Projects](/camp-reu/research_projects.shtml)
* [Faculty Mentors](/camp-reu/faculty_mentors.shtml)
* [Important Dates](/camp-reu/important_dates.shtml)
* [Frequently Asked Questions](/camp-reu/faq.shtml)

# Research Projects

## Truck and Drone Delivery Scheduling

### Mentor: Dr. Jillian Cannons

Over the last two decades, e-commerce has risen to take a commanding role in the global economy,
resulting in order fulfillment logistics becoming a significant concern for retailers.  Concurrently, in a similar time frame, unmanned aerial vehicles, or drones, have transitioned from primarily military applications to a wide range of civil and commercial applications.  Correspondingly, considerable interest has arisen in the use of drones for last-mile delivery.  In particular, one approach is to combine the use of drones with existing delivery trucks in developing a schedule to deliver packages to a set of customers.  This hybrid approach is rich with variations based upon classifications such as the number of trucks, the number of drones, drone restrictions, how the trucks and drones interact, the goal of the schedule, and customer requirements.  Typically, solution techniques for this NP-hard optimization problem strive to either find an exact solution (most frequently using linear programming) or use efficient heuristic or metaheuristic algorithms.

In this project, REU students will study the truck and drone delivery scheduling problem.  The students will begin by establishing a foundation in the concepts of linear programming underpinning typical exact solution techniques.  The students will then briefly investigate the advantages and disadvantages of exact solutions versus metaheuristic approaches.  After examining recent work and analyzing open research directions, the students will develop, implement (using MATLAB), and compare both exact and metaheuristic solution approaches for a specific variant of the truck and drone delivery scheduling problem.  Current directions of focus are expanding existing work to support multiple trucks and to provide flexibility in drone rendezvous locations by permitting drones to return to a depot or a different truck.

## Metric Basis Reconfiguration

### Mentor: Dr. Briana Foster-Greenwood

Imagine releasing a robot into the environment.  The robot is able to detect its distance to several strategically placed sensors and send us a list of these distances.  From this list of numbers, can we figure out the exact location of the robot?  How many sensors are needed in order to have no ambiguity in determining the robot's location?  What is the optimal number of sensors and where should they be placed?  The answers to these questions may change depending on the robot's environment.  The robot location problem is an optimization problem which can be modeled using graph theory.  Different graphs correspond to different environments for the robot, and the metric dimension of the graph corresponds to the minimum number of sensors we would need in order to unambiguously determine where the robot is.

Reconfiguration graphs are a tool for investigating relationships between solutions to a problem.  The vertices of the graph are solutions to the problem and adjacency is determined by a specified "reconfiguration rule" for transforming one solution into another.  Reconfiguration problems that have previously been studied include vertex covers, independent sets, matching, dominating sets, *k*-coloring, list coloring, shortest paths, and more.

In this project, REU students will study metric basis reconfiguration.  Specifically, we fix a graph and consider all metric bases for the graph.  Using reconfiguration rules known as token sliding or token jumping to transition from one metric basis to another, we can then draw the corresponding reconfiguration graph and ask questions about its structural properties.  Is the graph connected?  What is its diameter?  What do shortest paths look like?  Prior student research groups have investigated cycles, paths, prisms, and fan graphs.  For this project, students will explore other graph families such as grid graphs, complete bipartite graphs, and trees.  The number of metric bases of a given graph can be quite large, so programming (for instance with SageMath) will facilitate generating and visualizing examples from which to make conjectures.

## Kernel Engineering in Gaussian Processes and Support Vector Machines

### Mentor: Dr. Jimmy Risk

Kernel engineering, a specialized field within Gaussian processes (GPs) and support vector machines (SVMs), offers a rich and accessible research area for undergraduate students.  Kernel engineering's appeal lies in its applicability across various domains and its potential to model complex nonlinear relationships through both GP regression and SVM classification.  By focusing on the design and optimization of kernel functions, this project aims to provide a hands-on experience that bridges theoretical understanding with practical applications in time series analysis, image processing, mathematical finance, and/or actuarial (mortality) studies.

In this project, REU students will embark on a journey to explore kernel engineering.  To begin, students will learn the fundamentals of kernel functions, GPs, and SVMs.  Students will then investigate specific applications, with a focus on understanding the underlying mathematical principles and their real-world relevance.  Using programming languages such as R and Python, students will engage in hands-on algorithm design and optimization. Finally, students will apply their models to real-world data, fostering a deeper appreciation for the subject matter and its practical implications.

## Vibrations and Sound Synthesis

### Mentor: Dr. Ryan Szypowski

There are numerous ways to deeply connect the seemingly disparate fields of mathematics and music, such as through the study of acoustics, or by considering musical form from the perspective of symmetry.  One such connection of interest is the relationship between harmonic sounds and the vibrations of a string, which provides for many rich mathematical explorations.  It has long been noted that sound waves whose frequencies are related through multiplication by simple fractions sound consonant with each other, while Fourier analysis shows that the sound made by a simple vibrating string consists of the superposition of a fundamental mode and overtones whose frequencies are integer multiples of the fundamental frequency.  On the other hand, some instruments such as bells or the xylophone are based on the vibrations of a larger body and therefore have a different (possibly inharmonic) overtone series, where the frequencies of the modes are not necessarily related in the same fashion.  Recent work has been done to utilize features in order to synthesize new sounds by "sound morphing" between the timbres of two different instruments with similar frequency profiles, and it may be possible to extend these method to interpolate between instruments with different overtone frequency components.

In this project, REU students will learn about various elements found in this specific intersection of mathematics and music.  The work will begin by learning the fundamentals of Fourier analysis applied to the one-dimensional wave equation, and then learning about additive (digital) sound synthesis and timbre of musical instruments.  From here a number of research avenues open up depending on student interest and past preparation.  Two potential directions include using finite element techniques for spectral analysis of more complex vibrating bodies (such as cymbals or bells) or using signal filtering and deep learning techniques for feature identification and sound morphing.  Furthermore, students may combine efforts along both paths to extend current techniques to interpolate between sounds with very different frequency profiles.  Alternately, different techniques, such as through the use of ordinary differential equations, may be explored for sound synthesis.  Regardless of the path followed, the students will implement appropriate computational methods (using MATLAB or Python) in order to experience the results, providing a unique opportunity to see (and hear) content from mathematics and music come together.

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