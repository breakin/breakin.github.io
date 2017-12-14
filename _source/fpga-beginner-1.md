---
layout: post
date: 2018-09-18
title: FPGA beginners guide #1
tags: electronics, fpga
theme: electronics
landing: drafts
---

Introduction
============
I've been spending some time playing around with FPGAs. It has been quite challenging since they don't allow for as much sloppiness as a microcontroller. I will here assume that a FPGA is the right tool for you and describe how my understanding improved from super beginner level to beginner level.

First lets talk about what a FPGA is. My first inclination to look into FPGAs was that I was desillusioned by the slow GPIO-rate of devices such as the raspberry PI. GPIO here means general purpose input/output and I used the raspberry to read inputs and produce outputs. I felt limited by what I could do and I somehow felt that the clock frequency was somehow the culprit and I had gotten the idea that in FPGAs calculations were carried out as fast as possible (for that device) so that I would not be limited by the CPU. In a FPGA I thought I could interact with an external device and react to changes in output when it happened.

My first mental model was that you programmed a FPGA by specifying a network (a DAG) of calculations. Whenever inputs changed to the network (from say the world outside the FPGA) the calculations specified by my program would be carried out and the answer would be available at the outputs as soon as possible. The number (and kind) of operations between the input and the output would dictate the time this would take.

While trying to purchase a FPGA development board (not an easy task btw!) I read up and I was sad to understand that in a FPGA all operations were "clocked". That is inputs to the FPGA are only read at fixed intervals. Each such interval is called a clock cycle and on a 25 mhz fpga each clock cycle is 40 nanoseconds long. That felt fast enough to process my inputs if they were directed to the output directly, but what about my calculations? If each logical element needed to wait until the next clock before it fed its value "forward" in the FPGA the output would come much too late.

As I got my development board I realized that both of these two worlds very more or less correct and co-exist. The calculations carried out in the FPGA can be either sequential (clocked) or combinational (not-clocked).


Our mental model of the FPGA
============================
First thing first. Let's start with something that actually is true and then as we go into details, we also avoid some details! The FPGA has a number of physical _pins_ that can be configured to be inputs, outputs or both. How the pins are configured is part of the programming of the FPGA. On the outside of the FPGA the pins can be connected to pretty much anything that operates at the correct voltage (which is seldom above 3.3V for current FPGAs). On the inside the input pins affect the computations performed by the FPGA and the outputs pins are fed results from the computations. What computations are performed is decided by the bitstream that the FPGA is programmed with. The bitstream is constructed through proprietary toolchains supplied by the FPGA manufacturer. The computational elements (called logical elements) of the FPGA are also configured using the bitstream. How they actually behave depends on exact FPGA model, but today we will work on a higher level where we only need a mental model of how it all fits together. 

We think not of individual logical elements but rather of groups of them. There are two types of groups that can be connected together. The first type is called _combinational_ and the second type is _sequential_.

Combinational computations
--------------------------
Yes, I made a header for this section just so I could have a header with an alliteration in it.

Combinational computations does not depend on state. Given an arbitrary number of input signals simple computations are performed. Using simple building blocks (such as NAND, NXOR etc) more advanced computations like addition can be performed. From a high-level perspective we can assume that the computations happens at the speed of light, but in reality there is a short propagation delay associated with the computations. Different connections have different speed. Special "carry chains" are super fast. It is noteworthy that the speed of these computation is unrelated to the clock frequency that the FPGA is running at.

Let's outline how it can work. When the input signal changes the computation happens. Bit change in the network of logical elements, propagating towards the output. After a _short_ duration each output signal have a stable value. The time that it takes for different output to be stable depends on both the amount of computation taking place to compute that output bit, but also on how it was layout physically on the FPGA. Did some propagate through the faster carry chains? Was the combinational moved around on the FPGA due to being complicated, making some routes longer than others?

What value do we get if we try to access an output value before is is stable? In our mental model we will assume that we will get a random value (0 or 1). In reality I'm not sure what we get, but hopefully we can do what we need without knowing the exact reality here!

