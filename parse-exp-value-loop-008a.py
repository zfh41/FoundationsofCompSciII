'''
This program implements a recursive descent parser for the CFG below:

Syntax Rule  Lookahead Set          Strings generated
------------------------------------------------------------
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → (<exp>) | <number>
'''
import math

class ParseError(Exception): pass




#==============================================================
# FRONT END PARSER
#==============================================================

i = 0 # keeps track of what character we are currently reading.
err = None
d = {}

#---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err
 
    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value
#---------------------------------------
# Parse a Term   <term> → <factor>{*<factor> | /<factor>}
#
def term():
    global i, err
    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
#---------------------------------------
# Parse a Factor   <factor> → (<exp>) | <number> | pi | <func>(<exp>)
#       
def factor():
    global i, err
    value = None
    if w[i] == '(':
        i += 1       # read the next character
        value = exp()
        if w[i] == ')':
            i += 1
            return value
        else:
            print('missing )')
            raise ParseError
    elif w[i] == 'pi':
        i += 1
        return math.pi
    elif w[i] in ['sin', 'cos', 'tan', 'sqrt']:
        funcname = w[i]
        i+=1
        if w[i] == '(':
            i+=1
            express = exp()
            value = func(funcname,express)
#            print(w[i])
            if w[i] == ')':
                i+=1
                return value
            else:
                print('missing )')
                raise ParseError
        else:
            print('missing (')
            raise ParseError
    else:
#        print(w[i])
        try:
            if (w[i].isalpha()):
                value = atomic(d[w[i]])
                i+=1
            else:
                value = atomic(w[i])
                i += 1          # read the next character
        except ValueError:
            print('number expected')
            value = None
    
    #print('factor returning', value)
    
    if value == None: raise ParseError
    
    return value

#------------------------------------------
# Parse a Function   <func> -> sin | cos | tan | sqrt

def func(funcname,x):
    if funcname == 'sin':
        return math.sin(x)
    elif funcname == 'cos':
        return math.cos(x)
    elif funcname == 'tan':
        return math.tan(x)
    elif funcname == 'sqrt':
        return math.sqrt(x)
        

#------------------------------------------
# Parse a Statement  <statement> → table | show <exp>{,<exp>} | <id> = <exp>
#

def statement():
    global i, err
    if w[i] == 'table':
        print("\nSymbol Table\n")
        print("===================\n")
        for i in d:
            print(i + "     "  + str(d[i]) + "\n")
    elif w[i] == 'show':
        i+=1
        value = exp()
        print("value:  "  + str(value), end = "    ")
        while w[i] == ',':
            i+=1
            value=exp()
            print(str(value), end = "    ")
        print("\nDone")
    else:
        if (w[i].isalpha()):
            identifier = w[i]
            i+=1
            if w[i] == '=':
                i+=1
                expres = exp()
                d[identifier]=expres
                print("Done")
                
#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================

def binary_op(op, lhs, rhs):
    if op == '+': return lhs + rhs
    elif op == '-': return lhs - rhs
    elif op == '*': return lhs * rhs
    elif op == '/': return lhs / rhs
    else: return None

def atomic(x):
    return float(x)



w = input('=> ')
while w != '':
    #------------------------------
    # Split string into token list.
    #
    for c in '()+-*/,=':
        w = w.replace(c, ' '+c+' ')
    w = w.split()
    w.append('$') # EOF marker

    i = 0

    try:
        statement() # call the parser
    except:
        print('parse error')

    w = input('=> ')

