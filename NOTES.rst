Stuff I've learned
==================

I went to some pains to familiarize myself with the ISE simulator, hoping that it would more
accurately reflect the behavior of the FPGA than MyHDL's simulations. That meant shrinking
all my datapaths to make sure none exceeded 32 bits, and I didn't get any better simulation
accuracy. So I'm giving up on the ISE simulator, and I'll probably widen my datapaths again.

There is one disadvantage to MyHDL as a simulator, because it's running Python, which is that
it's slow. It's generally fine for unit tests but long simulation runs are better done by
producing Verilog and then simulating with iverilog.
