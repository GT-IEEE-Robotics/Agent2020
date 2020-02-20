#!/usr/bin/env python3
"""
File:          main.py
Author:        Binit Shah
Last Modified: Binit on 2/20
"""

import argparse
from agent.block_stacker_pf import BlockStacker
from agent.utilities import Utilities

def main(bin_config_yaml, system_type):
    agent = BlockStacker(Utilities.parse_bin_config(bin_config_yaml), system_type=system_type)

    while True:
        agent.step()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_configuration_yaml", help="file path to the bin configuration yaml", type=str)
    parser.add_argument('-s',
                        default='sim',
                        const='sim',
                        nargs='?',
                        choices=['sim', 'raspi', 'jetson'],
                        help='the hardware system on which this script is running (default: %(default)s)')
    args = parser.parse_args()
    
    print(args.bin_configuration_yaml, args.s)
    main(args.bin_configuration_yaml, args.s)
