#!/usr/bin/env python
# File used for generating the YAML configs
# Configured by a permutation of blocks to bins, an initial offset, and an 
#   offset step
# Bins are numbered with zero on the bottom-left and nine on the top-right; 
#   this is NOT consistent with the CoLab notebook, but the output from it 
#   will still work if you subtract one from each bin in the route and remove
#   the first and last elements.
# All units are SI -- meters, seconds, ...


# CONFIGURATION: ----------
ROUTE          = list(map(lambda x: x-1,
                    [0, 7, 6, 1, 6, 2, 8, 9, 4, 2, 7, 2, 10, 8, 3, 8, 7, 9, 7, 10, 5, 4, 9, 4, 5, 11]
                 [1:-1]))
OFFSET_INITIAL = .02
OFFSET_STEP    = .05


# CONSTANTS: ----------
BIN_XS = [-0.5461, -0.27305, 0.0, 0.27305, 0.5461, -0.5461, -0.27305, 0.0, 0.27305, 0.5461]
BIN_YB = .2667
PI_ARR = list(map(int,
            '31415926535897932384626433832795028841971693993751'+\
            '05820974944592307816406286208998628034825342117067'+\
            '98214808651328230664709384460955058223172535940812' ))

# PREPROCESSING: ----------
place_abs        = [BIN_YB + OFFSET_INITIAL] * 10
place_sign       = [-1]*5 + [1]*5


# GENERATION: ----------
print("blocks:")
for b,d in zip(ROUTE, PI_ARR):
    print(f"  - x: {BIN_XS[b]}")
    print(f"    y: {place_sign[b] * place_abs[b]}")
    print(f"    digit: {d}")
    place_abs[b] += OFFSET_STEP
