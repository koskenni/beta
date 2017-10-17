# beta.py
#
# Copyright 2017 by Kimmo Koskenniemi
#
# Reimplementation of the Beta string rewriting engine originally
# written by Benny Brodda in Fortran and later on reimplemented by
# Kimmo Koskenniemi in Pascal and in C.
# The input formalism follows the C version as documented in
# F. Karlsson and K. Koskenniemi, "Beta-ohjelma kielentutkimuksen apuvälineenä",
# Yliopistopaino, 1990.
#
# This program was written from scratch in Python3 without any
# reference to the above mentioned predecessors.
#
# This program is free software under the GPL 3 license
# Version 0.1 - 2017-04-26
#       0.1.1 - 2017-04-27
#         0.2 - 2017-10-17 : LIMITOR and BLANK implemented
#
from collections import deque
import string
import datrie

euroletters = "´áÁćĆéÉíÍĺĹńŃóÓŕŔśŚúÚẃẂýÝźŹǽǼǿǾǻǺ˘ăĂĕĔğĞĭĬŏŎŭŬˇǎǍčČďĎěĚǧǦȟȞǐǏǩǨľĽňŇǒǑřŘšŠťŤǔǓžŽǯǮ¸çÇģĢķĶļĻņŅŗŖşŞţŢâÂĉĈêÊĝĜĥĤîÎĵĴôÔŝŜûÛŵŴŷŶ¨äÄëËïÏöÖüÜẅẄÿŸ˙ḃḂċĊḋḊėĖḟḞġĠİṁṀṗṖṡṠṫṪżŻạẠẹẸịỊọỌụỤỵỴ˝őŐűŰàÀèÈìÌòÒùÙẁẀỳỲ¯āĀēĒīĪōŌūŪǣǢǟǞ˛ąĄęĘįĮǫǪųŲ˚åÅůŮãÃẽẼĩĨñÑõÕũŨỹỸđĐǥǤħĦłŁøØŧŦắặằẳẵẮẶẰẲẴấậầẩẫẤẬẦẨẪếệềểễỆỆỀỂỄốộồổỗỐỘỒỔỖǟǞȧǡȦǠảẢẻẺỉỈỏỎủỦỷỶơớợờờỡƠỚỢỜỞỠưứựừửữƯỨỰỪỬỮǭǬǻǺƒﬁﬂĳĲŀĿŉɼſẛẛșȘțȚ"

characters = string.printable + euroletters
allowed_characters = set(characters)

trie = datrie.Trie(characters)
chset = {}
stset = {}

def betaproc(line, max_cycles, verbosity):
    global trie, chset, stset
    cycles = 0
    items = deque()
    item = ("##", line + "##", 1)
    item_set = {item}
    items.appendleft(item)
    while len(items) > 0:                              # item loop
        cycles += 1
        if cycles > max_cycles:
            print("** possibly an infinite loop, stopped at", max_cycles)
            return
        left, right, state = items.pop()
        if verbosity > 0:
            print(left + " >>> " + right + " -- " + str(state))
        if len(right) <= 1 and len(left) >= 2:
            print(left[2:-1])
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
                    left1 = "##"
                    right1 = left[2:] + y + right[len(x):]
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
                    print(left1[2:-2])

                if ns < 0:              # neg rs increments
                    ns = state - ns
                elif ns == 0:           # zero rs keeps the state
                    ns = state

                if len(left1) >= 2 and len(right1) >= 2:
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

def character_sets(list_of_set_defs, verbosity):
    global chset, args
    for lineno, set_def in list_of_set_defs:
        if verbosity >= 20:
            print(lineno, ">>>" + set_def + "<<<") ##
        mat = re.match(r"^\s*([-#*\w]+):\s+(.+)\s*$", set_def)
        if mat:
            set_name = mat.group(1)
            symbol_str = mat.group(2)
            symbol_list = re.split(r"\s+", symbol_str)
            symbol_list = [' ' if x == "BLANK" else x for x in symbol_list]
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

def rules(list_of_rules, verbosity):
    global trie, args
    lc, rc, sc, rs, mv, md = ('0', '0', '0', 1, 5, 1)
    pat = re.compile(
        r"""^(?P<x>(?:[^;]|%[%;])+) # x part
             ;\s                   # terminates the x part
             (?P<y>(?:[^%;]|%[%;])*) # y part
             ;                     # terminates the y part
             (?:\s+
                (?P<lc> -? [-*\w]+))?  # lc
             (?:\s+
                (?P<rc> -? [-*\w]+))?  # rc
             (?:\s+
                (?P<sc> -? [-*\w]+))?  # sc
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
                x = gd['x']
            else:
                print("** no valid x part on line", linenum, line)
                exit()
            if gd['y'] or gd['y'] == "":
                y = gd['y']
            else:
                print("** no valid y part on line", linenum, line)
                exit()
            if gd['lc']:
                lc = gd['lc']
            if gd['rc']:
                rc = gd['rc']
            if gd['sc']:
                sc = gd['sc']
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
    state = "start"
    lineno = 0
    for line in f:
        line = line.rstrip()
        lineno += 1
        # print(lineno, state, ">>" + line + "<<") ##
        if len(line) == 0 or line[0] == '!':
            continue
        if state == "start" and line == "CHARACTER-SETS":
            list_of_char_sets = []
            state = "chsets"
            continue
        elif state in {"start", "chsets"} and line == "STATE-SETS":
            list_of_state_sets = []
            state = "stsets"
            continue
        elif state in {"start", "chsets", "stsets"} and line == "RULES":
            list_of_rules = []
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
    
def testing():
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
    if args.verbosity > 10:
        print(chset)
        for item in trie.items(''):
            print(item)
    return

if __name__ == "__main__":
    import argparse
    arpar = argparse.ArgumentParser("python3 beta.py")
    arpar.add_argument("-v", "--verbosity",
                       help="level of diagnostic output",
                       type=int, default=0)
    arpar.add_argument("-m", "--max_loops",
                       help="maximum number of cycles per one input line",
                       type=int, default=1000)
    arpar.add_argument("-r", "--rules", help="rule file")
    args = arpar.parse_args()

    read_beta_grammar(args.rules, args.verbosity)
    if "LIMITOR" not in chset:
        chset["LIMITOR"] = {' '}
    import sys
    for line in sys.stdin:
        if ' ' in chset["LIMITOR"]:
            wdlist = re.split(r"\s+", line.strip())
            for word in wdlist:
                betaproc(word, args.max_loops, args.verbosity)        
        else:
            betaproc(line[:-1], args.max_loops, args.verbosity)

