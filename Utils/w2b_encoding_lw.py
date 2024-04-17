"""
parse through lines
if node: 0 + binary rep
else : 1, 1, 1, .......1, 1
"""
from pycparser import c_parser, c_generator
import pycparser
parser = c_parser.CParser()

IF_EXPLORE = {pycparser.c_ast.BinaryOp : {'key':(), 'branches': ('left', 'right')},
              pycparser.c_ast.UnaryOp : {'key': (), 'branches': ('expr',)}}

HAMMING_WEIGHT = 20
BOOL_DICT = {'true': True, 'false': False, 'null':  False}

RET_FLAG = 0
def value_search(condition, val_lists):
        if type(condition) in IF_EXPLORE.keys():
            branches = IF_EXPLORE[type(condition)]['branches']
            kids = {child[0]: child[1] for child in condition.children()}
            for branch in branches:
                if type(kids[branch]) in IF_EXPLORE.keys():
                    val_lists = value_search(kids[branch], val_lists)
                    # val_lists.append(value)
                elif type(kids[branch]) == pycparser.c_ast.Constant:
                    if kids[branch].value.startswith('0x'):
                        value = int(kids[branch].value, 16)
                    else:
                        value = int(kids[branch].value)
                    # return value
                    val_lists.append(value)
                elif type(kids[branch]) == pycparser.c_ast.ID:
                     if kids[branch].name.lower() in BOOL_DICT:
                          val_lists.append(int(BOOL_DICT[kids[branch].name.lower()]))
        return val_lists

def encoder(vectors):
    for vector in range(len(vectors)):
        for row in enumerate(vectors[vector]['Lines']):
            encodedline = ''
            if row[1][7:-5].lstrip().rstrip().startswith('}'):
                pass
            raw_line = row[1][7:-5].lstrip().rstrip().lstrip('}').lstrip()
            if raw_line.startswith('if') or raw_line.startswith('else') or raw_line.startswith('while'):
                else_flag = 0
                if raw_line.startswith('if'):
                    encodedline += '10'
                elif raw_line.startswith('else if'):
                    else_flag = 4
                    encodedline += '10'
                elif  raw_line.startswith('while'):
                    encodedline += '01'
                else:
                    encodedline += '00'

                p_c = 0
                flag = 0
                cond_flag = 0
                branch_line = ''
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
                        branch_line = (raw_line[else_flag:i[0]+1])
                        break
                # encodedline += '0'
                line = 'int main() { ' + branch_line + ' {} return 0; }'
                value = 'none'
                # encodedline += '1'
                # vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]
                # vectors[vector]['Label'][row[0]] = 0
                # continue
                try:
                    parent_node = parser.parse(line)
                    condition  = parent_node.children()[0][1].children()[1][1].children()[0][1].children()[0][1]
                    value = value_search(condition, [])[0]
                    value = str(bin(value))[2:]
                    # value = value.count('1')
                    # value = 1 if value <= HAMMING_WEIGHT else 0
                    encodedline += (str(value) + '0'*(30-len(str(value))))
                    # encodedline += ('0' + '0'*(256 - len(value)) + value)
                    vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                    continue

                except:
                    pass

                if type(value) == str or value == None:
                    # encodedline += '0'*(257)
                    encodedline += '0*30'
                    vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                    print(encodedline)

            else:
                encodedline += ('0'*32)
                vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                # vectors[vector]['Label'][row[0]] = 1
            if len(encodedline)>258:
                print('??')
    return vectors