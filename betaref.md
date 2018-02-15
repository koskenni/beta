# BETA: Tool for a Linguist

Fred Karlsson, Kimmo Koskenniemi and Arvi Hurskainen

Helsinki 2018

## FOREWORD

Beta system has been designed for the analysis and processing of
linguistic materials. It is a multipurpose tool in that it suits to
phonological, graphemic and morphophonological, and also to limited
syntactic tasks. It is possible to use it for creating and testing
theoretical linguistic models, for rewriting computerized texts, and for
extraction of strings and structures from text corpora. All these tasks
can be performed by using the same basic Beta formalism.

Beta is easy to use. The experience shows that a new user can learn the
use of Beta after having practiced its use for some tens of hours,
preferably guided by an experienced user.

Beta is also efficient. It has been used in the universities of
Stockholm and Helsinki for implementing many kinds of applications on
natural languages. Among these applications are: FINHYP, the hyphenation
algorithm of Finnish (99.99 % precision); FINSTEMS, which produces
search stems for Finnish words; WGEN, which produces all inflected
word-forms of nouns and verbs in Finnish; SWEPARAD, which produces
inflected word-forms of nouns in Swedish; FINTAG, which disambiguates
word tokens and provides running Finnish text with surface syntactic
tags. The automatic hyphenation of several languages available in
Orthografix proofing tools has been programmed in Beta.

The basic version of Beta was first implemented by Benny Brodda in
FORTRAN in 1970s. Kimmo Koskenniemi from Helsinki rewrote it in Pascal
in 1981 and later in C-language. Fred Karlsson has written it in
InterLisp and MuLisp. Earlier implementations were not free and open
source, so Kimmo Koskenniemi re-implemented the Beta program in Python
in 2017 which is available at *https://github.com/koskenni/beta*.

The formalism for Beta rules is practically identical in all
implementations mentioned above. The subsequent discussion describes how
to use the Python Beta. Minor differences between the formalisms
accepted by different implementations may exist though.

To a great part the text of this manual is based on the text written and
published in Finnish by Fred Karlsson and Kimmo Koskenniemi (1990). The
major difference is that while the original authors used examples based
on Finnish, the present English version uses mainly examples from
Swahili.

We express our sincere thanks to Benny Brodda for making Beta available
to us and many other users of this magnificent tool.

Helsinki, February 2018

Fred Karlsson, Kimmo Koskenniemi, Arvi Hurskainen

## 1. INTRODUCTION

Beta is a computer formalism based on string substitutions and a state
mechanism. Beta can be used for performing important tasks in
linguistic research, such as:

1. To design theoretical models of phonological, morpho(phono)logical,
lexical and partly syntactic phenomena for analyzing words or sentences
or generating word tokens.

2. To extract and exclude patterns and structures from text corpora,
lexicons etc.

3. To convert and modify computer-readable linguistic materials.

The user of Beta does not need himself to know the internal structure of
the program in any detail. The linguist writes rules according to the
Beta rule formalism which is easy to learn. The Beta program first reads
in the rules and then performs the transformations to the input data as
defined by the rules.

Beta rule grammars may be written to perform various kinds of tasks,
including data conversion, extracting interesting examples out of text
data, modelling morphological structures or processes and selecting
correct readings of ambiguous word tokens and parsing surface
syntactic structures of sentences. Thus, the Beta program can be used
both for tasks for generating and for analyzing linguistic
expressions.

By substitution we mean that in a string W = X Y Z, which has a
substring Y, that substring is substituted by another string Q. After
the replacement, we get a new string X Q Z, which again may be made
subject to other substitutions. Beta rules do exactly this kind of
substitutions. Sometimes we wish to partition the rules so that not all
of them are available for all substitutions. For this purpose, Beta has
a state mechanism. By entering and testing states as is described in
this document. Beta grammars are often designed to consist of phases
which follow each other in a controlled manner.

Beta takes as input strings of varying lengths, either directly from
keyboard, such as individual words or sentences, or from a file, such
as text corpora of various sizes, up to hundreds of thousands of
words.  Certain definitions tell the program, how large records it is
supposed to process at a time. These records may be individual words,
lines of words, clauses, or sentences (as defined by punctuation
characters). The Beta program continues to transform each input record
as long as any of the rules apply. When no further rules can be
applied, the process is finished and the resulting string is output.

The output may be directed to the screen, or to a file, in which case it
can be processed further according to need. In Unix or Gnu/Linux
environments, the user can combine programs into so called pipelines. A
Beta program is often an element in such a sequence of programs, each of
which performs a specific part of a larger task. On other platforms,
Beta can be used so that the output goes to a file and is subsequently
processed by other programs.

When the Beta program is executed, a Beta grammar must be given to it.
Input to the program may be given either from the terminal or taken
from a file. Output may either appear on the terminal or it may be
directed into a file. If the user has problems in giving
the names of the rule grammar files and input files required by
Python Beta, one can ask it for help:

    $ beta.py --help

By default, input units are word tokens separated by blank space. If
several word tokens appear on a line, each is processed separately. It
is also possible to define the file, to which the results are directed.
The definitions in the Beta grammar regulate the size of the input
records (words, lines, sentences).

The Python Beta operates upon strings of characters. What it exactly
means needs some clarification. A string is a set of consecutive
characters, containing zero, one, or more characters. When using the
Python Beta, one may use any Unicode UTF-8 letters and symbols in the
Latin alphabets (see the Appendix for an explicit list of allowed
characters). Older, eight-bit characters, such as Latin-1 or Latin-9,
cannot be used with Python Beta. Files using such coding can easily be
converted into Unicode UTF-8 coding, (see the Appendix for the
practical conversion). The characters which may be used in the
definitions, rules and in the data, include:

1. Alphabetical characters i.e. letters. Upper-case and lower-case
letters are distinct. Letters with various diacritic marks (á, è, ô,
ï) or variants of more common letters (ð, þ, æ) are also allowed.

2. Digits: 0 1 2 3 4 5 6 7 8 9

3. All the punctuation marks and special characters, which are found on
the keyboard:
```
    . , ! ? : ; ( ) < > ' ` " & % / = - _ + # $ * @
    [ \ ] { | } ^ ~
