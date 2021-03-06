#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compare a HackerRank testcase result fairly with decimal numbers,
taking into account up to DECIMALS digits (and ignoring the following).
"""

from __future__ import print_function
import sys
import re
import itertools


DECIMALS = 6


def main():
    if len(sys.argv) != 3:
        print("Usage: compare.py file1 file2")
        sys.exit(2)

    try:
        f = open(sys.argv[1], "r")
        g = open(sys.argv[2], "r")

        float_pattern = re.compile(r'(\d+\.\d+)')

        def float_fmt(floats):
            def fmt(m):
                floats.append(float(m.group(0)))
                return "FLOAT"
            return fmt

        n = 0
        for i, j in itertools.zip_longest(f, g, fillvalue=''):
            n += 1

            # ignore line endings
            i = i.rstrip()
            j = j.rstrip()

            if len(i) > 500 or len(j) > 500:
                # line is too long, do not test floats
                # ... hard to find the ideal comparison that works everywhere ...
                floats_are_equal = True
                i_new = i
                j_new = j
            else:
                # when a float number is found, adjust decimal digits
                i_floats, j_floats = [], []
                i_new = float_pattern.sub(float_fmt(i_floats), i)
                j_new = float_pattern.sub(float_fmt(j_floats), j)

                floats_are_equal = len(i_floats) == len(j_floats)
                if floats_are_equal:
                    for a, b in zip(i_floats, j_floats):
                        if a == b:
                            continue
                        if abs(a - b) / abs(a + b) > 10 ** -DECIMALS:
                            floats_are_equal = False
                            break

            if i_new != j_new or not floats_are_equal:
                # a difference is found
                print('{}< {}'.format(n, i))
                print('{}> {}'.format(n, j))
                sys.exit(1)

        # everything's fine!
        sys.exit(0)

    except Exception as f:
        print(f, file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
