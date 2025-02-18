MiKoBots Studio is an opensource project, designed to control diy robot arms. So if you have designed your own robot arm and don't know how to control it, you can use MiKoBots Studio. The software has a lot of features build in to get the maximum out of your robotic arm, like:

* Blockly programming
* Simulation, you can upload the 3d model of your robot arm and simulate it.
* Export and import robot arms, with the software you can easily configure and share your ptofile with others
* Vision control build in the librery that allows you to connect a camera to the software to give your robot eyes
* Bluetooth and usb connectivity
* Add input and output signals

![MiKoBots Studio](MiKoBots_Studio/assets/images/MiKoBots_studio.png "MiKoBots Studio")

At the moment the following requirements are in place if you want to control your own robot arm.

**Requirements:**
* 6(RRRRRR), 5(RRRRR) or 3(RRR) axis robot arm 
* Type of motor: Stepper motors or servo
* Limit swithes: each joint should have a limit switch to set the home position, except the joints with servo's
* Microcontroller: ESP32, Arduino mega

**Version MiKoBots Studio:**
The current released version and which can be donwloaded on https://mikobots.com/ is: V1.15

**History MiKoBots Studio:**<br>
Version: 1.15<br>
Date: 18-2-2025<br>
* fixed some bugs regarding saving settings, connecting IO

Version: 1.14<br>
Date: 11-1-2025<br>
* added support for arduino mega boards
* besides stepper motor you can also choice out of a servo


Version: 1.13<br>
Date: 7-12-2024<br>
* Fixed a bug, related to connecting the robot to the software

Version: 1.12<br>
Date: 6-12-2024<br>
* Fixed a bug, not able to import new robot

Version: 1.11<br>
Date: 5-12-2024<br>
* More vision function
* Play and pause button for the robot
* Automaticcly closing of the connect windows
* and fixing some bugs that appears in the earlier vesion

Version: 1.1<br>
Date: 9-11-2024<br>
A lot of new updates since version 1.0, the mostimportant updates are:
* Connectivity with bluetooth
* Blockly programming 
* Seperate window for the robot settings
* Available for macOS

Version: 1.0<br>
Date: 1-10-2024<br>
First official release of MiKoBots studio.


**Version MiKoBots firmware:**
The current released version and which can be donwloaded on https://mikobots.com/ is: V1.22