```
4. Some invisible marks (white space), such as blank ( ), tab mark
(tab), and a newline.

When processing normal text, one must be aware of the problems caused by
these marks and characters. If one wants, for example, to extract all
instances of a pattern, one must take account also of all such cases,
where the search string is surrounded by one or two punctuation marks or
special characters, such as:

    car, car. car! car? car: car; 'car' "car" (car)

Word tokens may be identified by using suitable Beta rules and
definitions. Particularly important characters in defining contexts are
the character (\#), which is used to mark the beginning and end of the
logical record, and the space ( ), which is located on both sides of
the word tokens of the running text.

The substring means the string of consecutive characters, which are part
of a longer string. For example, in a string ABCD, substrings are AB,
BC, ABC, BCD and CD, but not AC, ACD or BD.

In the following discussion on Beta, it is assumed that the user has
access to such an operating system, where commands are given on a
command line (e.g. DOS, Linux, Unix, Mac iOS). The user should also be
acquainted with a program editor operating in ASCII or UTF-8 format
(e.g. Emacs, Epsilon). If one wants to use a text editor, such as
Microsoft Office Word, in writing Beta grammars, one must make sure
that the files will be saved in a 'Text Only' (or 'Plain Text')
format. Otherwise the hidden codes in the file will cause
unpredictable and usually wrong results.

## 2. THE STRUCTURE OF BETA GRAMMARS

### 2.1. Components of a Beta grammar

Beta grammars must be written with a suitable program editor into a
file containing the definitions and the rules. Among such suitable
editors are those of the Emacs family, such as Gnu Emacs, MicroEmacs
and Epsilon. Also, such text editors can be used if they enable
reading and saving the file in 'Text Only' Unicode UTF-8 coding.

Beta grammar files are given names according to the conventions of the
operating system (Linux, Unix, Mac iOS, Windows). Beta grammar files
are often given names with a suffix '.bta' or '.beta'. Examples of
suitable rule file names are:

    EXTR.BTA
    kwic.bta

In Linux and Unix, upper and lower-case letters are different characters
in file names.

The Beta rule grammar has three sections:

    CHARACTER-SETS
    ... definitions of character sets ...
    STATE-SETS
    ... definitions of state sets ...
    RULES
    ... rewriting rules ...

The RULES section must be present in every grammar file. Either of the
first two sections or both, may be empty (and then one may also omit the
keyword, e.g. STATE-SETS).

### 2.2. Comment lines

Beta grammar files may contain any amount of comment lines, which do
not affect the function of the rules in any way. They document the
purpose of the whole Beta grammar or its phases or individual sets and
rules. Each comment line starts with an exclamation mark (!). Note
that the exclamation mark must be the very first character on the line
(not even a blank may precede it). It is up to the author of the Beta
grammar file to define where to put the comments and how many to
write. It is advisable at least to write the name of the grammar file,
to describe its task, and also the name of the author and time of
writing, and the dates of modifications and additions. There may be
several consecutive comment lines:

    ! NOUNS.BTA A. Hurskainen 15.4. 1992
    ! These rules extract the noun entries in
    ! *Kamusi ya Kiswahili Sanifu* and list them
    ! in the order they appear in the dictionary.

Comment lines are particularly useful in the RULES section, which may
contain hundreds, and even thousands, of rules. It is also important
to structure the Beta grammar so that the designer, and possibly also
others, may afterwards be able to read what the rule grammar is
designed to do. Rules belonging together may be grouped under one set
of comment lines, which function as an instruction to the subsequent
rules. More about the formalism in section 3.

### 2.3. CHARACTER SETS

In the section CHARACTER-SETS, there are definitions for the possible
conditions for segmental contexts. These definitions are given as sets
of characters. Each character set must have a name, followed by a colon
(:), and after it are given the concrete characters belonging to this
set. The names of the character sets may have any form; they may consist
of letters, numbers, and certain special characters. They may not
include an empty space. All other marks and characters may be written as
they are except the empty space, which is also used as a separator
between characters. If an empty space is included into a character set,
it can be done by writing the string BLANK.

    CHARACTER-SETS
     #: #
     Punc: . : ; ! ?
     Con: p t k d s h v j l m n
     Vo: a e i o u
     Ck: p t k
     Vbk: u o a
     Sep: BLANK

The name of the first context set is (\#), and it includes only one
character (\#), which is the delimiter between input records. Punc
includes punctuation marks, which normally end sentences. Con has some
consonants, and Vo contains five vowels etc. The sets may contain
natural and non-natural sets. It is up to the user to define what kinds
of sets are needed. The above examples contain only lower-case letters.
If the material to be processed has also upper-case letters, they also
must be included into the character sets.

It is possible to treat also the newline and tab characters with Beta
rules. There are no newline marks in the input text, but it is possible
to produce them by means of rewriting rules. For this purpose, the
percent character (%) has been reserved, and the exceptional
characters are produced as combinations of two characters:

- `%n` newline

- `%t` tab

- `%;` semicolon (in rules)

- `%!` exclamation mark (in the first column)

- `%%` percent mark

These combinations of two characters must be used in rules as well as in
character set definitions, e.g.:

    Spec: ! %% / ( ) ? ; : * ' " ^ ~ &
    Sep: BLANK %n %t #

### 2.4. State sets

When operating, Beta rules utilize also the so-called state mechanism. A
state can be any positive integer (of reasonable size). State sets
appear in the rules as conditions for the application of rules, so that
the application of a rule is possible only, if the process is at that
moment in a state, which belongs to the state set defined in the rule.
In other respects, the state sets are formally quite similar with
character sets, e.g.:

    STATE-SETS
    Start: 1
    Begin: 1 2
    5: 5
    Sx: 1 2 3 4 5 6
    W: 7
    567: 5 6 7
    6,10: 6 10

In the above example, the state set Start has only the state 1. The
state set Begin has two states, 1 and 2. State set 5 has only the state
5, while the state set Sx has the states 1 to 6. The state set '567'
has the states 5, 6 and 7, while the state set '6,10' has the states 6
and 10. Character sets and state sets may have also identical names.
They will not get mixed, because they are referred to in different
places in the rules.

One may separate individual characters or state numbers with one or
more spaces in the definitions of character sets and state sets. The
lines may be as long as needed to include all members in the sets. Tab
character should, however, be avoided. The colon (:) after the set
name is important, because it indicates the border between the set
name (on the left) and the members belonging to the set (on the
right). Empty lines are permitted at various parts of the Beta grammar
file and they are ignored.

### 2.5. RULES

RULES is normally the largest section of the Beta grammar file. The rules
are substitution rules, and their context conditions are defined in the
section CHARACTER-SETS, and the state conditions are defined in the
section STATE-SETS. The set of rules is based on the carefully
designed cooperation of character sets and state sets.

In the following is given an example of a small grammar file, which
transforms the vowel u into w between the consonant m and a vowel.

    ! demou-w.bta ( u > w between 'm' and a vowel)
    ! A. Hurskainen 15.4. 1992
    CHARACTER-SETS
    Vo: a e i o u
    M: M m
    STATE-SETS
    Start: 1
    RULES
    !               lc rc   sc rs mv md
    u; w;            M Vo Start 0  5  1

The input record is a word, that is, a string of characters separated by
empty spaces (or newline) by default. This means that if there are
several such words on a line, each word is processed separately and the
result of each is printed on a line of its own. The rule looks for
possible occurrences of u and rewrites the u as a w, if the context
conditions M and Vo are met.

Before explaining the structure of individual rules and the function of
the program in more detail, we will take a concrete example and
experiment with it by using a computer. Assuming that the above grammar
file demou-w.bta has been saved in the current directory (the directory
where we are currently operating), we may execute the program by writing
on the command line (again assuming that the beta.py program has been
installed properly):

    $ beta.py demou-w.bta

After being called the program reads in the grammar file, interprets
the rules and then waits for input. Let us input a word to be
processed:

    mualimu

After this, examples to be analyzed may be given one by one from the
keyboard, one word per line. The program responds by producing the
transformed string, e.g.:

    mwalimu

This is how the Beta program typically works: a string in and another
out. If we are interested in finding out through which steps the process
goes, we may ask the program to show more of the intermediate steps in
the process. This facility is useful in tracing the interplay of the
rules, and it helps in spotting weaknesses and bugs in rules. A way to
ask for this kind of tracing is to include a parameter -v 1 or -v 2 on
the command which starts the Beta program. We can then see the
intermediate steps as follows. The first line is the command starting
Beta, the second line is the word we typed as input to the rules. The
last line is the output string the program produces, and the lines
before that contain the tracing information.

    $ beta.py demou-w.bta -v 2
    mualimu
    ## >>> mualimu ## -- 1
    ##m >>> ualimu ## -- 1
    u;w; M Vo Start 0 5 1
    ##mw >>> alimu## -- 1
    ##mwa >>> limu## -- 1
    ##mwal >>> imu## -- 1
    ##mwali >>> mu## -- 1
    ##mwalim >>> u## -- 1
    ##mwalimu >>> ## -- 1
    ##mwalimu# >>> # -- 1
    mwalimu

Here the `>>>` marks the points where the Beta processor is. It
starts from the beginning, i.e. just after the boundary marker `##`
and looks for a rule to be applied there. There is none, so it proceeds
one character to the right. Now it is looking at the 'u' and finds a
rule to apply, and removes the 'u' and replaces it with a 'w'. It
continues at the point after the replacement. No further rules are found
as the processor goes to the right one character at a time. When it
reaches the end marker `##`, the string is complete and is printed.

