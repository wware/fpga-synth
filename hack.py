# Let's simulate the more conventional delta-sigma design and see if it works better than mine.
# It makes a lot of sense to do this using MyHDL.
# See http://www.beis.de/Elektronik/DeltaSigma/DeltaSigma.html

import unittest
import sys
import math
from myhdl import Signal, delay, Simulation, always_comb, \
    instance, intbv, bin, toVerilog, toVHDL, always, now, traceSignals
from config import signed_bus, unsigned_bus, signed_to_unsigned, clip_signed


NBITS = 24
FFF = (1 << NBITS) - 1
SIGN_BIT = 1 << (NBITS - 1)

SINE_TABLE_SIZE = 4096
SINE_TABLE_MAX = int(0.03 * SIGN_BIT)
sine_values = []
for i in range(SINE_TABLE_SIZE):
    phase = 2 * math.pi * i / SINE_TABLE_SIZE
    sine_values.append(int(round(SINE_TABLE_MAX * math.sin(phase))))

# ramp wave
sine_values = []
for i in range(SINE_TABLE_SIZE):
    phase = -1. + 2. * i / SINE_TABLE_SIZE
    sine_values.append(int(round(SINE_TABLE_MAX * phase)))

FREQ_RATIO = 1000
ITERATIONS = 5000

# This is -dt/RC for the fast frequency
alpha = math.exp(-0.01)   # a number close to 1
beta = 1 - alpha          # a number close to 0


def dsig(clk, _input, dac_bit):

    y = signed_bus(NBITS + 10)
    q = signed_bus(NBITS)
    dac_bit_internal = Signal(False)

    PUSH = FFF

    @always_comb
    def drive_bits():
        if dac_bit_internal:
            y.next = (q << 8) + 3 * (PUSH - q)
        else:
            y.next = (q << 8) - 3 * (PUSH + q)

    @always(clk.posedge)
    def clock_tick():
        q.next = y >> 8
        # if _input > q:
        if _input > (y >> 8):
            dac_bit_internal.next = 1
            dac_bit.next = 1
        else:
            dac_bit_internal.next = 0
            dac_bit.next = 0

    return (drive_bits, clock_tick)


def simulate():
    clk = Signal(False)
    _input = signed_bus(NBITS)
    dac_bit = Signal(False)
    voltage = signed_bus(NBITS)

    ds = dsig(clk, _input, dac_bit)

    @instance
    def drive_stuff():
        vc_estimate = 0.
        clk.next = 0
        _input.next = 0
        for i in range(ITERATIONS):
            if (i % (ITERATIONS / 100)) == 0:
                sys.stderr.write('.') 
            yield delay(1)
            clk.next = 0
            yield delay(1)
            clk.next = 1
            phase = int(SINE_TABLE_SIZE * i / FREQ_RATIO) % SINE_TABLE_SIZE
            _input.next = sine_values[phase]
            if dac_bit:
                vc_estimate = alpha * vc_estimate + beta
            else:
                vc_estimate = alpha * vc_estimate
            voltage.next = clip_signed(NBITS, int(round(200 * NBITS * vc_estimate)))
        sys.stderr.write('\n')

    return (ds, drive_stuff)

Simulation(traceSignals(simulate)).run()
