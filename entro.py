#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add 'entropy' to values in a file
"""
import os
import sys
import csv
import random
import locale
import argparse

if sys.version < '3':
    integer_types = (int, long,)
else:
    integer_types = (int,)
# check if number is int or float
# isinstance(yourNumber, integer_types)  # returns True if it's an integer
# isinstance(yourNumber, float)  # returns True if it's a float

# allow break in piped stdin/stdout
# https://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

locale.setlocale(locale.LC_ALL, '')

def entropize(n, deg = 0.1):
    """
    Adds entropy to a value by randomly increasing or decreasing it by a degree (`deg`)

    Parameters
    ----------
    n: int/float
        value to be randomized
    deg: float
        percentage range of `n` to set the amount of randomness

    Returns
    -------
    float
    """
    upper = abs(n * deg)
    lower = -1 * upper
    offset = random.uniform(lower, upper)
    res = n + offset
    return(res)

class EntropyValue(object):
    """
    from test import EntropyValue; EntropyValue(n = '1,000.2')
    """
    def __init__(self, n, deg = 0.1):
        self.deg = deg
        self.input_str = n
        self.input_val = self.santize_input(n = self.input_str)
        self.output_val = entropize(n = self.input_val, deg = self.deg)
        self.is_int = isinstance(self.input_val, integer_types)

        if self.is_int:
            # if int was passed, output int
            self.output_val = int(self.output_val)
        else:
            # assume float; round to the same number of decimal places as the input
            self.output_val = round(self.output_val, len(locale.str(self.input_val).split(locale.localeconv().get('decimal_point'))[1]))

        # check if the input value had thousands groupings
        self.has_groupings = locale.localeconv().get('thousands_sep') in self.input_str


    def santize_input(self, n):
        """
        Return a number object represented by input string

        Parameters
        ----------
        n: str
            a string representing a float or int value

        Returns
        -------
        int/float
            a float or int value of the input string
        """
        n2 = n.replace('\xc2\xa0', ' ')
        n2 = n2.strip()
        res = locale.atof(n2) if locale.localeconv().get('decimal_point') in n2 else locale.atoi(n2)
        return(res)

    def __str__(self):
        if self.has_groupings:
            # output_str = locale.format("%g", self.output_val, grouping = True)
            output_str = "{:n}".format(self.output_val)
        else:
            output_str = locale.format("%g", self.output_val)
        return(output_str)



def process_file(fin, fout, delimiter, field):
    """
    """
    cut_field = field - 1
    reader = csv.reader(fin, delimiter = delimiter)
    writer = csv.writer(fout, delimiter = delimiter)
    for row in reader:
        if len(row) > 0:
            val = row[cut_field]
            x = EntropyValue(n = val)
            writer.writerow([str(x)])
            # row[cut_field] = str(x)
            # writer.writerow(row)
            # print row[cut_field]

def process_file_with_headers(fin, fout, delimiter, field):
    """
    """
    # initialize input file as dict
    reader = csv.DictReader(fin, delimiter = delimiter)
    input_fieldnames = reader.fieldnames
    # field in the input file table to process
    cut_field = field - 1
    cut_fieldname = input_fieldnames[cut_field]

    # initialize output file
    # writer = csv.DictWriter(fout, delimiter = delimiter, fieldnames = input_fieldnames)
    # writer.writeheader()
    writer = csv.writer(fout, delimiter = delimiter)
    for row in reader:
        val = row[cut_fieldname]
        x = EntropyValue(n = val)
        writer.writerow([str(x)])
        # writer.writerow(row)

def main(**kwargs):
    print(kwargs)
    input_file = kwargs.pop('input_file', None)
    output_file = kwargs.pop('output_file', None)
    vals = kwargs.pop('vals', None)
    field = kwargs.pop('field', 1)
    delimiter = kwargs.pop('delimiter', '\t')
    has_header = kwargs.pop('has_header', False)

    # if vals were passed, only process those ignore input/output files
    if vals and len(vals) > 0:
        for val in vals:
            x = EntropyValue(n = val)
            print(val, str(x))
        return()

    if input_file:
        fin = open(input_file)
    else:
        fin = sys.stdin

    if output_file:
        fout = open(output_file, "w")
    else:
        fout = sys.stdout

    if has_header:
        process_file_with_headers(fin, fout, delimiter, field)
    else:
        process_file(fin, fout, delimiter, field)

    fout.close()
    fin.close()

def parse():
    """
    Parses script args
    """
    parser = argparse.ArgumentParser(description='Add entropy to values')
    parser.add_argument("-i", default = None, dest = 'input_file', help="Input file")
    parser.add_argument("-o", default = None, dest = 'output_file', help="Output file")
    parser.add_argument('-v', '--vals', dest = 'vals', nargs='*', help="Values to randomize")
    parser.add_argument('-f', dest = 'field', type = int, default = 1, help="Field in input file to randomize")
    parser.add_argument("-d", default = '\t', dest = 'delimiter', help="Delimiter for input and output file")
    parser.add_argument("--header", action='store_true', dest = 'has_header', help="Whether input file has headers")
    args = parser.parse_args()
    main(**vars(args))

if __name__ == '__main__':
    parse()
