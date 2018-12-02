An FPGA-based synthesizer
=========================

Back in the 1970s and 80s, I was interested in electronics and music synthesizers, and they were
still a pretty big novelty. By that time, Bob Moog had already identified a collection of analog
modules that could be set up like this to produce a very wide range of interesting, obviously
synthetic musical noises.

.. image:: http://www.headphone-amplifier.com/pro_light_sound_2008/images/pro_light_and%20_sound_2008_making_musik_analog_synthesizer1_600.jpg

So a friend and I used to play with this stuff because his father had gotten him started with it,
and then he'd gotten me interested (actually I guess my first impetus was the vinyl album "Switched
On Bach"), and I knew some electronics so that was a welcome addition to his pool of knowledge on
the subject. We had a good time and I built a few electronic musical instruments in college and
immediately after, but then got too busy with my career to pursue it more.

Fast-forward thirty years, and we have cheap 8- and 32-bit microcontrollers and powerful FPGAs. In
my career as an electrical engineer I'd done some FPGA work, and it has occurred to me that the
kinds of fixed-point arithmetic computations that FPGAs do well are the ones that would do the jobs
of all those analog modules. So my hope/plan is to use a Papilio One or Papilio Pro FPGA board to
make a synthesizer with very few analog parts.

Getting back into this stuff after 15 years as a software engineer, there has been a bit of a learning
curve. I don't have the resources of a large corporation supporting the FPGA development effort, I
just have what I find online and can purchase mail-order. Sometimes the simulation acts one way and
the chip acts another, so there's a good bit of floundering involved. Some of the early commits in
this repo will be of stuff that just barely works or doesn't work at all, but that's why they call
it a hobby.

Hacking MyHDL
=============

Installation on Ubuntu 10.04 (Lucid)
------------------------------------

::

 sudo add-apt-repository ppa:balau82/ppa
 sudo apt-get update
 sudo apt-get install myhdl gtkwave verilog

Making sure it works::

 (cd /usr/share/doc/myhdl/examples/rs232; python test_rs232.py)

Online manual:

* http://www.myhdl.org/doc/0.6/manual/index.html

Projects:

* http://www.myhdl.org/doku.php/projects:intro
* http://www.antfarm.org/blog/aaronf/2008/02/myhdl_a_brief_discussion_2.html
* /usr/share/doc/myhdl/examples

Installation on OSX 10.8.3 (Mountain Lion)
------------------------------------------

Download MyHDL from this website: http://sourceforge.net/projects/myhdl

Then::

 tar xfz Downloads/myhdl-0.7.tar.gz
 cd myhdl-0.7
 python setup.py build
 sudo python setup.py install

Unpack the GTKWave zip in the /Applications directory: http://gtkwave.sourceforge.net/gtkwave.zip

Add this to your .bash_profile::

 export PATH=$PATH:/Applications/gtkwave.app/Contents/Resources/bin

Add this line to your MyHDL source file::

 Simulation(traceSignals(testBench)).run()

This will produce a file called testBench.vcd, and now you just type::

 gtkwave testBench.vcd

Open up the device under test in the upper left, select signals you want to look at, and drag them
over to the waveform display. Right-click on the signal name to choose a data format, including
analog formats that show waveforms.

The MyBlaze core
----------------

MyBlaze is a MyHDL implementation (LGPL) of the GCC-targetable MicroBlaze soft
processor core which runs on Xilinx FPGAs. Some people have run MMU-less Linux
on it, and it can also run FreeRTOS.

* http://en.wikipedia.org/wiki/MicroBlaze
* https://github.com/wware/myblaze
* http://xilinx.wikidot.com/mb-gnu-tools
* http://xilinx.wikidot.com/microblaze-linux
* Here is a guy in Israel who has done a lot of Microblaze work: http://billauer.co.il/blog/category/fpga/
