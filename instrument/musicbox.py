#!/usr/bin/env python

"""\
MyHDL code for music-box mode of the FPGA synthesizer

Usage:
  PROG [options]

Options:
  -s --sim        run a simulation
  -h --hdl        generate Verilog
  -t --unit-test  run unit tests
"""

import docopt
import sys
from myhdl import *

options = docopt.docopt(__doc__.replace('PROG', sys.argv[0]))


def genclocks(clk, clk40, clk2):
    """
    Given a 32 MHz clock, generate clocks at 40 kHz and 2 Hz.
    """
    counter1 = Signal(intbv(0)[10:])
    counter2 = Signal(intbv(0)[15:])

    @always(clk.posedge)
    def foo():
        if counter1 >= 799:
            clk40.next = 1
            counter1.next = 0
            if counter2 >= 19999:
                counter2.next = 0
                clk2.next = 0
            elif counter2 == 1:
                counter2.next = counter2 + 1
                clk2.next = 1
            else:
                counter2.next = counter2 + 1
                clk2.next = 0
        else:
            counter1.next = counter1 + 1
            clk40.next = 0
            clk2.next = 0

    return foo


# Calculate dphase values for the white piano keys for 3 octaves, not
# including the highest C.
if sys.argv[1:2] == ['calculate']:
    k = (440. * (1<<24) / 40000) / (2 ** 0.75)
    j = 0
    for octave in range(3):
        for i in (0, 2, 4, 5, 7, 9, 11):
            p = 12.0 * octave + i
            count = (2.0 ** (p / 12)) * k
            print j, int(count + 0.5)
            j += 1
    sys.exit(0)


def get_freq(clk, pitch, freq):
    """
    Using dphase values above, map pitch (as an index of the white piano keys)
    to dphase value, from middle C to the C two octaves higher.
    """
    @always(clk.posedge)
    def foo():
        if pitch == 0:
            freq.next = 109734
        elif pitch == 1:
            freq.next = 123172
        elif pitch == 2:
            freq.next = 138256
        elif pitch == 3:
            freq.next = 146477
        elif pitch == 4:
            freq.next = 164415
        elif pitch == 5:
            freq.next = 184549
        elif pitch == 6:
            freq.next = 207150
        elif pitch == 7:
            freq.next = 219467
        elif pitch == 8:
            freq.next = 246344
        elif pitch == 9:
            freq.next = 276512
        elif pitch == 10:
            freq.next = 292954
        elif pitch == 11:
            freq.next = 328830
        elif pitch == 12:
            freq.next = 369099
        elif pitch == 13:
            freq.next = 414299
        elif pitch == 14:
            freq.next = 438935
        else:
            freq.next = 0
    return foo


def voice(clk, clk40, keydn, dphase, _out):
    ampl = Signal(intbv(0)[14:])
    phase = Signal(intbv(0)[24:])
    twave = Signal(intbv(0)[14:])

    @always(clk.posedge)
    def piece1():
        if keydn:
            ampl.next = 16383
        if clk40:
            if ampl > 0:
                ampl.next = ampl - 1
            phase.next = (phase + dphase) & ((1 << 24) - 1)
            if (phase & (1 << 23)) != 0:
                twave.next = ((1 << 24) - 1 - phase) >> 9
            else:
                twave.next = phase >> 9
            # ampl is unsigned, twave is signed. This is how you multiply a
            # signed int by an unsigned int to get a signed result.
            _out.next = ((((1<<14) - 1 - ampl) << 13) + ampl * twave) >> 14

    return piece1


def dacwriter(clk, clk40, dac_data, dacbit, cs_active):
    dac_counter = Signal(intbv(0)[4:])
    dac_data_latched = Signal(intbv(0)[14:])

    @always_comb
    def drive_dacbit():
        if dac_counter < 14:
            dacbit.next = ((dac_data_latched >> (13 - dac_counter)) & 1) != 0
        else:
            dacbit.next = 0

    @always(clk.posedge)
    def count():
        if clk40:
            dac_counter.next = 0
            cs_active.next = 1
            dac_data_latched.next = dac_data
        elif dac_counter < 16:
            if dac_counter == 15:
                cs_active.next = 0
            dac_counter.next = (dac_counter + 1) & 15

    return (count, drive_dacbit)