Usually we are not that curious to see all those steps where no rules
are applied. Then we use a weaker trace, '-v 1':

    $ beta.py demou-w.bta -v 1
    mualimu
    u;w; M Vo Start 0 5 1
    ##mw >>> alimu ## -- 1
    mwalimu

This (weaker) trace facility can also be activated during an interactive
session by entering a line consisting of `##`. The program then
responds by Trace now ON. Trace may be turned off by giving the same
command again.

    ##
    Trace Now ON

If we enter the string *muanamuali*, we get the following traced output:

    muanamuali
    u;w; M Vo Start 0 5 1
    ##mw >>> anamuali## -- 1
    u;w; M Vo Start 0 5 1
    ##mwanamw >>> ali## -- 1
    mwanamwali

We see that the same rule has applied two times, because there are two
occurrences with proper contexts in the same string, where the context
conditions are met.

On Linux, Unix and Mac iOS platforms, you can exit the Beta program by
the entering a Control-D (= press Ctrl-key first and then D-key without
releasing the Ctrl key). In Windows and MS-DOS operating system, one
enters a Control-Z in order to signal the end of input and exit the Beta
program.

## 3. THE STRUCTURE OF THE BETA RULE

### 3.1. The basic components of a Beta rule

The principle of the substitution grammar is well known from the theory
of formal languages. Thue, Post and Turing, for example, developed this
theory. The rewrite rules of the generative grammar are of the same
general type:

    X -> Y / LC _ RC

This means, rewrite X as Y in the context, where the context conditions
(LC=left context, RC=right context) are fulfilled. X and Y are the
substitution part of the rule, and LC and RC are its segmental context
conditions. Both context are just single characters immediately before
or respectively after the X part. Rules of this type are generally used
in describing syntactical, morpho(phono)logical and phonological
phenomena. The Beta rule contains corresponding rule parameters X, Y, LC
and RC, and some additional parameters, such as the state mechanism.
Each context condition is simply a name of a character set as defined in
the beginning of the rule grammar. The test is the character in the
context that belongs to the set named in LC or respectively in RC. Rules
need not have explicit context condition. Either one or both can be just
a zero (0) which means that the corresponding test is not made (i.e. it
always succeeds).

State is a mechanism for the rule processor to remember something. The
rule processor is always in a certain state, and when applying, Beta
rules can move the processor into another state as a side effect. Each
rule defines whether there is a move to another state after the
application of that rule or not. The current state of the Beta
processor has one important use: individual Beta rules can be
activated or inactivated through their state condition, which tests
whether the current state of the processor is among the set of allowed
states for that rule.

The state mechanism is controlled by two rule parameters in the Beta
rules: SC (state condition), and RS (resulting state). The state-sets
were introduced above, and the state condition is usually just the name
of a state-set, and the test effectively checks whether the processor's
current state belongs to that set. Keep in mind that SC refers to a *set
of states*, the RS always refers to a *single state*. Rules need neither
change nor test the state of the processor. A state condition zero (0)
means that no test is needed and a resulting state (0) means that the
processor will remain in the same state.

The seventh parameter of a Beta rule, MV (move), moves the dot (also
called control or cursor) to a point where the analysis continues.
Normally the process is directed to continue immediately after the
substitution part Y, but sometimes there is a need to return backwards
to a certain point, or further to the right. This is defined by giving
the appropriate numeric parameter (see below 3.2.5). 

The eighth and last parameter (MD) allows non-deterministic application
of rules. Normally rules are applied deterministically, so that if they
can be applied then they will be applied, and the option of not applying
is not considered at all. This is the deterministic mode of application.
With the help of the MD-parameter it is possible to make the rule to
apply in a non-deterministic way, whereby Beta processes both
alternatives in parallel. The first alternative is that the rule is
applied immediately without considering other alternatives. The second
alternative is that this rule will be left unapplied so that the
applicability of other rules may be tested. Non-deterministic rules are
needed in describing free variation, for instance. In such cases more
than one rule may apply to the same basic string.

The full Beta rule has eight rule parameters, which form three groups
(see the graph below): (1) defines the substitution (1-3), (2) defines
the conditions for substitution (4-5), and (3) directs further
processing (7-8).

(1)      |   (2)   |  (3)  |   (4)  |  (5)  |  (6)   | (7)  |  (8)
---------|---------|-------|-------|-------|--------|------|-------
text to be sub- stituted | result of sub- stitution | left con- text | right con- text |  state cond. | result state | move | mode of appl.
X    |   Y   |  LC   |   RC   |   SC  |  RS   |   MV   | MD

Each rule has the eight parameter values, either as given or indirectly
by default. A full Beta rule with all parameter values looks as follows:

    ki; ch;          Blank    Vo    Affr    2       5      1

According to the rule, the string ki (X) is rewritten as ch (Y), if
there is a character belonging to the character set Blank on the left
side (LC), and a character belonging to the character set Vo (RC) on the
right side, and also assuming that the program is in the state belonging
to the state set Affr (SC). The substitution is performed only if all
the three conditions are met. If any of the conditions is not met, the
rule does not apply.

If all three conditions (LC, RC and SC) are met, the substitution is
executed and the control moves to the state 2 (RS). The further analysis
is continued immediately after the substitution part (MV=5), and the
rule is applied in the normal manner, in the deterministic way (MD=1).

The rewriting parts (X, Y) end always in a semicolon (;). If semicolons
or exclamation marks will be included in them, a percent character (%)
must be placed in front of them.

The resulting states are integers of the range 1 - 127. Moves to new
states are defined only as parameters in rules. To be meaningful, they
must occur in the state sets defined in the section STATE-SETS.

The parameter MOVE (MV) has several numerical values, and the parameter
for the mode of application (MD) has only the values 1 and 2.

Below is a detailed description of rule parameters.

### 3.2. Parameters for substitution: X, Y

Parameters for substitution, i.e. the section to be rewritten (X) and
the result of rewriting (Y), are concrete strings. Any strings may be
rewritten, including all punctuation marks and the space ( ). X must
be written starting immediately from the left margin. The juncture
indicating the end of the part X is the first semicolon (;). After the
semicolon there is one empty space. Then follows the substitution part
Y. If more than one blank is added after the first semicolon, those
will be part of the substitution string. Such empty spaces may
sometimes be useful, for example in indicating the place of the found
string in searching. Here are examples of substitution:

X; Y;        | replacement&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;           |    comments
-------------|-----------------------|-------------------------
`a; b;` | `"a" -> "b"`  |
`ab; ac;` | `"ab" -> "ac"` |
`abc; def;` | `"abc" -> "def"` |
`abc; d;` | `"abc" -> "d"` |
`a; ;` | `"a" -> ""` | (a, semicolon, space, semicolon) a is deleted
`a;  ;` | `"a" -> " "` | a is changed into a space
`abc; ;` | `"abc" -> ""` | (a, b, c, semicolon, space, semicolon)
`abc;`&#160;&#160;`;` | `"abc" -> " "` | (a, b, c, semicolon, two spaces, semicolon)
`abc;`&#160;&#160;&#160;`abc;` | `"abc " -> "`&#160;&#160;`abc"` | (a, b, c, semicolon, three spaces, a, b, c, semicolon) add two extra empty spaces in front of the string abc
&#160;`; ;` | `" " -> ""` | (space, semicolon, space, semicolon) a space character is deleted
`a; a;` |  | a is only observed; used e.g. when moving into another state  when a is encountered
&#160;;&#160;&#160;&#160;; | `" " -> " "` | (one space, semicolon, two spaces, semicolon) an empty space is only observed; used particularly in extraction when passing a word boundary; by adding the value of state by one each time when an empty space  has been encountered, it is possible to count how many words have been bypassed.


