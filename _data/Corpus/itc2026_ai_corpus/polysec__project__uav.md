**Source:** https://www.cpp.edu/polysec/project/uav

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

* 1

![unmanned aerial vehicle](../../img/securecommunications.jpg)

Securing the Communication of Unmanned Aerial Vehicle (UAV)

Researchers: J. Needleman, A. Barton, and M. I. Husain

[Previous](#CPPCarousel)
[Next](#CPPCarousel)

PolySec Lab

* [Home](/polysec/index.shtml)
* [About](/polysec/about.shtml)
* [Publications](/polysec/publications.shtml)
* [Projects](/polysec/projects.shtml)
* [Outreach](/polysec/outreach.shtml)
* [Competitions](/polysec/competitions.shtml)
* [Scholarship and Curriculum](/polysec/scholarship.shtml)
* [Sponsors](/polysec/sponsors.shtml)
* [Organizations and Resources](/polysec/organizations.shtml)
* [People](/polysec/people.shtml)
* [Contact](/polysec/contact.shtml)

# Securing Communications of UAVs

## About

Drones are fast becoming a popular consumer and commercial product. With the prominent use of drones throughout US military operations and subsequent security risks publicized by the media, this project aims to **survey possible attack vectors of consumer grade unmanned air vehicles** as well as, **testing whether or not these vectors are, in fact, possible on a consumer grade drone.**

## Dr. Mohammad Husain

Project Director

Professor at Cal Poly Pomona

## Joe Needleman

Project Lead

Student at Cal Poly Pomona

## Ashly Barton

Developer

Alumni at Cal Poly Pomona

## Project Details

### Hardware

*Parrot Drone AR 2.0*

The drone we used to complete our experiments was the Parrot AR 2.0. In terms of total revenue, Parrot is the 2nd largest drone company. The retail price of it’s most popular model is roughly $400. Once the drone is powered on, it hosts its own wireless network automatically. The user must connect to this network via their supported (android or iOS) device in order to fly the drone. It is also necessary to install a mobile application maintained by Parrot. This application has a “piloting mode” that ultimately unables the user to launch and maneuver the drone.

### Software

*Wireless Network Cracking*

Once we got on the firmware the telnet interface was running as root, so we were able to reconfigure the firewall - and effectively disable it using iptables. With the firewall down, it did not reconfigure or lock its elf down when a client connected allowing multiple clients to connect to the drone causing confusion on which user should stay connected. This action caused the drone to drop out of the air several times in our tests.

Further research indicated it would be ideal to use the drone as an embedded platform to track and monitor networks. We were able to reconfigure the drone to act as a Wireless Client and a Wifi AP, so we could both connect to the drone and use the drone to connect elsewhere. By cross compiling WPASupplicant (used on all Linux systems to authenticate WPA2), we were able to get the drone to connect to normal networks. This also gives us ability to brute force wireless connections in the area - first listing it and then attempting common passwords and storing the results.

Further efforts are still underway to compile the full sets of tools statically. This would allow us to use the drone to sniff all local packets and log it to storage or exploit local devices. This in theory could be returned, and use the drone in a malicious manner which would upload infected binaries to client phone or networks it hijacks. Unlike previous research, this does not require additional payloads (Pi) and can be done on the drone itself without degradation of flight.

Eventually, we will be continuing our research by introducing an additional drone and mimicking drone-on-drone attack vectors.

[![hardware ribbon cable](img/hardwa.jpg)

### Overview

*Hardware*](img/hardwa.jpg)

[![hardware circuit board](img/hardwar.jpg)

### Overview

*Hardware*](img/hardwar.jpg)

[![hardware ribbon cable and connector](img/hardw.jpg)

### Overview

*Hardware*](img/hardw.jpg)

[![hardware circuit board and cable](img/hard.jpg)

### Overview

*Hardware*](img/hard.jpg)

[![computer screen with file listing](img/user.png)

### Screenshot

*Software*](img/user.png)

[![computer screen listing wireless connections](img/soft.png)

### Screenshot

*Software*](img/soft.png)

[![computer screen with PID user listing](img/connect.png)

### Screenshot

*Software*](img/connect.png)

## Sponsors

This project would not be possible without the help of:

![Boeing](../../img/boeing.png)

![Northrop Grumman](../../img/northrop.png)

PolySec Lab

PolySec lab is a center for education and research in Information assurance, security and forensics at the department of Computer Science of Cal Poly Pomona led by Prof. Mohammad Husain.

Useful Links

* [Lab Director](https://www.cpp.edu/faculty/mihusain/)
* [Cal Poly Pomona](https://www.cpp.edu/)
* [CPP Computer Science Department](https://www.cpp.edu/sci/computer-science/)

Contact Info

3801 West Temple Avenue
 Pomona, CA 91768, U.S.

mihusain@cpp.edu

![PolySec Lab Cal Poly Pomona](https://www-test.cpp.edu/polysec/img/polysec-white.png)

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