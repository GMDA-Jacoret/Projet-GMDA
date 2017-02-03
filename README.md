# Random oriented kd-trees and adaptation to intrinsic dimension

## Abstract

## How to run
Program options. Programs should have command-line options properly documents, in order for users to easily pass di↵erent arguments. In python, one can use the package OptionParser, see https://docs.python.org/2/library/optparse.html. In C++, boost program options are highly recommended, see http://www.boost.org/doc/libs/1_62_0/doc/html/program_options.html.

## Output

Output of executions. Ad hoc output are not easily dealt with, unless one knows how to parse the output. Albeit verbose, xml files have two major advantages: (i) the tags allow one to comment on the output, and (ii) xml files are easily parsed with XML query language.

## Experiments

Experiments. If you run several experiments, for example by varying one (or several) parameter(s), as requested in several projects, it is highly recommended to use a batch manager (BM). From a simple text file listing the options and their values, a batch manager handles all executions, by passing the relevant options on the command line.
You can for example use the BL from the Structural Bioinformatics Library, see http://sbl.inria. fr/doc/Batch_manager-user-manual.html.
In passing, if you have serialized your data structures, you can easily compute statistics using PALSE, see http://sbl.inria.fr/doc/PALSE-user-manual.html.
