**Source:** https://www.cpp.edu/bigdatasec-reu/projects.shtml

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

REU in Big Data Security and Privacy

* [Home](/bigdatasec-reu/index.shtml)
* [Program Overview](/bigdatasec-reu/overview.shtml)
* [Application Instructions](/bigdatasec-reu/application.shtml)
* [Research Projects](/bigdatasec-reu/projects.shtml)
* [Faculty Advisors](/bigdatasec-reu/faculty.shtml)

# Introduction of Sample Research Projects

## Project 1: Privacy Preserving Deep Learning

Machine learning models especially deep learning models have been widely applied on various types of data, and will further transform many aspects of our daily lives. However, these popular machine learning algorithms typically were developed without a thorough consideration of data security and privacy issues. When it comes to big data with high volume, variety and velocity, existing data security solutions fall short in efficiency, flexibility, and scalability. These security and privacy challenges either endanger some critical technology to malfunction (e.g., self-driving cars could misclassify a stop sign as a yield sign with the computer vision learning model under adversarial attack) or undermine the promising future that big data and machine learning can bring us (e.g., with unsolved privacy issues, human genome-based personalized medicine and medical practice will be delayed). In this project, our goal is to solve the data privacy issues when a deep learning model is trained in a cloud. We aim to design and develop a new protocol which provides privacy preservation for the training and test input data, under the semi-honest security model, and guarantees the accuracy and efficiency of prediction at a reasonable level. In this project, Keras/Tensorflow, and the crytographic library SEALs are used.

Faculty Advisor: Dr. Chen

## Project 2: Adversarial Machine Learning and Defense

Since the advent of machine learning to the field of computer vision, image classification software has surpassed human capabilities and enabled new technologies including facial recognition authentica- tion, self-driving cars, and smart security cameras. However, a unique challenge threatens these technologies: the existence of images which appear normal to humans, but reliably fool image classifiers. The carefully manipulated adversarial samples are called adversarial examples. In this project, we aim to explore different ways of generating adversarial examples, and study the countermeasures to defense against such attacks.

Faculty Advisor: Dr. Ji, Dr. Chen

## Project 3: Using Machine Learning for Intrusion Detection in Encrypted Network Traffic

The network security solutions, such as next-generation firewalls, network intrusion detection system (NIDS) and network intrusion prevention system (NIPS), are based on deep packet inspection technique (DPI). Deep packet inspection is currently the predominant technique of examining network traffic. Deep packet inspection inspects the content of packet including the packet header and the packet payload and makes decision based on predefined rules depending on what a packet contains. An efficient and robust deep packet inspection technique requires visibility into content and context. Nowadays, more than 80% of enterprises’ web traffic is encrypted; 94% of all Google web traffic is encrypted. Therefore, the visibility across the network is getting increasingly difficult, and our traditional deep packet inspection cannot assume that the content of the packet is available for inspection. Moreover, many malwares use encryption techniques such as TLS to encrypt the communication traffic to evade the detection of firewall and network intrusion detection system. In this research, we will explore two tracks:

* Feature engineering track: REU students in this track will use two or three public datasets to understand encrypted traffic and master network traffic analysis tools such as Zeek. Then, students use that tool to investigate and extract metadata about network traffic that have the most discriminatory power between benign and malicious traffic.
* Machine learning track: students will use the contextual information that have been extracted from feature engineering track into different type of machine learning algorithms. Students will learn and choose the Machine Learning algorithm that significantly distinguish encrypted malicious network traffic from encrypted benign traffic with high accuracy, low false-positive rate.

Faculty Advisor: Dr. Amamra

## Project 4: Smart Grid Cyber Threat Testbed and Analysis

Power systems are becoming more computerized and integrated with the cyber world like never before. Entering another realm, such as cyber space, poses new threats and issues for modern day power systems with high volume of data. In order to understand those threats, a cyber-power test bed must be developed for testing cyber-attacks on a power system and along with its crucial components and data. The cyber-power test bed in development will include the RTDS (Real Time Digital Simulation) machine for simulating the power system, a computer with a virtual machine that will simulate the power system via RSCAD, a database to store the important data for the power system that is streamed via OpenPDC [44], an attacking computer with a virtual machine containing common hacking tools, and a network switch to place all virtual and real machines on the same network for an isolated testing environment.

In this research, the creation of a cyber testbed is the first step in understanding the cyber threats that are present in the current world with big data as well as understanding how to defend from cyber threats. To follow up the creation of this testbed, it must be attacked, the response must be analyzed, and a defense must be introduced and tested. REU students will fully understand the networking, including the multiple layers that a network typically consists of in smart grid, the functions of network devices, and the logic behind networks. They will also explore the vulnerability of the testbed with additional intelligent electronic devices on the power system such as a SEL 311 Protection Relay, the addition of power system stabilizers, a larger computer network, and better system security.

