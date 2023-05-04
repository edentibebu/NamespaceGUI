# NamespaceGUI
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]




<!-- PROJECT LOGO 
<br />
<div align="center">
  <a href="https://github.com/edentibebu/NamespaceGUI">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->
<h3 align="center">Namespace GUI</h3>

  <p align="center">
    Our project is an enhancement to the Linux userspace that is a graphical user interface for namespaces. This is a significant modification which would improve the user experience in creating namespaces and editing namespaces, as the current interface is through command line only. 
    <br />
    <br />
    <!--<a href="screenshots/demo.mkv">View Demo</a>-->
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">The Breakdown</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>

  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


We've created a GUI for namespaces. Our project is an enhancement to the Linux userspace that is a graphical user interface for namespaces. This is a significant modification which would improve the user experience in creating namespaces and editing namespaces, as the current interface is through command line only. 

Functionality Features:
New namespace creation with an interface that will cover most-used command-line arguments
Creating veth devices and linking them between two namespaces
Displaying current namespaces and their devices
Port forwarding 
Monitoring additions/deletions of namespaces made outside GUI
Removing namespaces

Security Features: 
Check if namespaces are modified via command line while GUI is open 
The GUI access differs based users' permissions.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### The Breakdown


* screenshots
  ```txt
  This folder contains screenshots and images of the interface.
  ```
* main.py
  ```txt
  This is what starts up the GUI using Python’s tkinter package and what starts a thread
  running our inotify functionality. When using the GUI, one should run python main.py, and if they
  are the root user or have root privileges, one should prepend this command with sudo, so that full
  functionality of our GUI is available. Without root privileges, one will run into alerts that do two
  things: (1) do not allow non-root users access to see/access/edit certain information (2) provide a
  pop-up window that alerts the user that they do not have the privileges to see/access/edit certain
  parts of the network namespaces.  
  ````
* home.py
  ```txt
  Upon running the GUI, we load up a home page. This page lists the current network namespaces that are on the system, where each of these items is a button, which can be clicked on and takes the user to view/edit details regarding that namespace. There is also functionality here to
  click the (+) button to add a namespace, which then pops up a separate window to add a network
  ```
* utils.py
```txt
  A lot of our work that interfaces with the operating system is done via bash scripts. This
  file contains several functions which run a few lines of bash scripting to get some output, then parse
  this output to be returned for displaying in a human readable format, which gets displayed on the GUI.
  This file also contains some general purpose functionality that is used across several windows/parts of
  our GUI. For example, the show alert function is used across the entire GUI and we keep it in utils.py
  so that it is easy to access and avoids redundancy in our code.
```
* add net ns.py: 
```txt
This brings up a separate window for adding a network namespace, and users can
specify the name of the namespace they are creating. Once the ”submit” button is clicked, you will see
a live update of the home page with the newly added namespace. We know that with network names-
paces, the local loopback is not automatically enabled, but in our GUI, adding a network namespace
runs the bash command to enable local loopback automatically, making our GUI a more convenient
experience for users.
```
* ns view.py: 
```txt
To view details and edit details about the network namespace, users can click on the name
of a network namespace on the home page. In this view, users can add devices, delete the namespace,
or set up port forwarding.
```
* add device.py: 
```txt 
Within the namespace view, users can add a port to the network namespace so that
they can communicate with other namespaces. They have the option to select which device numbers
they want to add to the subnet and which other namespace they want to communicate with, via a
dropdown with these namespaces as options. Something we considered here is if a user tries to add a
line of communication between namespaces, with only one namespace created, they are shown an alert
which tells them that they must have multiple network namespaces in order to communicate between
them.
```
* port forwarding.py: 
```txt
If users want to enable port forwarding from one namespace to another, they
can click the button to add port forwarding, which opens up a separate window and provides options
to connect to a different device in a different namespace, and users can type in the port numbers that
they want to forward to and from.
```
* inotify gui.c: 
```txt
We realize that there could be security issues with edits being made to the OS via
command line and also through our GUI. We have chosen to handle this by using inotify to monitor
whether changes are being made via command line while our GUI is open.
```
* index.html: 
```txt 
This is a test page being used to verify the port forwarding between 2 network namespaces.
Using port forwarding, this html page can be hosted with a web server on one namespace and then
accessed using the IP address of the other namespace due to port forwarding.
```
* gui log.txt: 
```txt 
A text file whose contents consist of the most recent changes done in the GUI. This in-
cludes adding and deleting namespaces directly from the GUI. Whenever these event occur, gui log.txt
is updated with either ”{namespace} was created” or ”{namespace} was deleted”.
```
* output.txt: 
```txt 
A text file whose contents consist of the most recent changes to the namesapces on the
system. Similar to gui log.txt, this file is updated upon adding and deleting namespaces, both from
the GUI and on the terminal. This file is compared with gui log.txt to see if the most recent change
made in the namespaces were from the GUI or not. If the last line of these files are the same, it means
that the most recent change came from the terminal.
```
### Installation
1. Make sure you have the latest installment of python on your system. You can do this by going to this <a href="https://www.python.org/downloads/">website</a>

2. Clone the repo
   ```sh
   git clone https://github.com/edentibebu/NamespaceGUI.git
   ```
3. Navigate to the NamespaceGUI directory
   ```sh
   cd NamespaceGUI
   ```
4. Launch the python program main.py
   ```sh
   sudo python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
The image below is of the home page. It displays all the current namespaces. To see more details for a specific namespace, click on the name. 

* ![](screenshots/home_page.png)
<br>
Clicking on a namespace takes you to the namespace page view. This displays all the capabilities and their status (whether they are enabled/disabled), which can be toggled using the checkboxes.

* ![](screenshots/capabilities.png)
<br>
Also on the namespace page view are the current running processes for that specific namespace. Information like the user, pids, cpu and memory usage, etc. are shown in a table.

* ![](screenshots/processes.png)


<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/edentibebu/NamespaceGUI.svg?style=for-the-badge
[contributors-url]: https://github.com/edentibebu/NamespaceGUI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/edentibebu/NamespaceGUI.svg?style=for-the-badge
[forks-url]: https://github.com/edentibebu/NamespaceGUI/network/members
[stars-shield]: https://img.shields.io/github/stars/edentibebu/NamespaceGUI.svg?style=for-the-badge
[stars-url]: https://github.com/edentibebu/NamespaceGUI/stargazers
[issues-shield]: https://img.shields.io/github/issues/edentibebu/NamespaceGUI.svg?style=for-the-badge
[issues-url]: https://github.com/edentibebu/NamespaceGUI/issues
[license-shield]: https://img.shields.io/github/license/edentibebu/NamespaceGUI.svg?style=for-the-badge
[license-url]: https://github.com/edentibebu/NamespaceGUI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png

[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/