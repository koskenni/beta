#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5
# beta.py - Version 0.5.3
#
copyright = """Copyright © 2017-2018, Kimmo Koskenniemi
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#
# Reimplementation of the Beta string rewriting engine originally
# written by Benny Brodda in Fortran and later on reimplemented by
# Kimmo Koskenniemi in Pascal and in C.
# The input formalism follows the C version as documented in
# F. Karlsson and K. Koskenniemi, "Beta-ohjelma kielentutkimuksen apuvälineenä",
# Yliopistopaino, 1990.
#
# This program was written from scratch in Python3 without any
# reference to the predecessors mentioned above.
#
from collections import deque
import string
import datrie

euroletters = "´áÁćĆéÉíÍĺĹńŃóÓŕŔśŚúÚẃẂýÝźŹǽǼǿǾǻǺ˘ăĂĕĔğĞĭĬŏŎŭŬˇǎǍčČďĎěĚǧǦȟȞǐǏǩǨľĽňŇǒǑřŘšŠťŤǔǓžŽǯǮ¸çÇģĢķĶļĻņŅŗŖşŞţŢâÂĉĈêÊĝĜĥĤîÎĵĴôÔŝŜûÛŵŴŷŶ¨äÄëËïÏöÖüÜẅẄÿŸ˙ḃḂċĊḋḊėĖḟḞġĠİṁṀṗṖṡṠṫṪżŻạẠẹẸịỊọỌụỤỵỴ˝őŐűŰàÀèÈìÌòÒùÙẁẀỳỲ¯āĀēĒīĪōŌūŪǣǢǟǞ˛ąĄęĘįĮǫǪųŲ˚åÅůŮãÃẽẼĩĨñÑõÕũŨỹỸđĐǥǤħĦłŁøØŧŦắặằẳẵẮẶẰẲẴấậầẩẫẤẬẦẨẪếệềểễỆỆỀỂỄốộồổỗỐỘỒỔỖǟǞȧǡȦǠảẢẻẺỉỈỏỎủỦỷỶơớợờờỡƠỚỢỜỞỠưứựừửữƯỨỰỪỬỮǭǬǻǺƒﬁﬂĳĲŀĿŉɼſẛẛșȘțȚ"

punctuation = ''.join([chr(i) for i in range(160,192)])
characters = string.printable + euroletters + punctuation
allowed_characters = set(characters)

trie = datrie.Trie(characters)
chset = {}
stset = {}

def betaproc(line, max_cycles, verbosity, output_file):
    global trie, chset, stset
    cycles = 0
    items = deque()
    item = ("#", "#" + line + "##", 1)
    item_set = {item}
    items.appendleft(item)
    while len(items) > 0:                              # item loop
        cycles += 1
        if cycles > max_cycles:
            print("** possibly an infinite loop, stopped at", max_cycles)
            return
        left, right, state = items.pop()
        if verbosity > 1:
            print("    " + left + " >>> " + right + " -- " + str(state))
        if len(right) <= 1 and len(left) >= 2:
            print(left[2:-1], file=output_file)
            continue                         # nothin more for this item
        rule_items = trie.prefix_items(right)
        item_list = []
        for x in rule_items:
            item_list.append(x)
        if verbosity >= 10:
            print("list of prefix items:", item_list)
        for x, rule_list in reversed(item_list):       # prefix loop 
            for rule in rule_list:                     # rule loop
                if verbosity >= 10:
                    print("testing for rule:", rule)
                y, lc, rc, sc, ns, mv, md = rule
                if lc != '0':
                    if lc[0] == '-':
                        if left[-1] in chset[lc[1:]]:
                            continue         # no more tests for this rule
                    elif left[-1] not in chset[lc]:
                        continue             # no more tests for this rule
                    if verbosity >= 10:
                        print("left conditon tested and satisfied")
                if rc != '0':
                    if rc[0] == '-':
                        if right[len(x)] in chset[rc[1:]]:
                            continue         # no more tests for this rule
                    elif right[len(x)] not in chset[rc]:
                        continue             # no more tests for this rule
                    if verbosity >= 10:
                        print("right conditon tested and satisfied")
                if sc != '0':
                    if sc[0] == '-':
                        if state in stset[sc[1:]]:
                            continue         # continue with next rule
                    elif state not in stset[sc]:
                            continue         # continue with next rule
                    if verbosity >= 10:
                        print("state conditon tested and satisfied")
                # all tests passed for this rule
                if mv == 0:             # delete this item
                    left1 = ""
                    right1 = ""
                elif mv == 1:           # move to the beginning
                    left1 = "#"
                    right1 = "#" + left[2:] + y + right[len(x):]
                elif mv == 2:
                    left1 = left[:-1]
                    right1 = left[-1:] + y + right[len(x):]
                elif mv == 3:
                    left1 = left
                    right1 = y + right[len(x):]
                elif mv == 4:
                    left1 = left + y[:-1]
                    right1 = y[-1] + right[len(x):]
                elif mv == 5:
                    left1 = left + y
                    right1 = right[len(x):]
                elif mv == 6:
                    left1 = left + y + right[len(x):-2]
                    right1 = "##"
                elif mv == 7:           # accept this item immediately
                    left1 = left + y + right[len(x):]
                    right1 = ""
                    print(left1[2:-2], file=output_file)

                if verbosity > 0:
                    print("    " + x + ";" + y + "; ", lc, rc, sc, ns, mv, md)
                if ns < 0:              # neg rs increments
                    ns = state - ns
                elif ns == 0:           # zero rs keeps the state
                    ns = state

                if verbosity == 1:
                    print("    " + left1 + " >>> " + right1 + " -- " + str(ns))

                if len(left1) >= 1 and len(right1) >= 2:
                    items.appendleft((left1, right1, ns))
                if verbosity >= 10:
                    print((left1, right1, ns), "pushed to the queue")
                if md != 2:             # non-deterministic rule
                    break               # leave the 
            else:                            # all rules for this prefix tested
                continue                     # to the next prefix
            break                       # leave the prefix loop
            #                             (reached by breaking the rule loop)
        else:                                # all prefixes processed 
            if len(right) > 0:
                left1 = left + right[0:1]
                right1 = right[1:]
                item = (left1, right1, state)
                if item in item_set:
                    print("** have been in this configuration before:", item)
                items.appendleft(item)
                if verbosity >= 10:
                    print("shifting one step to the right")
    return

import re

def decode_quoted(str):
    str = str.replace("%;", ";")
    str = str.replace("%!", "!")
    str = str.replace("%n", "\n")
    str = str.replace("%t", "\t")
    str = str.replace("%%", "%")
    return(str)

def character_sets(list_of_set_defs, verbosity):
    global chset, args
    for lineno, set_def in list_of_set_defs:
        if verbosity >= 20:
            print(lineno, ">>>" + set_def + "<<<") ##
        mat = re.match(r"^\s*([^( :]+):\s+(.+)\s*$", set_def)
        if mat:
            set_name = mat.group(1)
            symbol_str = mat.group(2)
            symbol_list = re.split(r"\s+", symbol_str)
            symbol_list = [' ' if x == "BLANK"
                               else decode_quoted(x) for x in symbol_list]
            chset[set_name] = set(symbol_list)
        else:
            print(lineno, ":", set_def, "** incorrect set definition")

def state_sets(list_of_set_defs, verbosity):
    global stset, args
    for lineno, set_def in list_of_set_defs:
        if verbosity >= 20:
            print(lineno, ">>>" + set_def + "<<<") ##
        mat = re.match(r"^\s*([-\w*]+):\s+(.+)\s*$", set_def)
        if mat:
            set_name = mat.group(1)
            state_str = mat.group(2)
            str_list = re.split(r"\s+", state_str)
            state_list = [int(str) for str in str_list]
            stset[set_name] = set(state_list)
        else:
            print(lineno, ":", set_def, "** incorrect")

def check_validity_of_set(name, the_set, lineno, rule):
    if name == "0": return
    if name and name[0] == "-":
        if name[1:] in the_set: return
    else:
        if name in the_set: return
    print("*** ERROR: undefined set name:", name)
    print("LINE", lineno, ":", rule)
    exit()

def rules(list_of_rules, verbosity):
    global trie, args, chset, stset
    lc, rc, sc, rs, mv, md = ('0', '0', '0', 1, 5, 1)
    pat = re.compile(
        r"""^(?P<x>(?:[^%;]|%[%;!nt])+) # x part
             ;\s                   # terminates the x part
             (?P<y>(?:[^%;]|%[%;!nt])*) # y part
             ;                     # terminates the y part
             (?:\s+
                (?P<lc> -? [^( ]+))?  # lc
             (?:\s+
                (?P<rc> -? [^( ]+))?  # rc
             (?:\s+
                (?P<sc> -? [^( ]+))?  # sc
             (?:\s+
                (?P<rs> -? \d+))?  # rs
             (?:\s+
                (?P<mv> \d+))?     # mv
             (?:\s+
                (?P<md>\d+))?      # md
             \s*
             (?:  [(]  .*  [)]  )?  # comment in round parentheses
             \s*
           $""",
        re.X)
    for lineno, rule in list_of_rules:
        mat = pat.match(rule)
        if mat:
            gd = mat.groupdict()
            if verbosity >= 20:
                print(gd)
            if gd['x']:
                x = decode_quoted(gd['x'])
            else:
                print("** no valid x part on line", linenum, line)
                exit()
            if gd['y'] or gd['y'] == "":
                y = decode_quoted(gd['y'])
            else:
                print("** no valid y part on line", linenum, line)
                exit()
            if gd['lc']:
                lc = gd['lc']
                check_validity_of_set(lc, chset, lineno, rule)
            if gd['rc']:
                rc = gd['rc']
                check_validity_of_set(rc, chset, lineno, rule)
            if gd['sc']:
                sc = gd['sc']
                check_validity_of_set(sc, stset, lineno, rule)
            if gd['rs']:
                rs = int(gd['rs'])
            if gd['mv']:
                mv = int(gd['mv'])
            if gd['md']:
                md = int(gd['md'])

            new_rule = (y, lc, rc, sc, rs, mv, md)
            if verbosity >= 20:
                print("new rule:", x, new_rule)
            if x in trie:
                list_of_rules = trie[x]
                if verbosity >= 20:
                    print("trie[x]", x, list_of_rules)
            else:
                list_of_rules = []
            list_of_rules.append(tuple(new_rule))
            # print("list_of_rules:", list_of_rules) ##
            trie[x] = list_of_rules
        else:
            print("error on line", lineno, rule)
    return

def read_beta_grammar(file_name, verbosity):
    global chset, stset, trie
    f = open(file_name, 'r')
    list_of_char_sets = []
    list_of_state_sets = []
    list_of_rules = []
    state = "start"
    lineno = 0
    for line in f:
        line = line.rstrip()
        lineno += 1
        # print(lineno, state, ">>" + line + "<<") ##
        if len(line) == 0 or line[0] == '!':
            continue
        if state == "start" and line == "CHARACTER-SETS":
            state = "chsets"
            continue
        elif state in {"start", "chsets"} and line == "STATE-SETS":
            state = "stsets"
            continue
        elif state in {"start", "chsets", "stsets"} and line == "RULES":
            state = "rules"
            continue
        elif state == "chsets":
            list_of_char_sets.append((lineno, line))
            # print(list_of_char_sets)
        elif state == "stsets":
            list_of_state_sets.append((lineno, line))
        elif state == "rules":
            list_of_rules.append((lineno, line))
        else:
            print("*** missing keyword on line", lineno)
            print(line)
            exit()
    # print("-- parsing character sets") ##
    character_sets(list_of_char_sets, verbosity)
    if verbosity >= 10:
        print(chset)
    # print("parsing state sets")
    state_sets(list_of_state_sets, verbosity)
    if verbosity >= 10:
        print(stset)
    # print("-- parsing rules")
    rules(list_of_rules, verbosity)
    
def testing(verbosity):
    character_sets(
        'V: a e i o u y ä ö',
        'C: d f g h j k l m n p r s t v'
    )
    #state_sets('MID: 2 3')
    rules(
        "i; j; V V 0",
        "i; ö; C V",
        "i; ii; C C",
        "iiii; ii; 0 0",
        "c; k; "
    )
    if verbosity > 10:
        print(chset)
        for item in trie.items(''):
            print(item)
    return

if __name__ == "__main__":
    import argparse, sys
    arpar = argparse.ArgumentParser("python3 beta.py # version 0.5.2")
    arpar.add_argument("rules", help="the name of the beta rule grammar file")
    arpar.add_argument("-i", "--input",
                        help="file from which input is read if not stdin",
                        default="")
    arpar.add_argument("-o", "--output",
                            help="file to which output is written if not stdout",
                            default="")
    arpar.add_argument("-v", "--verbosity",
                       help="level of diagnostic output",
                       type=int, default=0)
    arpar.add_argument("-m", "--max-loops",
                       help="maximum number of cycles per one input line",
                       type=int, default=10000)
    args = arpar.parse_args()

    if args.output:
        output_file = open(args.output, "w")
    else:
        output_file = sys.stdout
    if args.input:
        input_file = open(args.input, "r")
    else:
        input_file = sys.stdin

    read_beta_grammar(args.rules, args.verbosity)
    if "LIMITOR" not in chset:
        chset["LIMITOR"] = {' '}
    lim_expr = "[" + "".join(["\\" + s if s in {'-', ']'} else s
                                  for s in chset["LIMITOR"]]) + "]+"
    #print("LIMITOR splitting expr:", lim_expr)###
    buffer = ""
    for line in input_file:
        if line == "##\n" and args.verbosity in {0,1}:
            args.verbosity = 1-args.verbosity
            if args.verbosity == 1:
                print("    Trace now ON")
            else:
                print("    Trace now OFF")
            continue
        if ' ' in chset["LIMITOR"]:
            wdlist = re.split(r"\s+", line.strip())
            for word in wdlist:
                betaproc(word, args.max_loops, args.verbosity, output_file)        
        elif '#' in chset["LIMITOR"]:
            betaproc(line[:-1], args.max_loops, args.verbosity, output_file)
        else:
            if line[-1] == "\n":
                buffer = buffer + " " + line[:-1]
            else:
                buffer = buffer + " " + line
            while True:
                lst = re.split(lim_expr, buffer, maxsplit=1)
                if len(lst) == 1:
                    break
                lgth = len(lst[0]) + 1
                left_part = buffer[:lgth]
                right_part = buffer[lgth:]
                betaproc(left_part, args.max_loops, args.verbosity, output_file)
                buffer = right_part
    if buffer:
        betaproc(buffer, args.max_loops, args.verbosity, output_file)