An important restriction on the substitution is that X and Y must be
*concrete strings*. By 'concrete' is here meant that the parts to be
rewritten *cannot contain abstractions*, which signify character sets.
If one wants, for example, to describe the variation of the nominal
prefix of the class 9/10 nouns in Swahili, one must write all of them
concretely with context conditions, e.g.:

    NI; n;          (parameter values)
    NI; ny;         (parameter values)
    NI; m;          (parameter values)
    NI; ;           (parameter values)

It is not, therefore, possible to use a set of segments defined in
CHARACTER-SETS, in the rewriting part of the rule, like this:

    CHARACTER-SETS
    #: #
    Ai: i a u
    RULES
    Ai; ;      0  #      (other parameter values)

This rule does not delete the vowels i, a and u in the context, where
the left context is anything and the right context is the end of the
input record. This rule deletes the string Ai in the given context, and
not the elements of the character set Ai. The intended effect will be
achieved in this way:

    CHARACTER-SETS
    #: #
    STATE-SETS
    RULES
    ! LC RC
    i; ;       0  #      (other parameter values)
    a; ;       0  #      (other parameter values)
    u; ;       0  #      (other parameter values)

There are two principles concerning the order of rules. If there are two
or more rules, each of which would apply to the X-part of the string,
the *longest one* is given precedence. If the X-parts are equally long,
the first in order is given precedence. This is the order of priority,
assuming that also the context (LC, RC) and state (SC) conditions are
fulfilled. If these conditions are not fulfilled, the next in the order
of priority is taken for similar testing.

If we apply, for example, to the string \#\#\>\>\>abcdefgh\#\# the
following rules:

    ab; ad;              (parameter values)
    abc; fgh;            (parameter values, the same or different)

first will be checked whether the context conditions of the latter rule
will be fulfilled (the conditions are not given in the example). If they
are met, abc -\> fgh. If they are not met, the context conditions of the
former rule will be tested. The string with a longer X-part may,
therefore, take rules which otherwise would fit also to other strings,
if context conditions are at least partly identical. If context
conditions are totally different, such 'bleeding' is not possible.

Another principle is that among the rules with identical X-parts,
rules will be sought for application in the order they are written in
the Beta grammar. There may be other rules in between. If there are
the following rules in the grammar:

    a; b;                (parameter values)
    a; ab;               (parameter values, the same or different)

first will be tried a -\> b. If the order of the rules is opposite, then
the rule a -\> ab will be tried first.

### 3.3. Context conditions: LC, RC

The context conditions (LC, RC) are expressed by the names of such
character sets, which have been defined in the section CHARACTER-SETS.
The sets of segments so defined consist of elements of *one character*
*only*, never of strings of characters. In the context conditions of a
Beta rule, it is possible to refer only to the segment immediately to
the left or right of the substitution part, and this segment may be only
one character long.

In 2.5 we had a simple example of how the entries in the section
CHARACTER-SETS should be formulated. Here we discuss this topic in
more detail. Below is given an example of a Beta grammar, which
describes the variation of the nominal prefix NI of the noun class
9/10 in Swahili.

    CHARACTER-SETS
    M: b v
    N: d g j z
    NY: a e i o u
    Zero: c f k m n p s t
    STATE-SETS
    RULES
    !       lc rc  sc rs mv md
    NI; m;   # M    0  0  5  1
    NI; n;   # N    0  0  5  1
    NI; ny;  # NY   0  0  5  1
    NI; ;    # Zero 0  0  5  1

As is seen in CHARACTER-SETS above, the definition of character sets
starts with the name of the set. The name is followed immediately by a
colon. After the name, the individual characters belonging to that set
are listed, separated by a space. These are the elements of the context
sets. In the above example, NI is rewritten as m, when the left context
is the input record boundary, and the right context is a character
belonging to the set M. In the definition under CHARACTER-SETS we see
that the right context may be either b or v. The string NI can be
rewritten also as n, ny, or zero, depending on the right context.

There are no restrictions as to the format of the set name. However,
some common sense and mnemonics is recommended to make the rules as
readable as possible. In the section CHARACTER-SETS, empty spaces are
allowed in the beginning of the line, as well as after the colon, and
between individual elements of the sets. But remember, *do not use tabs*
in writing a Beta grammar!

When the context on either or both sides can be anything, the
0-character (zero) is used to indicate that there are no restrictions.
There is no need to define the value of 0. Note that in the above
example, in the last rule, it is not possible to use the set name 0 for
the set of consonants, which cause the zero realization of the
substitution string. This is because the number 0 is reserved for
denoting non-restriction. Instead any other set name, in this case Zero,
is suitable.

If a complement of a character set or state set is needed, this is done
by placing the minus sign in front of the set name, e.g. -Segm, -Zero.
The complement set consists of all other characters that do not belong
to the given set.

It is possible to define as many sets as one considers needed. The
largest number of sets the program can digest is given in the
parenthesis, when the program is called. In practice, however, seldom
more than ten or twenty are needed.

It is up to the linguist to decide which sets are needed. The sets can
be natural or non-natural, depending on the given task. It is, of
course, theoretically sound to try to find as natural context conditions
as possible.

Upper and lower case characters have to be defined in the character
sets, if the task requires it. The program does not require, however,
that all the characters encountered in the input text are defined. Only
the characters referred to in context conditions must be defined.

### 3.4. State conditions

State conditions are sets of individual states. A set may contain one or
more states. There is no direct connection between an individual state
and the state condition with the same name. If only one state belongs to
a state set, it would be convenient to name the state using merely its
number, as follows:

    STATE-SETS
    14: 14

In case there are more than one state belonging to the same state set,
the use of numbers in naming the set is less informative. In the
following are examples of state sets:

    STATE-SETS
    Start: 1
    Cnt: 2 3
    3: 3
    456: 4 5 6
    35: 3 5

The definition of state sets and their application in practice, as well
as debugging, requires clear and logical thinking. The user decides
himself which state conditions will be taken into use, and which
individual states are defined belonging to each state set.

During substitutions, the rule processor is always in a certain
state. When a new logical record is red in, the process always starts
from state 1.  The rule processor continues to be in this state as
long as one of the rules moves the processor into another state. The
process continues in the state which is given in the fourth parameter
of the rule (RS), and if nothing is indicated, it continues in the
state where it was last moved in a rule application. But remember that
a new logical record read in starts again from state 1. State
conditions are one of the three conditions for the application of
rules (the other two are LC and RC). A rule is applied only when the
context conditions and the state condition are fulfilled.

The following example illustrates the interplay between states. Note
that, because of simplicity, context restrictions have been
eliminated.

    ! states.bta (illustrates the use of states)
    ! A.H. 15.4. 1992
    CHARACTER-SETS
    STATE-SETS
    Start: 1
    24: 2 4
    13: 1 3
    35: 3 5
    RULES
    !               lc rc   sc rs mv md
    ae; ai;          0  0 Start 4  5  1      (rule 1)
    i; ii;           0  0    24 3  5  1      (rule 2)
    ou; uu;          0  0    13 5  5  1      (rule 3)
    x; xx;           0  0    24 4  5  1      (rule 4)
    yz; yx;          0  0    35 6  5  1      (rule 5)
    a; b;            0  0 Start 2  5  1      (rule 6)

When the string *aeiouxyz* is entered, with trace on (by parameter -v
1), we get the following trace:

    $ beta.py states.bta -v 1
    aeiouxyz
    ae;ai; 0 0 Start 4 5 1
    ##ai >>> iouxyz## -- 4
    i;ii; 0 0 24 3 5 1
    ##aiii >>> ouxyz## -- 3
    ou;uu; 0 0 13 5 5 1
    ##aiiiuu >>> xyz## -- 5
    yz;yx; 0 0 35 6 5 1
    ##aiiiuuxyx >>> ## -- 6
    aiiiuuxyx