def tune(clk, clk40, clk2, dphase1, dphase2, dphase3, keydn1, keydn2, keydn3):
    pitch1, pitch2, pitch3 = [Signal(intbv(0)[5:]) for i in range(3)]
    tunestep = Signal(intbv(0)[4:])

    f1 = get_freq(clk, pitch1, dphase1)
    f2 = get_freq(clk, pitch2, dphase2)
    f3 = get_freq(clk, pitch3, dphase3)

    @always(clk.posedge)
    def foo():
        if clk2:
            if tunestep == 0:
                pitch1.next = 0
                keydn1.next = 1
                pitch2.next = 4
                keydn2.next = 1
                pitch3.next = 9
                keydn3.next = 1
            elif tunestep == 1:
                pitch1.next = 2
                keydn1.next = 1
            elif tunestep == 2:
                pitch1.next = 4
                keydn1.next = 1
            elif tunestep == 3:
                pitch1.next = 0
                keydn1.next = 1
                pitch2.next = 5
                keydn2.next = 1
                pitch3.next = 10
                keydn3.next = 1
            elif tunestep == 4:
                pitch1.next = 3
                keydn1.next = 1
            elif tunestep == 5:
                pitch1.next = 5
                keydn1.next = 1
            elif tunestep == 6:
                pitch1.next = 1
                keydn1.next = 1
                pitch2.next = 6
                keydn2.next = 1
                pitch3.next = 11
                keydn3.next = 1
            elif tunestep == 7:
                pitch1.next = 4
                keydn1.next = 1
            elif tunestep == 8:
                pitch1.next = 6
                keydn1.next = 1
            elif tunestep == 9:
                pitch1.next = 7
                keydn1.next = 1
                pitch2.next = 9
                keydn2.next = 1
                pitch3.next = 11
                keydn3.next = 1

            if tunestep < 12:
                tunestep.next = tunestep + 1
            else:
                tunestep.next = 0
        else:
            keydn1.next = 0
            keydn2.next = 0
            keydn3.next = 0

    @always(clk)
    def foo2():
        pitch1.next = 0
        keydn1.next = 1
        pitch2.next = 7
        keydn2.next = 1
        pitch3.next = 16
        keydn3.next = 1

    return (foo, f1, f2, f3)


def fpga(clk, out_a, out_b, out_c, out_d):
    clk40 = Signal(False)
    clk2 = Signal(False)
    cs_active = Signal(False)
    outb_internal = Signal(False)
    _out = Signal(intbv(0)[14:])
    _out1, _out2, _out3 = [Signal(intbv(0)[14:]) for i in range(3)]
    dphase1, dphase2, dphase3 = [Signal(intbv(0)[24:]) for i in range(3)]
    keydn1, keydn2, keydn3 = [Signal(False) for i in range(3)]

    g = genclocks(clk, clk40, clk2)
    dw = dacwriter(clk, clk40, _out, outb_internal, cs_active)
    t = tune(clk, clk40, clk2, dphase1, dphase2, dphase3, keydn1, keydn2, keydn3)

    v1 = voice(clk, clk40, keydn1, dphase1, _out1)
    v2 = voice(clk, clk40, keydn2, dphase2, _out2)
    v3 = voice(clk, clk40, keydn3, dphase3, _out3)

    @always_comb
    def out_acd():
        #_out.next = (_out1 + _out2 + _out3) >> 2
        _out.next = (_out1 >> 2) + (_out2 >> 2) + (_out3 >> 2)
        out_b.next = outb_internal
        out_a.next = 0
        out_c.next = not clk
        out_d.next = not cs_active

    return (g, dw, t, out_acd, v1, v2, v3)


def simulate():
    out_a, out_b, out_c, out_d = [Signal(False) for i in range(4)]
    clk = Signal(False)
    _fpga = fpga(clk, out_a, out_b, out_c, out_d)

    @instance
    def bench():
        clk.next = 0
        for i in range(1000000):
            yield delay(1)
            clk.next = 1
            yield delay(1)
            clk.next = 0

    return (bench, _fpga)


if options['--hdl']:
    out_a, out_b, out_c, out_d = [Signal(False) for i in range(4)]
    clk = Signal(False)
    toVerilog(fpga, clk, out_a, out_b, out_c, out_d)

if options['--sim']:
    Simulation(traceSignals(simulate)).run()

if options['--unit-test']:
    raise Exception('not implemented yet')
