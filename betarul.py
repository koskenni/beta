#
# plytw.py
#
import re

tokens = (
     'CHARACTER', 'CHSETS', 'EOL', 'NAMECOLON', 'NUMBER',
     'RULES', 'SEMICOLON',
     # 'SPACE',
     'STSETS',
     'UPTOENDOFLINE', 'XYCHARACTER'
)

states = (('chs','exclusive'),
          ('sts','exclusive'),
          ('rul','exclusive'))

# Tokens

def t_chs_CHARACTER(t):
     r'\w|BLANK'
     if len(t.value) == 2:
          t.value = t.value[1:]
     elif t.value == 'BLANK':
          t.value = ' '
     print("CHARACTER", t.value)
     return(t)

#def t_COMMENT(t):
#    r'\!.*'
#    pass
#    # No return value. Token discarded

def t_CHSETS(t):
     r'CHARACTER-SETS'
     t.lexer.begin = 'chs'
     print("CHSETS", t.value)
     return(t)

def t_ANY_EOL(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    print("EOL", t.value)
    print("lineno", t.lexer.lineno)
    return(t)

def t_chs_sts_NAMECOLON(t):
     r'[Va-zåäöA-ZÅÄÖ0-9_]+:'
     #r'\w+:'
     t.value = t.value[:e-1]
     print("NAMECOLON", t.value)
     return(t)
     
def t_sts_NUMBER(t):
     r'[0-9]+'
     return(int(t.value))

def t_INITIAL_chs_sts_RULES(t):
     r'RULES'
     t.lexer.begin = 'rul'
     return(t)

t_rul_SEMICOLON = r'; '

#t_rul_SPACE = r'[ ]'

def t_INITIAL_chs_STSETS(t):
     r'STATE-SETS'
     t.lexer.begin = 'sts'
     return(t)

def t_rul_UPTOENDOFLINE(t):
     r'[^\n]+'
     print("UPTOENDOFLINE", t.value)
     return(t)

def t_rul_XYCHARACTER(t):
     r'%.\[^;\s\n]'
     if len(t.value) == 2:
          t.vallue = t.value[:-1]
     return(t)

# Ignored characters
t_ANY_ignore = " "

#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += t.value.count("\n")
    
def t_ANY_error(t):
    global input_lines 
    #print("Illegal character '%s'" % t.value[0])
    lno = t.lexer.lineno-1
    print(input_lines[lno])
    pos = t.lexpos
    skip = sum([len(input_lines[i])+1 for i in range(0, lno)])
    ###print("skip, pos", skip, pos, input_lines[lno])
    print(" "*(t.lexpos-1-skip), "*", "Illegal token", ">>>" + t.value[:2] + "<<<")
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex(debug=9)

# Parsing rules

precedence = (

)

import datrie
trie = datrie.Trie("abcdefghijklmnopqrstuvwxyz0123456789-_.:,;'!@#€$%&/|\()+")
chset = {}
stset = {}

#from beta import chset, stset, trie

verbosity_level = 0

def p_grammar(p):
    '''grammar : character_sets_part EOL state_sets_part EOL rules_part'''
    pass

def p_character_sets_part(p):
    '''character_sets_part : CHSETS EOL character_sets
                           | empty'''
    pass

def p_character_sets(p):
    '''character_sets : character_sets character_set
                      | empty'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_character_set(p):
    '''character_set : NAMECOLON characters EOL'''
    global chset
    chset[p[1]] = p[2]
    print("character set:", p[1], p[2])
    pass

def p_characters(p):
    '''characters :  CHARACTER
                  | characters CHARACTER'''
    if len(p) == 2:
         p[0] = p[1]
         p[0].add(p[2])
    else:
         p[0] = {p[1]}
    return(p[0])

def p_state_sets_part(p):
    '''state_sets_part : STSETS EOL state_sets'''
    pass

def p_state_sets(p):
    '''state_sets : state_sets state_set
                  | empty'''
    pass

def p_state_set(p):
    '''state_set : NAMECOLON numbers EOL'''
    stset[p[1]] = p[2]
    pass

def p_numbers(p):
    '''numbers : NUMBER
               | numbers NUMBER'''
    if len(p) == 1:
         p[0] = {p[1]}
    else:
         p[0] = p[1]
         p[0].add(p[2])
    return(p[0])

def p_rules_part(p):
    '''rules_part : RULES EOL rule_list'''
    pass

def p_rule_list(p):
    '''rule_list : rule
                 | rule_list rule'''
    pass

def p_rule(p):
    '''rule : xy_part xy_part parameters EOL'''
    global chset, stset, trie, default_param
    x = p[1]
    y = p[3]
    pars = p[5]
    pars[0:0] = [y]
    val = trie.setdefault(x, [])
    trie[x] = val.append(tuple(pars))
    pass

def p_xy_part(p):
    '''xy_part : xychars SEMICOLON'''
    p[0] = p[1]

def p_xychars(p):
    '''xychars : xychars XYCHARACTER
               | empty'''
    if len(p) == 1:
         p[0] = p[1]
    else:
         p[0] = p[1] + p[2]

def p_parameters(p):
    '''parameters : UPTOENDOFLINE'''
    p[0] = p[1]


input_lines = []

def print_error(p, explanation, sym):
    ###print(input_lines[p.lineno])
    print(" "*(p.lexpos(0)-1), "*", explanation, sym)

def p_error(t):
    global parser, input_lines
    if not t:
        # print('EOF') ##
        return
    print(input_lines[t.lineno])
    print(" "*(t.lexpos-1), "*",
          "Syntax error at '{}' in line {}".format(t.value, t.lineno))

import ply.yacc as yacc

def parse_rule(debugging):
    global parser, lines
    result = parser.parse(lines, tracking=True)
    return(result)

def init(verbosity, debugging): 
    global parser, verbosity_level
    global trie, chset, stset
    parser = yacc.yacc(debug=debugging)
    verbosity_level = verbosity
    return(parser)

if __name__ == "__main__":
    import argparse
    arpar = argparse.ArgumentParser("python3 betarul.py")
    arpar.add_argument("-e", "--examples", help="name of the examples file",
                       default="test.pairstr")
    arpar.add_argument("-r", "--rules", help="name of the rule file",
                       default="test1.beta")
    arpar.add_argument("-v", "--verbosity",
                       help="level of  diagnostic output",
                       type=int, default=0)
    arpar.add_argument("-d", "--debug",
                       help="level of PLY debugging output",
                       type=int, default=0)
    args = arpar.parse_args()

    # twex.read_examples(args.examples) ## read here if not already read
    # print(twex.symbol_pair_set) ##

    init(args.verbosity, args.debug)
    rule_file = open(args.rules, 'r')
    lines = rule_file.read()
    input_lines = lines.split("\n")
    #for line in input_lines:
    #     print('"' + line + '"')
    res = parse_rule(args.debug)

    print(chset)
    for item in trie.items(''):
         print(item)