The trace output shows that four of the six rules have been applied.
Rule 1 is first applied, because the string immediately matches with
the X-part of the rule, and the state condition in the rule is Start,
which has the state 1 (the process always starts from state 1). Note
that rule 6 would also fulfil the conditions, but because its X-part
is shorter than that of rule 1, it loses the competition. It is also
sequentially later than rule 1. After application of rule 1, the state
is changed to 4, and the dot moves to show the character immediately
after the Y-part. There it 'sees' the string i and applies the rule,
because the state condition belongs to the set 24, where state 4 is
one of its members.  Rule 2 moves the state to 3, while the dot moves
to point the string o.  The string ou matches with the X-part of rule
3, and because its state condition is also met (state 3), the rule is
applied. State is moved to 5 and the dot points to the string x. At
first look it seems as if also rule 4 would apply, because its X-part
matches with the string. It does not, however, because the state
condition is not met. The dot moves forward to find possible rules to
apply, and finds the string yz, which is the X-part of rule 5. Because
its state conditions (35) include the state 5, the rule is applied,
and the state is moved to 6. Because no more rules apply, the
resulting string is monitored.

### 3.5. Resulting states: RS

How the rules are applied depends on the condition parameters (LC, RC,
SC). When a rule has applied, normally the control is moved to another
state, and the number (or name) of the new state is indicated by the
fourth rule parameter (RS=resulting state). The resulting state is
always a *move to a single state*. The *states should not be mixed with
the state condition* (SC), which is always given as a set name. Here are
some examples:

    !        lc rc sc rs mv md
    ab; abc;  #  0 11  7  5  1
    a; ;      0  # S2 11  5  1
    ; ;       0  0 Se  9  5  1

After the application of the first rule, the program is moved to state
7; the second rule moves it to state 11, and the third moves it to state
9. The number of the new state can be bigger or smaller than the current
state. Generally, the chains of resulting states are ascending, but
moves to lower states are equally possible.

One single state may be simultaneously a member of more than one state
set.

Here are some additional conventions for resulting states. If there is
no need to move the state after the application of a rule, the RS
parameter will be given a value 0 (zero). Let us look at the following
example:

    CHARACTER-SETS
    STATE-SETS
    S1: 1
    S12: 1 2
    RULES
    !       lc rc  sc rs mv md
    AB; AC;  0  0  S1  2  5  1
    A; D;    0  0  S1  0  5  1
    E; F;    0  0 S12  0  5  1

If the input string is ABE and the state is 1, rule 1 produces the
string ACE, and the process moves to state 2. In this state, rule 3 is
applied, and this produces the string ACF, while the state is not moved.
Then the input string AE matches with the rule 2 in state 1, and the
output is DE, but the state does not move. Now the input string DE
matches with rule 3, and the output is DF, while the state continues to
be 1.

Another important convention concerns such cases, where the context
condition of the rule relates to several states, and, by the application
of the rule, there is a need to elevate the value of all states in
question by one. Such is the case, for example, when different states
are memories of the rules applied before, and there is a need to store
this information for further computing, but combined with the
information on the application of the current rule. This may be done by
giving the RS-parameter the value -1. This somewhat illogical convention
means: 'elevate the current state by one'. Correspondingly, -2
elevates the state by two etc. For example:

    ...
    STATE-SETS
    X3: 3 13 23
    RULES
    !      lc rc sc rs mv md
    B; G;   0  0 X3 -1  5  1

If the input is BDF, and the state is 13, the rule applies and the new
state is 14. If the input is B while being in state 24, the state after
the application of the rule will not change and it will be 24.

In the normal case, i.e. when the parameter value of RS is positive, the
same move of state concerns all the states included in the relevant
state set. If the above rule were in the form:

    RULES
    !     lc rc sc rs mv md
    B; G;  0  0 X3  8  5  1

and the state sets were the same as above, the states 3, 13, and 23
would all move, after the application of the rule, into state 8. The
convention described by -1 is needed when the states belonging to the
same state set must be kept separate also after the application of a
certain rule. Such a collective elevation of states presupposes careful
scaling of the states, and the establishment of sufficiently large
intervals between groups of states, which belong together.

### 3.6. The move parameter

Beta processes a logical record character by character, testing whether
any of the rules applies, and if an applicable rule is found, the
further analysis continues from the spot, where the dot is moved after
the application of the rule. There are several alternatives to position
the dot after substitution.

