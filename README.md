beta.py
=======

Reimplementation of the Beta string rewriting engine originally written by Benny Brodda in Fortran and later on reimplemented by Kimmo Koskenniemi in Pascal and in C.

The input formalism follows the C version as documented in F. Karlsson and K. Koskenniemi, "Beta-ohjelma kielentutkimuksen apuvälineenä", Yliopistopaino, 1990.

This program was written from scratch in Python3 without any reference to the above mentioned predecessors.

This program is free software under the GPL 3 license

The program depends on a package "datrie" which can be loaded using a command:

    $ python3 -m pip install datrie

which works for Python 3.4 or later, or

    $ pip install datrie

where you have to first install pip by some means specific to your system.

Version 0.1 - 2017-04-26
