beta.py
=======

Reimplementation of the Beta string rewriting engine originally written by Benny Brodda in Fortran and later on reimplemented by Kimmo Koskenniemi in Pascal and in C.

The input formalism follows the C version as documented in F. Karlsson and K. Koskenniemi, "Beta-ohjelma kielentutkimuksen apuvälineenä", Yliopistopaino, 1990.

This program was written from scratch in Python3 without any reference to the above mentioned predecessors.

This program is free software under the GPL 3 license

The program depends on a package "datrie" which can be loaded for global use (if you have the priviliges) by using a command:

    $ python3 -m pip install datrie

which works for Python 3.4 or later, or (again if you have sufficient privliges)

    $ pip3 install datrie

where you have to first install pip by some means specific to your system.

If you are using a server for which you have only normal user priviliges, you might use the following command in order to install datrie in your home directory:

    $ pip3 install --install-option="--prefix=$HOME/.local" datrie

- **Version 0.1** - 2017-04-26: Initial release
- **Version 0.1.1** 2017-04-27: Set identifiers may now contain also "-" and "*", x parts in rules may nou start with a space 