Faculty Advisor: Dr. Monemi

## Project 5: Classification of phishing e-mail contents according to FFM personality bias using Natural Language Processing (NLP)

A general approach for phishing susceptibility analysis is to profile the user’s personality using personality models such as the Five Factor Model (FFM) and find out the susceptibility for a set of phishing attempts. The FFM is a personality profiling system that scores participants on five separate personality traits: Openness to experience (O), Conscientiousness (C), Extraversion (E), Agreeableness (A), and Neuroticism (N). It is often known as the OCEAN or CANOE model. However, these approaches don’t consider the fact based on the content. For example, a phishing email offering an enticing free prize might be very luring to a dominant O-personality (curious, open to new experience), but not to an N-personality (tendency of experiencing negative emotion). Therefore, it is necessary to consider the personality bias of the phishing e-mail contents during the susceptibility analysis. The main goal of this project is to build a system that can correlate a person’s FFM profile to their susceptibility to one or more types of phishing e-mails.

Faculty Advisor: Dr. Husain

## Project 6: Parallel Algorithms for Large Scale Cyber Anomaly Detection on Heterogenous Computing Environments

Anomaly detection aims to identify outliers or variations from normal behavior that indicate the occurrence of various cyber events including host-based and network-based attacks. Machine learning techniques, such as supervised and unsupervised learning, have shown to be effective in detecting such anomalies. In this research project we focus on two key emerging computational challenges in this problem space, specially the large amounts of instrumentation data generated by cyber environments and time/resource constraints on the detection technique and explore computational solutions that utilize parallel processing techniques. In this project, we will focus on formulating parallel algorithms designs for cyber anomaly detection. We will explore coarse grained and fine-grained parallelism for computing environments which have a combination of multi-core and many core processors. This project will involve research that will leverage existing parallel designs for shared and distributed memory architectures and will aim to combine them, so as to allow cyber anomaly detection to be conducted using a heterogenous computing environment.

Faculty Advisor: Dr. Korah

## Project 7: Detecting Hidden Information in Video Games

Video games are a global industry worth over $100 Billion, rivaling the professional sports industry in size. There are large video game tournaments paying out millions of dollars in prizes. Such large monetary values also attract players using less honest methods to gain an edge over the competition. While there is existing work in detection of cheats based on anomalous behavior or debugging software running on the client-machine or malicious instructions sent to the server, attacks that only passively observe a game are understudied. In other areas, however, various such side-channel attacks have been shown to allow the extraction of private information, for example using memory access timing. We propose that an attacker could e.g. monitor network traffic, and despite its encryption, infer information that would normally be hidden from the player, such as an enemy coming closer. As the first step to detect an attacker is to determine their capabilities, we would like to investigate these options in more detail. There are several attractive targets for this line of research, including the popular games DotA2, Fortnite or Starcraft II. There are several options for REU students to explore, including: a) Record network traffic from a third-party machine, or measure CPU and/or GPU usage and correlate this information with game-play events using Machine Learning techniques. b) Determine how such exploits can feasibly be detected or thwarted. c) Use such exploits to construct an illicit communication channel within a game that AI agents can use to communicate with each other undetected, as an extension and new application of our prior work.

Faculty Advisor: Dr. Eger

## Project 8: Vulnerability Exploitation Prediction

Prediction of software vulnerabilities that are likely to be exploited by malicious hackers. Standard vulnerability score systems like CVSS are known not to be useful for patch prioritization. By exploring AI, machine learning, and SNA (Social Network Analysis) techniques on features computed from hacker environments on the deepweb, the darkweb, and on social media (socialD2web), this project attempts to mine vulnerabilities mentioned directly or indirectly by credible hackers.

Faculty Advisor: Dr. Marin

## Project 9: Hacker Engagement Prediction

Hacker communities are continually evolving. Due to social influence effects, values are often transmitted from one person to another and this behavior is also observed among malicious hackers. Holding acknowledged reputations, hackers generally use online platforms to advertise exploits, vulnerabilities, techniques, code samples, and targets and also to recruit individuals for malicious campaigns, attracting low-skill-level individuals who aim to improve their hacking skills. Those influential activities not only expand the hackers’ networks, bringing like-minded collaborators and learners, but also help them to increase revenue. Therefore, this research project studies the hacker adoption behavior online, using it as crowdsourced sensor to gain insight about future users’ activities that may lead to cyber-attacks, such as recruitment or mass adoption of exploits.

Faculty Advisor: Dr. Marin

## Project 10: Cascade Prediction

Predicting when a hacking message will go “viral” is important for cybersecurity, since information cascades can signal hacktivism campaigns or mass adoption of cyber-threats. Then, this project tries to model information diffusion on hacker communities, investigating which influential and topological patterns can be leveraged for the early extraction of popular threads.

Faculty Advisor: Dr. Marin

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