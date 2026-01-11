beta-str
========

Reimplementation of the Beta string rewriting engine originally written by Benny Brodda in Fortran and later on reimplemented by Kimmo Koskenniemi in Pascal and in C.

The input formalism follows the C version as documented in F. Karlsson and K. Koskenniemi, "Beta-ohjelma kielentutkimuksen apuvälineenä", Yliopistopaino, 1990. An English version of that manual is available here as a manual [BETA: Tool for a linguist](https://github.com/koskenni/beta/blob/master/betaref.md) (which is the file *betaref.md* in this project).

This program was written from scratch in Python3 without any reference to the above mentioned predecessors.

This program is free software under the GPL 3 license. 

Instructions for installing the beta.py program can be found in the [Beta wiki](https://github.com/koskenni/beta/wiki/faq) and in particular, on the page [install](https://github.com/koskenni/beta/wiki/install).

The program depends on a package "datrie" which must be installed on your system, see the Beta wiki for [detailed instructions](https://github.com/koskenni/beta/wiki/faq). **Note:** Version 0.7.1 of datrie has been tested to work.  The latest version 0.8 (2019-07-03) might cause troubles, if you meet such, see the Beta wiki mentioned above.

The beta program runs at least on Gnu/Linux, Unix, Mac OS X and WIndows 7 platforms providing that an appropriate Python 3 (version 3.5 or higher) is installed.

- **Version 0.1** - 2017-04-26: Initial release
- ...
- **Version 0.5.3** - 2019-07-16: Non-ascii punctuation and some special characters (e.g. §) can now be used in rules.  
