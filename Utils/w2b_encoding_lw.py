"""
parse through lines
if node: 0 + binary rep
else : 1, 1, 1, .......1, 1
"""
from pycparser import c_parser, c_generator
import pycparser
parser = c_parser.CParser()

IF_EXPLORE = {pycparser.c_ast.BinaryOp : {'key':(), 'branches': ('left', 'right')},
              pycparser.c_ast.UnaryOp : {'key': (), 'branches': ('expr')}}

HAMMING_WEIGHT = 20
def value_search(condition):
            if type(condition) in IF_EXPLORE.keys():
                branches = IF_EXPLORE[type(condition)]['branches']
                kids = {child[0]: child[1] for child in condition.children()}
                for branch in branches:
                    if type(kids[branch]) == pycparser.c_ast.Constant:
                        value = int(kids[branch].value)
                        return value
                    elif type(kids[branch]) in IF_EXPLORE.keys():
                        value_search(kids[branch])
            return None

def encoder(vectors):
    for vector in range(len(vectors)):
        for row in enumerate(vectors[vector]['Lines']):
            encodedline = ''
            raw_line = row[1][7:-5].lstrip().rstrip()
            if row[0] == 123:
                pass
            if raw_line.startswith('if'):
                p_c = 0
                flag = 0
                cond_flag = 0
                for i in enumerate(raw_line):
                    if i[1] == '(':
                        if flag == 0:
                            flag = 1
                        p_c+=1
                    elif i[1] == ')':
                        if flag == 1:
                            if p_c == 1:
                                cond_flag = 1
                        p_c -= 1
                    if cond_flag:
                        if_line = (raw_line[:i[0]+1])
                        break
                encodedline += '0'
                line = 'int main() { ' + if_line + ' {} return 0; }'
                value = 'none'
                try:
                    parent_node = parser.parse(line)
                    condition  = parent_node.children()[0][1].children()[1][1].children()[0][1].children()[0][1]
                    value = value_search(condition)
                    value = str(bin(value))[2:]
                    value = value.count('1')
                    value = 1 if value >= HAMMING_WEIGHT else 0
                    encodedline += ('0' + '0'*(256 - len(value)) + value)
                    vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                    continue

                except:
                    pass

                if type(value) == str or value == None:
                    encodedline += '0'*(257)
                    vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)

            else:
                encodedline += ('1'*258)
                vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
            if len(encodedline)>258:
                print('??')
    return vectors