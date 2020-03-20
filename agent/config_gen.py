#!/usr/bin/env python
# File used for generating the YAML configs
# Configured by a permutation of blocks to bins, an initial offset, and an 
#   offset step
# Bins are numbered with one on the bottom-left and ten on the top-right; we 
#   use the convention that an invalid bin is the end
# When using the CoLab notebook to generate the route, make sure to strip off 
#   the first element -- the starting point
# Don't remove the last element as that queues going to the end
# All units are SI -- meters, seconds, ...


# CONFIGURATION: ----------
ROUTE          = [0, 7, 6, 1, 6, 2, 8, 9, 4, 2, 7, 2, 10, 8, 3, 8, 7, 9, 7, 10, 5, 4, 9, 4, 5, 11][1:]
OFFSET_INITIAL = .03
OFFSET_STEP    = .09
OFFSET_END     = 0      # Nothing now; may be useful later

# PREPROCESSING: ----------
place_offs = [OFFSET_INITIAL] * 10


# GENERATION: ----------
print("blocks:")
for b in ROUTE:
    print(f"  - bin: {b}")
    
    # We may get an invalid index for the end
    try:
        # Recall that bins are one indexed
        print(f"    offset: {place_offs[b-1]:.3f}")
        place_offs[b-1] += OFFSET_STEP
    except IndexError:
        print(f"    offset: {OFFSET_END:.3f}")
        break