Rules to respect in our mental model:

- Arbitrary number of inputs
- Computations are performed, propagating signals within the logical elements
- Each output become stable once all propagation it depends on is done
- Different output bits can be stable at different times
- If someone tries to read an output bit before it is stable the value will be undefined (0 or 1 randomly).

NOTE: The last rule might be overly conservative and might put us in problem. Perhaps it is defined to something that we can depend on, like the last value?

Clocked computations
--------------------
Yes, another alliteration. I'm on fire today!

Let us start with an example. We are making a counter using only combinational logic inside the FPGA. It might sound impossible but we will use a magical device so it is ok. To make a counter we need a current state and then we want to advance it to a next state by adding one. We represent the state state as a N-bit number.

First we take the current counter value as an N-bit input to the FPGA. We need state and since we pretend that we only have combinational logic here we need to keep the state outside of the FPGA. Based on the N-bit input we compute a N-bit output that is the next counter value. It is done using combinational logic and the output will be stable after a short duration of time.
Now it is time to use our magical external device and hook it up to the FPGA. It stores the current state and sends it to the FPGA. It also recieves the next state from the FPGA outputs. It has a button that, when pressed, accepts the next state as the current state. The next state send out from the FPGA will be unstable for a short duration after a button press, but if we press the button slowly the output will be stable and we get a stable new counter state.
How fast can we press the button? For a given FPGA it depends on how long chains of combinational logic we've managed to put together, as well as how they were allocated on the FPGA.

These magical devides actually exists inside the FPGA. More or less. They can only store one bit of information each and there is no button. There is, however, a global clock signal that goes off every now and then at a steady rate.

All together
------------
WARNING! This section is work in progress and does contain grave errors right now!

We are ready to introduce a mental model for an actual FPGA. We have two types of actors. We will denote them M and C for now. 

M1 stores an arbitrary large state. Parts of that state is fed forward to a combinational computation box denoted C1. C1 does some simple combinational calculations to produce a new result. Parts of that result can be fed back to M1 and parts of it can be fed forward to M2.

M1 and M2 accepts their new state based on inputs whenever a clock signal arrives.
C1 and C2 computes their outputs based on the inputs all the time, but their input is only changed whenever a clock signal arrives and M1 and M2 starts to output a new state.

Here is an illustration:

************************************************************
* ----------------------.                                  *
*   inputs              |                                  *
*                       v                                  *
*           .----.    .----.    .----.    .----.           *
*           | M1 +--->| C1 +--->| M2 +--->| C2 +---------> *
*           '----'    '-+--'    '----'    '----'           *
*              ^        |                                  *
*              |        |                                  *
*              '--------'                                  *
************************************************************

Note that this is not related to actual circuitry. This image just represents our mental model on a high level.

Mental Model + Problem = Solution?
==================================


Bonus
=====

Clock frequency
---------------
The clock frequency is determined by the maximum propagation delay. The longer chains we have, the lower the clock frequency must be such that all outputs from combinational computations are stable when the next clock goes off. It is possible to incrase the clock frequency by dividing long combinational computations into several steps, saving the intermediate values as clocked state.

Lies, lies, lies...
-------------------
Here I put facts to illustrate where I lied or over-simplified my mental model.

- FPGAs can have multiple clock domains, each with their own clock frequency.
- There are cool ways to sync up clock domains if you have control over both sides (or if the other sides implements something you can adhere to)
- I'm still not sure how combinational results are stored in the FPGA. They must be written backwards somehow.
- FPGA pins are divided into different banks. Some FPGAs can run each bank on a different voltage. This affects what can be connected to them.

by Anders Lindqvist (2015-12-01)

<!-- Markdeep: --><style class="fallback">body{white-space:pre;font-family:monospace}</style><script src="markdeep.min.js"></script><script src="https://casual-effects.com/markdeep/latest/markdeep.min.js"></script>