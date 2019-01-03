# entroPy

Tool to add randomness to values.

Values can be passed either on the command line, or from a file or stdin for convenience.

Attempts to respect the formatting of input values and mirror it on the output; integers should be returned as integers, floats as floats, and numbers with commas and decimals should be returned as such. Note that this is not perfect, if in doubt pre-parse your data to remove thousands separators (e.g. '1,000' -> '1000').

Examples:

```
# pass individual values
$ ./entro.py -v 1 12000.1 1,000,000.1 1000000.1 9000.1 9,000.1 --deg 0.5
1
10535.8
814,481
1.20718e+06
5744.5
12,247

# read the second column from a .csv file with header
$ ./entro.py -i data/data1.csv --header -d , -f 2
"2,402,958"
"1,962,653"
"1,940,965"
"612,368"
"1,917,236"
"2,022,920"
"2,037,701"
"2,126,468"
"2,107,586"
"2,050,470"
"78,355"
"2,021,788"
"1,867,169"
"2,017,480"
"1,840,679"
"1,989,053"
"1,712,943"
"1,651,422"

# read the third column of a .csv file without header
$ ./entro.py -i data/data2.csv -d , -f 3
83
87.6
67.3
79
73
68.9
83.7
69.9
68.4
76.6
10
80.4
75.3
82.8
70.8
67.4
66
79.9

# read from stdin
$ printf '12827.5\n1,875,977\n1.5' | ./entro.py --deg 0.25
13996.5
2,027,344
1.4

# pipe stdin from a chain of commands
$ head data/data2.csv | cut -d , -f1 | sort -k 1nr | ./entro.py
9
8
8
7
6
4
4
2
2
0

```

# Software

- tested with Python 2.7, should work on 3+
