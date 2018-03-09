beta.py
=======

Reimplementation of the Beta string rewriting engine originally written by Benny Brodda in Fortran and later on reimplemented by Kimmo Koskenniemi in Pascal and in C.

The input formalism follows the C version as documented in F. Karlsson and K. Koskenniemi, "Beta-ohjelma kielentutkimuksen apuvälineenä", Yliopistopaino, 1990. An English version of that manual is available here as a manual [BETA: Tool for a linguist](https://github.com/koskenni/beta/blob/master/betaref.md) (which is the file *betaref.md* in this project).

This program was written from scratch in Python3 without any reference to the above mentioned predecessors.

This program is free software under the GPL 3 license. 

Instructions for installing the beta.py program can be found in the [Beta wiki](https://github.com/koskenni/beta/wiki/faq) and in particular, on the page [install](https://github.com/koskenni/beta/wiki/install).

The program depends on a package "datrie" which must be installed on your system, see the Beta wiki for [detailed instructions](https://github.com/koskenni/beta/wiki/faq).

The beta.py program runs at least on Gnu/Linux, Unix, Mac OS X and WIndows 7 platforms providing that an appropriate Python 3 (version 3.5 or higher) is installed.

- **Version 0.1** - 2017-04-26: Initial release
- **Version 0.1.1** 2017-04-27: Set identifiers may now contain also "-" and "*", x parts in rules may nou start with a space 
- **Version 0.2** 2017-10-17: Now even LIMITOR and BLANK implemented
- **Version 0.3** - 2018-02-07: LIMITOR improved, tracing improved
- **Version 0.3.2** - 2018-02-08: Char and state set names can now include #
- **Version 0.3,3** - 2018-02-09: Validity of ch and st sets is checked; character and state names may now have more symbols in them; parenthesis comments now also for rules without condition or other params
- **Version 0.4** - 2018-02-15: grammar file now as obligatory argument and --input and --output parameters added
- **Version 0.5** - 2018-03-03: mv=1 now moves to between the initial two boundary markers, i.e. `# >>> #xyzabcd##`
- **Version 0.5.1** - 2018-04-09: The punctuation char of LIMITOR now included in the record

