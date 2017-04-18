from collections import deque
import string
import datrie

trie = datrie.Trie(string.ascii_lowercase + "äö")
chset = {}
stset = {}

def betaproc(line, verbosity):
    global trie, chset, stset
    items = deque()
    items.appendleft(("##", line + "##", 0))
    while len(items) > 0:
        left, right, state = items.pop()
        if verbosity > 0:
            print(left + " >>> " + right + " -- " + str(state))
        if len(right) == 0 and len(left) > 0:
            print(left[2:-2])
            continue
        rule_items = trie.prefix_items(right)
        if verbosity > 11:
            print(rule_items)
        for x, rule_list in rule_items:
            for rule in rule_list:
                if verbosity > 10:
                    print("testing for", rule)
                y, lc, rc, sc, ns, mv, md = rule
                if lc != '0' and lc != '':
                    # print("testing that", left[-1], "is in", chset[lc]) ##
                    if left[-1] not in chset[lc]:
                        continue
                    else:
                        if verbosity > 10:
                            print("left conditon tested and satisfied")
                if rc != '0' and rc != '':
                    if right[len(x)] not in chset[rc]:
                        continue
                    else:
                        if verbosity > 10:
                            print("right conditon tested and satisfied")
                if sc != '0' and sc != '':
                    if state not in stsets[sc]:
                        continue
                    else:
                        if verbosity > 10:
                            print("state conditon tested and satisfied")
                if mv == 1:
                    left1 = ""
                    right1 = left + y + right[len(x):]
                elif mv == 2:
                    left1 = left[:-1]
                    right1 = left[-1:] + y + right[len(x):]
                elif mv == 3:
                    left1 = left
                    right1 = y + right[len(x):]
                elif mv == 4:
                    left1 = left + y[:-1]
                    right1 = y[-1] + y + right[len(x):]
                elif mv == 5:
                    left1 = left + y
                    right1 = right[len(x):]
                elif mv == 6:
                    left1 = left + y + right[len(x):]
                    right1 = ""
                items.appendleft((left1, right1, ns))
                if verbosity > 9:
                    print((left1, right1, ns), "pushed to the queue")
                if md != 2:
                    break
            else:
                continue
            break
        else:
            if len(right) > 0:
                left1 = left + right[0:1]
                right1 = right[1:]
                items.appendleft((left1, right1, state))
                if verbosity > 9:
                    print("shifting one step to the right")
    return

import re

def character_sets(*list_of_set_defs):
    global chset
    for set_def in list_of_set_defs:
        mat = re.match(r"^\s*(\w+):\s+(.+)\s*$", set_def)
        if mat:
            set_name = mat.group(1)
            symbol_str = mat.group(2)
            symbol_list = re.split(r"\s+", symbol_str)
            chset[set_name] = set(symbol_list)
        else:
            print(set_def, "** incorrect")

def rules(*list_of_rules):
    global trie
    par = [0, 0, 0, 0, 5, 1]
    for rule in list_of_rules:
        mat = re.match(r"^([^;]*); ([^;]*);(.*)$", rule)
        if mat:
            x = mat.group(1)
            y = mat.group(2)
            rest = mat.group(3).strip()
            # print("x:", x, "y:", y, "rest:", rest) ###
            lst = re.split(r"\s+", rest)
            par[0:len(lst)] = lst
            print("par: ", par)
            new_rule = [y]
            new_rule.extend(par)
            print("new rule:", new_rule)
            if x in trie:
                list_of_rules = trie[x]
                print("trie[x]", x, list_of_rules)
            else:
                list_of_rules = []
            list_of_rules.append(tuple(new_rule))
            print("list_of_rules:", list_of_rules)
            trie[x] = list_of_rules
        else:
            print("error in", rule)

if __name__ == "__main__":
    import argparse
    arpar = argparse.ArgumentParser("python3 beta.py")
    arpar.add_argument("-v", "--verbosity",
                       help="level of diagnostic output",
                       type=int, default=0)
    args = arpar.parse_args()

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

    import sys
    for line in sys.stdin:
        betaproc(line.strip(), args.verbosity)

