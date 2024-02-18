#!/usr/bin/env python3

#https://docs.python.org/3.10/library/argparse.html#action

#learning argparse, goals:
#pass flag argument 
#pass numerical argument to the script
#pass filename to the script
#pass text (for example for specifiying a COM port number or an IP address)


import os
import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numbers", action="store_true", dest="b_number", help="this is description for the -n argument")
    parser.add_argument("-x1", type=int, dest="i_x1", help="this is a single passed number")
    parser.add_argument("integers", type=int, nargs="*", help="those are multiple passed numbers")
    parser.add_argument("-dev", type=ascii, default="COM1")
    args = parser.parse_args(argv)

    b_number: bool = args.b_number
    x1: int = args.i_x1
    inputIntegers = args.integers
    device = args.dev

    print("flag -n = {}".format(b_number))
    print("integer x1 = {}".format(x1))
    print(inputIntegers)
    print("-dev = {}".format(device))

    return 0        

if __name__ == '__main__':
    raise SystemExit(main())