When the record is red in, a double hatch `##` is placed to the
beginning and the end of the record. The hatch has an important function
in showing the beginning and end of the record. If there is \# on the
left side of a certain character, it marks the beginning of the record.
If \# is located to the right of the character, it marks the end of the
record. Because of the special meaning of the hatch (\#) character it is
recommended that this character will not be used except for indicating
the beginning and end of the logical record.

The analysis of the record proceeds, if nothing else is defined in the
MV-parameter, character by character from left to right. By each
character, the applicability of rules is tested. If an applicable rule
is encountered, it is applied; if not, the dot moves one character to
the right looking for applicable rules. The rule applied defines the
point in the string, where the search continues.

When testing applicable rules, Beta takes, at each character, the string
from the dot to the right under scrutiny. Remember that if there are
more than one rule applicable at any one time, the one with the longest
X-part has precedence.

The dot is exactly in the place where it is moved, or where it moves by
its default definition. When using the trace facility, the three angle
brackets `>>>` show the location of the point after substitution.
It is always in the place where it is moved by the fifth parameter (MV)
of the rule. If no rule is applicable for the given string, the dot
moves one character forward. Potentially applicable rules are those, the
substitution part of which (X-part) is found to the right of the dot.

In the beginning of analysis, the dot is after the inital pair of hash
signs in the record; it is part of the record to be analyzed:

    ## >>> abcdefg##

Beta tries to apply rules to the following strings, and in this order*:
abcdefg, abcdef, abcde, abcd, abc, ab, a, ''* The first
suitable rule is applied, and then the process continues as defined by
the rule. If there is no matching rule, the dot moves one character to
the right and the process continues:

    ##a >>> bcdefg##

Now the following strings will be analyzed: *bcdefg, bcdef, bcde*
\... etc.

The MV-parameter has six central numerical values, and each of them
relocates the dot into a certain place compared to its present location.
In order to illuminate the various possibilities, let us take a string
*aacdefg*, and in the rules the rule d -\> xy. The six possible values
of the MV-parameter and their consequences are the following. Note that
after substitution the string d is rewritten as xy, as the rule defines.
Thus the rewritten string xy matches with the Y-part of the rule.

The value The location of dot Dot moved to

of MV after rule application point to

1. \# \>\>\> \#aacxyefg\#\# the second of two hatches in the beginning of
the record

2. \#\#aa \>\>\> cxyefg\#\# the character before Y, the one which was LC

3. \#\#aac \>\>\> xyefg\#\# the first character of Y, i.e. the character
after LC

4. \#\#aacx \>\>\> yefg\#\# the last character of Y, i.e. the character
before RC

5. \#\#aacxy \>\>\> efg\#\# the character after Y, i.e. the character
which was RC

6. \#\#aacxyefg \>\>\> \#\# the end of record

If Y is empty, i.e. if the X string is deleted, the MV-points 2 and 4
are mutually identical, as well as the points 3 and 5.

The MV-parameter has two other additional values, used in special cases:

0: the record is deleted

7: the record is accepted without further analysis

The value 0 is important in extraction, because it enables the deletion
of such records, which do not have the searched strings. The value 0 is
also important in cases where the task is to delete records (e.g. lines)
defined in rules. The value 7 is used when a hit is encountered and
there is no need to test the applicability of other rules. This speeds
up the process to some extent.

Below are the values of the MV-parameter shown in a schematic form:

    # # A B C LC Y Y Y RC F G H # #
       |     |  |   | |        |    |
       1     2  3   4 5        6    7

### 3.7. The mode of application

The sixth parameter of the rule (MD) defines the way how the rule will
be applied. The parameter value 1 defines a deterministic application,
and the value 2 effects a non-deterministic application. By choosing the
value 1, which is the normal case, the first applicable rule will be
applied, without investigating whether there are other applicable rules,
which also could be applied here. After the application of the rule, the
processing continues from the point, to which the MV-parameter of the
rule moved it.

By choosing the non-deterministic application (value 2) the current rule
will be applied, but it will also be left unapplied. Therefore, another
copy will be created of the current record. The current rule will be
applied to the other copy of the record, and the state is changed to the
value defined by the RS-parameter, and the dot is placed as defined by
the MV-parameter. The first copy of the record will be left as it was,
and it will be checked whether there are also other rules which would
apply. If there are, they will be applied in the order of priority. If
no other rules apply, the dot moves one character to the right and the
process continues as usual.

For demonstrating the function of the non-deterministic mode of
application, let us look at the following task. We want to generate some
of the tense forms of Swahili verbs by writing only the string +TENSE+
in place of the tense marker. We write the following Beta grammar:

    ! tense.bta (produces some Swahili tense forms)
    ! A.H. 15.4. 1992
    CHARACTER-SETS
    STATE-SETS
    RULES
    +TENSE+; +NA+; 0 0 0 0 5 2
    +TENSE+; +ME+; 0 0 0 0 5 2
    +TENSE+; +LI+; 0 0 0 0 5 2
    +TENSE+; +KA+; 0 0 0 0 5 1

If we now enter the string NI+TENSE+SOMA, with trace on, we get the
following output:

    $ beta.py tense.bta -v 1
    NI+TENSE+SOMA
    +TENSE+;+NA+; 0 0 0 0 5 2
    ##NI+NA+ >>> SOMA## -- 1
    +TENSE+;+ME+; 0 0 0 0 5 2
    ##NI+ME+ >>> SOMA## -- 1
    +TENSE+;+LI+; 0 0 0 0 5 2
    ##NI+LI+ >>> SOMA## -- 1
    +TENSE+;+KA+; 0 0 0 0 5 1
    ##NI+KA+ >>> SOMA## -- 1
    NI+NA+SOMA
    NI+ME+SOMA
    NI+LI+SOMA
    NI+KA+SOMA

The trace shows that all four rules have been applied at the point where
they were applicable. Each application produced a separate branch of
processing because of the value of the parameter MD was 2. Normally,
when MD is 1, only the first rule would have been applied and the other
three would have been skipped because the first rule changes the string.
One can understand the non-deterministic rules so that they both apply
the rule and don't apply it. Not applying means that the Beta processor
skips this rule and continues to find further rules or maybe step
further to the right. Note that the fourth rule has explicitly MD value
1. Otherwise, we would have a fifth copy where none of the four rules
have been applied. The interested reader is encouraged to try the above
example with the more intensive tracing '-v 2' in order to see in detail
the order in which these four parallel strings are processed.

The non-deterministic application of the rules is used especially in
describing free variation. Non-deterministic rules are also practical
for extracting occurrences from text. With them one can locate, mark and
output sentences where the words or constructions occur, even if there
were several occurrences in the same sentence.

### 3.8. Abbreviations in rules

There are several conventions, which can be used in writing rules.

If two or more consecutive rules have identical parameter values, it is
enough to write the values to the topmost rule. If no parameters are
given in a rule, the values of the previous rule are taken as the values
of the rule. It would have been more economical to write the above rules
in this way:

    +TENSE+; +NA+; 0 0 0 0 5 2
    +TENSE+; +ME+;
    +TENSE+; +LI+;
    +TENSE+; +KA+; 0 0 0 0 5 1

Note that all the values of the last rule must be written, because the
last parameter is different than in other rules.

If consecutive rules have partly identical parameter values, there is no
need to rewrite those values, which, counted from the right, can
unambiguously be identified as belonging to certain columns. In the
following examples the parameters placed in parentheses may be left
unwritten.

    !      lc  rc  sc   rs  mv  md
    A; B;   V   R   S7   9   5  1
    C; D;   C Sgm   12   8  (5  1)
    E; F;   V   P   S7   9   4  2
    C; D;   C  (P   S7   9   4  2)
    G; H;   V   P   S7   9   4  1
    CC; N;  C Sgm   12   8  (4  1)
    E; FF;  Z   Q  (12   8   5  1
    GG; H;  V  (Q   12   8   5  1)
    J; K;  (V   Q   12   8   5  1)

As can be seen above, the empty spaces get their interpretation
according to the value found above in the same column. This convention
to abbreviate the description is commonly used in the last parameter,
the value of which is commonly 1. If all the rules are applied in a
deterministic way, it is enough to give the value 1 in the first rule
only. And even there it is not necessary, because the default value of
this parameter is 1.

Excessive abbreviation of rules may sometimes cause difficulties in
interpreting rules. It is often useful to write up all the parameters of
the first rule in the group of rules, which otherwise belong together
and have the same parameter values.

Special care must be taken not to abbreviate the description, if all the
parameters to the right are not identical with the previous rule. If we
have the following rules:

    !    lc rc sc rs mv md
    A; B; #  0  S  3  5  1
    C; D; #  0  S  4  5  1

we *cannot* abbreviate them in this way:

    !    lc rc sc rs mv md
    A; B; #  0  S  3  5  1
    C; D;          4

The latter rule would be interpreted so that it has the value 4 as LC,
while it takes the rest of the parameters from the previous rule.
Therefore, the only possible abbreviation is the following:

    !    lc rc sc rs mv md
    A; B; #  0  S  3  5  1
    C; D; #  0  S  4

## 4. LIMITOR: The definition of the input record

The Beta program can process logical records of various lengths,
depending on the need in each case. Such input records can be single
words, clauses, sentences, and physical lines. The type of the input
record is defined by a character set called LIMITOR within the section
CHARACTER-SETS. If no such set is defined, the Beta program assumes that
the delimiter is BLANK, i.e. the empty space. By default, Beta reads in
strings of characters, which are delimited on both sides by (at least
one) empty space or the beginning or end of a line.

If we want to process the input lines as the units, we may define a
LIMITOR set which contains just a `#` sign. Otherwise the LIMITOR set
contains the characters which delimit the units we want to process. We
might e.g. want to process each sentence as a unit. We may use
punctuation marks such ('.', ';', '?', '!') as delimiters in the LIMITOR
set. The Beta program, then, reads in units up to the next delimiter,
even if that would be on another line. The delimiters are not part of
the record processed by the Beta program, only the text between the
delimiters. It is obvious that punctuation marks are not always only at
the sentence boundaries but in practice such approximations are quite
useful.

Sometimes there is a need to read in logical records longer than a
sentence. For such tasks the text may be temporarily provided with
special characters, which are defined for Beta as delimiters. Another
and often more natural solution is to keep the record as a single line,
whereby no temporary tagging is needed.

Below are some examples, which show the effect of various delimiters and
their combinations on the input record:

    LIMITOR: BLANK                              (record is a word)
    LIMITOR: #                         (record is a physical line)
    LIMITOR: . ? !       (record is a sentence; narrow definition)
    LIMITOR: . ? ! : ;    (record is a sentence; broad definition)

The present Beta version does not take a paragraph as such as input.
This effect can be achieved by marking first the paragraph boundaries
with a certain character and by defining it as the delimiter. Another
useful convention, for example in corpus texts, is to keep the whole
paragraph as a single line. The advanced program editors, such as those
belonging to the Emacs family, allow the use of lines with the length of
thousands of characters.

## 5. TEXT EXTRACTION

### 5.2. General

Although Beta is actually a rewriting program, it is also useful in text
extraction. It is possible to extract phonological, morphological and
syntactic structures. If the text has been encoded, it is possible to
use these codes as criteria in searching.

The structures to be searched will be defined by using rules, following
the conventions described in section 3. In text extraction, strings are
rewritten as such (i.e. Y-parts are equal to X-parts), and the strings
found will be monitored, while other strings will be discarded.

In the following, the string to be searched is called a key, and the
case which fulfils the conditions for searching is called a hit. There
is normally context around the hit. It is possible to use e.g. the
following kinds of keys in searching:

1. Parts of individual words (prefixes, suffixes, endings etc.).

2. Individual words.

3. Strings of consecutive words.

4. Strings of words (or parts of words) which appear consecutively or
with other words in between.

In fact, a skilled user of Beta can extract most of the needed
structures from the untagged normal text. This is a big advantage,
taking into account the laborious task of tagging the text just because
of facilitating text extraction. If the text is already tagged, as is
the case in many annotated corpora, text extraction is naturally easier
and more effective.

### 5.2. Text extraction on the basis of individual words

In searching, we must make sure that all searched strings are found. We
must keep in mind that one input record may contain more than one hit.
Therefore, we must make sure at least that searching is
non-deterministic. Otherwise one input record would produce one result
only; i.e. only one hit would be monitored. Let us demonstrate the task
with a simple example. We have a string:

    there were boys and girls and many adults

and we want to find the occurrences of the string 'and'. We should get
the following output:

    there were boys <and> girls and many adults
    there were boys and girls <and> many adults

The following simple Beta grammar performs the task:

    CHARACTER-SETS
    B: BLANK #
    #: #
    LIMITOR: #
    STATE-SETS
    1: 1
    RULES
    !            lc rc sc rs mv md
    and; <and>;   B  B  1  0  7  2
    #; #;         0  #  0  0  0  1

If no string is found where the first rule applies, the dot continues to
move forward, until in the end of the record it encounters the final
hatch `#`. Now the second rule applies, and because its MV-parameter
is 0 (see 3.2.5.), the whole string is discarded. If a string and is
found, with a blank or boundary character on both sides, the process is
divided into two parts. The first branch continues further in state 1
without applying the first rule yet, looking for other similar strings.
The second branch applies the first rule, and because its MV-parameter
is 7, the whole record is monitored immediately. The first branch will
later find another string *and*, where it again branches out. The first
branch continues still further, until it will be killed at the final
hatch (rule 2 applies). The new branch applies the first rule to the
second occurrence of the string and, and monitors it immediately.

If we want to extract several kinds of strings simultaneously, we may
add them to the rules. For example, the following Beta grammar
extracts the occurrences of the words: *and*, *or*, *but*.

    CHARACTER-SETS
    B: BLANK #
    #: #
    LIMITOR: #
    STATE-SETS
    1: 1
    RULES
    !           lc rc sc rs mv md
    and; <and>;  B  B  1  0  7  2
    or; <or>;
    but; <but>;
    #; #;        0  #  0  0  0  1

### 5.3. Extraction of structures

The basic principle in searching for more complex structures is the same
as described above. When an applicable rule is found, the process
branches out for finding further hits. The found string cannot be
monitored yet, however, because only the first part of the structure is
found, and it is not sure whether the entire structure will be found.

The solution to this problem is that the rule which finds the first part
of the structure marks its beginning and moves to a state which keeps
memory of the hit of the first part of the structure. If other part(s)
of the structure are found, the end of the structure is marked and the
whole record is monitored. Only such records will be monitored, where
the whole structure is found; all other records will be discarded.

Below is a Beta program which extracts verb constructions with the
auxiliary verb *kuwa* in Swahili. The Beta grammar is quite
complicated, due to the multitude of possible prefixes of the
auxiliary verb and the main verb. For the sake of simplicity, negative
forms have been omitted.

    ! SW-AUX.BTA, extracts auxiliary verb constructions of
    ! Swahili, 15.4.1992, A. Hurskainen
    !
    CHARACTER-SETS
    #: #
    B: BLANK # . , ? ! ; :
    S: a b c d e f g h i j k l m n o p q r s t u v w x y z
    LIMITOR: . ? !
    STATE-SETS
    1: 1
    2: 2
    3: 3
    4: 4
    5: 5
    6: 6
    7: 7
    RULES
    ! mark the subject prefix of the auxiliary verb
    !               lc rc sc rs mv md
    ni; <<ni=;       B  S  1  2  4  2
    u; <<u=;
    a; <<a=;
    tu; <<tu=;
    m; <<m=;
    wa; <<wa=;
    li; <<li=;
    ya; <<ya=;
    ki; <<ki=;
    vi; <<vi=;
    i; <<i=;
    zi; <<zi=;
    ku; <<ku=;
    pa; <<pa=;
    !
    ! find the tense marker and then look for the
    ! auxiliary verb stem
    !               lc rc sc rs mv md
    =na; na=;        S  S  2  3  4  2
    =li; li=;
    =ta; ta=;
    =nge; nge=;
    =ngali; ngali=;
    !
    ! tense marker, followed by the relative prefix
    !               lc rc sc rs mv md
    =na; na=;        S  S  2  7  4  2
    =li; li=;
    =taka; taka=;
    !
    ! find the relative prefix and then look for
    ! the auxiliary verb stem
    !                lc rc sc rs mv md
    =ye; ye=;         S  S  7  3  4  1
    =o; o=;
    =lo; lo=;
    =yo; yo=;
    =cho; cho=;
    =vyo; vyo=;
    =zo; zo=;
    =ko; ko=;
    =po; po=;
    =mo; mo=;
    !
    ! auxiliary verb 'kuwa' (with infinitive marker *ku*)
    !               lc rc sc rs mv md
    =kuwa; kuwa;     S  B  3  5  5  1
    !
    ! tense marker of the verb (does not require
    ! infinitive marker)
    =ka; ka=;        S  S  2  4  4  1
    =ki; ki=;
    !
    ! auxiliary verb 'wa' (without infinitive marker *ku*)
    !               lc rc sc rs mv md
    =wa; wa;         S  B  4  5  5  1
    !
    ! When the auxiliary verb is found,
    ! then look for the main verb.
    !
    ! subject prefix of the main verb
    !               lc rc sc rs mv md
    ni; ni=;         B  S  5  6  4  1
    u; u=;
    a; a=;
    tu; tu=;
    m; m=;
    wa; wa=;
    li; li=;
    ya; ya=;
    ki; ki=;
    vi; vi=;
    i; i=;
    zi; zi=;
    ku; ku=;
    pa; pa=;
    ! tense marker of the main verb
    !               lc rc sc rs mv md
    =na; na>>;       S  S  6  0  7  2
    =ki; ki>>;
    =me; me>>;
    !
    ! If the rule has applied thus far,
    ! assume that the rest of the string is verb stem.
    ! No further tests made.
    !
    ! Abandon other alternatives.
    !
    #; #;            0  #  0  0  0  1

The above Beta grammar has been so structured that it minimizes the
need of writing rules. It utilizes the restrictions of various
morpheme combinations, and therefore the X- and Y-parts contain only
one morpheme. Particularly notice the use of a temporary tag '=' in
the morpheme boundary, where any of a set of morphemes may combine
with any of another set of morphemes. The dot in such rules is moved
to point the last character of the Y-part, which is the tag
'='. When the control continues to look for applicable rules, it
'sees' this tag first. Only such rules apply on this point, the
X-part of which starts with this tag. By prefixing the possible
following morphemes with this tag, the application of the rule in a
wrong place (e.g. when a similar string is encountered later in the
record) is avoided. Notice also the use of state changes in directing
permissible combinations. The first and last ones of the pattern
combination rules are applied non-deterministically, thus allowing
them to apply to more than one string in the record. When the process
of constructing the structure has initiated, the mode of application
is normally deterministic, except in such cases, where a possibility
for application must be given to competing rules (rules for
alternative morpheme markers).

## 6. THE EXECUTION OF THE PROGRAM

### 6.1. Input and output

The following guidelines apply to the Linux and Unix systems. In order
to get information on the use of the program, one may first ask it for
help:

    $ beta.py --help

The program responds by listing the different parameters it
understands and their short forms. Then, one can start the Beta
program e.g. for testing. When the Beta program is called, also a Beta
grammar file must be given to it.

    $ beta.py sw-aux.bta

Now Beta expects input from the keyboard, and the standard output is the
screen. This is a useful mode of operation when testing rules and
studying their operation, possibly with trace on (with the additional
parameter '-v 1' or by entering a double hash `##`).

If input is taken from a file, this will be given as the third
parameter. Also, in this case the output is seen on the screen.

    $ beta.py sw-aux.bta < test.txt

### 6.2. Trace

When testing and debugging rules, it is often useful to have the trace
facility on. One can start the Beta program with a parameter '-v 1' or
'-v 2' for tracing. The weaker tracing can also be started in the middle
of an interactive session by entering a double hash `##`. By
entering the double hash again, the trace will be turned off. The trace
facility prints out every rule which is applied and shows the point
where the dot was moved after the application of the rule.

### 6.3. Capacity of the Python Beta program

The Python Beta program has no specific limits for the number of rules,
character sets or state sets. Python system adapts to the needs of each
execution of the Beta program. Present-day computers, even modest
laptops, appear to have so much memory that even large Beta rule sets
can be processed without any problems.

### 6.4. What is Beta good for in 2018?

Processing of text has developed tremendously since the time when Beta
became available for the first time. There are several tasks in language
processing that can be performed in a number of ways. Especially Linux
and Unix have many utilities that can be used for many tasks described
above. It is a wise policy that the user makes use of such programs,
utilities and programming languages that one is familiar with, because
the end result is what counts.

It was pointed out above that Beta rules do not support regular
expressions. This is a true limitation of Beta, and it should be taken
into account when choosing the strategy for performing the required
task. An example of the power of regular expressions is the
implementation of a rewriting program that converts the disjoining
writing system of Kwanyama language into the conjoining system
(conjoining writing is predominant in Bantu languages). The system was
programmed in Beta and Perl. The Beta version required a total of
187,000 rules for verbs alone, while the Perl implementation needed only
48 rules.

It can be claimed that all what is done by Beta can be done with
generally available programming tools. It may be true, but it is not
always convenient to do so. For example, the power of state conditions
is normally not available in other tools. Although the linear context
conditions (LC and RC) are available in Perl, for example, the
processing cannot be controlled with a third parameter, which state
conditions provide.

Beta is good in retrieving or extracting strings with varying context.
In addition to the default record size (a string) and the line delimiter
`#`, one can define other characters as a delimiter and thus define the
size of the context in string retrieval. Beta is especially good in
retrieving strings, each of which has a form of its own, and regular
expressions cannot be used for generalizing search. The writing of rules
can be automated with scripts or macros, so that a minimal amount of
typing is needed. Therefore, individual words from text can be
retrieved, as well as the words with context, defined with varying
criteria.

But Beta alone is not ideal for concordances, where hits need to be
aligned and perhaps sorted according to the right or left context. There
are many such programs freely available, especially in Linux
environment.

Beta is also good in deleting strings, although this facility is often
forgotten. The RS value 0 of the rule causes the record to be deleted.
Thus, by defining the record size carefully it is possible to delete
from text individual words, lines, sentences, etc. In fact, what can be
retrieved can also be deleted. Beta is a handy device for comparing the
contexts of two lists, because it does not require the lists to be
sorted first, which most utilities require, before comparison becomes
meaningful. With Beta it is possible to delete from list A such words
that are found in list B, and vice versa, and the order of the words in
lists does not matter. Also, words shared by both lists can be retrieved
with the retrieving option. Therefore, the union and intersection of two
lists can be performed with Beta.

Finally, we would like to point out that although Beta can perform a
wide range of tasks, it is wise to look for the easiest, yet reliable,
way of solving the problem. Often it is not Beta, but if you are
convenient with Beta, you will often find yourself implementing it with
it. And there are tasks that are very hard to implement without Beta.

## Appendix


### Installing the Python Beta program

In order to use the Python Beta program, one needs to have a fairly
recent version of Python3 installed and the beta.py file which is
located in https://github.com/koskenni/beta and is freely
available. The detailed instructions for installing the program are
found in the [Beta wiki](https://github.com/koskenni/beta/wiki/). One
related package, datrie, is needed in addition to the beta.py program
itself. See the instructions in the same Beta wiki. Please, report to
the author if you meet any problems in installing or using beta.py.


### Characters which can be used in the Beta grammars and in input texts 

Letters and symbols that can be used as characters in Beta consist of
Unicode UTF-8 characters which are needed for writing those European
languages which use some Latin alphabet. Thus, Greek and Cyrillic
scripts cannot be used without some minor modifications in the Python
Beta program.

ASCII printable characters:

```
      0123456789abcdefghijklmnopqrstuvwxyz  
      ABCDEFGHIJKLMNOPQRSTUVWXYZ  
      !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
```
	  
Latin alphabet characters used by European languages (roughly the
following ones):

```
      ´áÁćĆéÉíÍĺĹńŃóÓŕŔśŚúÚẃẂýÝźŹǽǼǿǾǻǺ
      ˘ăĂĕĔğĞĭĬŏŎŭŬˇǎǍčČďĎěĚǧǦȟȞǐǏǩǨľĽňŇǒǑřŘšŠťŤǔǓžŽǯǮ
      ¸çÇģĢķĶļĻņŅŗŖşŞţŢ
      âÂĉĈêÊĝĜĥĤîÎĵĴôÔŝŜûÛŵŴŷŶ
      ¨äÄëËïÏöÖüÜẅẄÿŸ
      ˙ḃḂċĊḋḊėĖḟḞġĠİṁṀṗṖṡṠṫṪżŻ
      ạẠẹẸịỊọỌụỤỵỴ˝őŐűŰàÀèÈìÌòÒùÙẁẀỳỲ
      ¯āĀēĒīĪōŌūŪǣǢǟǞ˛ąĄęĘįĮǫǪųŲ˚åÅůŮãÃẽẼĩĨñÑõ
      ÕũŨỹỸđĐǥǤħĦłŁøØŧŦ
      ắặằẳẵẮẶẰẲẴấậầẩẫẤẬẦẨẪếệềểễỆỆỀỂỄốộồổỗỐỘỒỔỖ
      ǟǞȧǡȦǠảẢẻẺỉỈỏỎủỦỷỶơ
```

### Converting eight-bit texts and Beta grammar files into Unicode UTF-8

From eight-bit Latin-1 to UTF-8

    $ iconv -f ISO8859-1 -t UTF-8 < latin.txt > unicode.txt

If you need to use other coding systems, you can find a list of the
names of all coding systems that the program knows by:

    $ iconv --list

### Python Beta help

```
$ beta.py --help
usage: beta.py [-h] [-i INPUT] [-o OUTPUT]
               [-v VERBOSITY] [-m MAX_LOOPS]
               rules

positional arguments:
  rules                 the name of the beta rule grammar file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        file from which input is read if not stdin
  -o OUTPUT, --output OUTPUT
                        file to which output is written if not stdout
  -v VERBOSITY, --verbosity VERBOSITY
                        level of diagnostic output
  -m MAXLOOPS, --max-loops MAXLOOPS
                        maximum number of cycles per one input line
                        rule file    rule file
```
