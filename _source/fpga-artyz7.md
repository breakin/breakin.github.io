---
layout: post
date: 2018-13-06
title: FPGA Arty Z7-20
tags: electronics, fpga
theme: electronics
landing: drafts
---

I recently bought a Arty Z7-20 FPGA development board from Digilent. [Link](https://store.digilentinc.com/arty-z7-apsoc-zynq-7000-development-board-for-makers-and-hobbyists/). The main motivation was to have a 7-series FPGA so I could get Vivado support. ISE just felt old and buggy! I also wanted a slightly larger FPGA in terms of block ram and DSP-units. Going into this I will not use the Z-portion of the card, that is I will not use the ARM core for the time being.

# Start

I plugged the board in using a micro-USB cable. RGB LEDs started blinking and pushing buttons seemed to affect the LEDs. The program that is preloaded is [https://reference.digilentinc.com/learn/programmable-logic/tutorials/arty-general-io-demo/start](https://reference.digilentinc.com/learn/programmable-logic/tutorials/arty-general-io-demo/start) ([git](https://github.com/Digilent/Arty-GPIO)). The code doing the actual blinking can be found [here](https://github.com/Digilent/Arty-GPIO/tree/master/src/hdl).

At this point it was time to create a "Hello World" program. I used the wizard and I specified no constraints file (.XDC), insteading relying on the Arty Z7-20 board file.

Steps:
* Downloading Vivado
	* I somehow did not get an icon on the desktop or anywhere but Vivado could be launched using C:\Xilinx\Vivado\2017.4\bin\vivado.bat
* Installing board files into Vivado
	* https://reference.digilentinc.com/reference/software/vivado/board-files
	* https://github.com/Digilent/vivado-boards/
	* https://github.com/Digilent/vivado-boards/tree/master/new/board_files/arty-z7-20/A.0
* Creating a Vivado project
	* Choose board in wizard. XDC?

Resources:
* [Resource Center Arty Z7](https://reference.digilentinc.com/reference/programmable-logic/arty-z7/start)
* [Arty](https://reference.digilentinc.com/reference/programmable-logic/arty/start)

In progress:
* https://forums.xilinx.com/t5/Embedded-Processor-System-Design/Board-file-XML-and-Constraints-file-XDC-in-Vivado/m-p/673380#M29471