from myhdl import Signal, delay, always_comb, instance, intbv, bin, always, now, toVerilog


######### General stuff ################

# Papilio board clocked at 32 MHz, audio rate is 40 kHz
MHZ = 32 * 1000 * 1000
SECOND = AUDIO_RATE = 40 * 1000

DIVIDER = MHZ / AUDIO_RATE

N = 14
assert N < 18   # keep multiplier happy

WHOLE = 1 << N
MASK = WHOLE - 1
HALF = 1 << (N - 1)
QUARTER = 1 << (N - 2)

PHASEWIDTH = 24

LOADWIDTH = 4

(RAMP, TRIANGLE, SQWAVE, NOISE) = range(4)

def signed_bus(numbits):
    min = -(1 << (numbits - 1))
    max = 1 << (numbits - 1)
    return Signal(intbv(0, min=min, max=max))

def unsigned_bus(numbits):
    return Signal(intbv(0)[numbits:])

def signed_to_unsigned(nbits, _in, _out):
    @always(_in)
    def drive_out():
        _out.next = _in + (1 << (nbits - 1))
    return drive_out

def unsigned_to_signed(nbits, _in, _out):
    @always(_in)
    def drive__out():
        _out.next = _in - (1 << (nbits - 1))
    return drive_out

def clip_signed(nbits, x):
    SIGN_BIT = 1 << (nbits - 1)
    return min(max(x, -SIGN_BIT), SIGN_BIT - 1)


############## Simulation stuff ################

def compute_delta_phase(freq):
    ONE_HERTZ = 1. * (1 << PHASEWIDTH) / AUDIO_RATE
    return int(round(ONE_HERTZ * freq))

R = """
initial begin
    $dumpfile("simulate.vcd");
    $dumpvars;
end

"""

def run_simulation(simulate):
    # Simulation(traceSignals(simulate)).run()
    # let's use iverilog instead, might be faster
    toVerilog(simulate)
    import os
    n = int(os.popen("grep -n initial simulate.v | sed 's/:.*//'").read())
    os.system('head -%d simulate.v > _simulate.v' % (n - 1))
    open('_simulate.v', 'a').write(R)
    os.system('tail +%d simulate.v >> _simulate.v' % n)
    os.system('iverilog _simulate.v')
    os.system('vvp a.out')