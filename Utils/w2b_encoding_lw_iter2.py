"""
parse through lines
if node: 0 + binary rep
else : 1, 1, 1, .......1, 1
"""
from pycparser import c_parser, c_generator
import pycparser
parser = c_parser.CParser()

IF_EXPLORE = {pycparser.c_ast.BinaryOp : {'key':[], 'branches': ('left', 'right')},
              pycparser.c_ast.UnaryOp : {'key': (), 'branches': ('expr',)},
              pycparser.c_ast.ID : {'key': (), 'branches': ()}}

HAMMING_WEIGHT = 20
BOOL_DICT = {'true': True, 'false': False}
OP_FILTER = ['>','<','==','<=','>=', '!=','||','&&']
RET_FLAG = 0
def value_search(condition, val_lists, depth):
    depth += 1
    if type(condition) in IF_EXPLORE.keys():
        branches = IF_EXPLORE[type(condition)]['branches']
        key = IF_EXPLORE[type(condition)]['key']
        kids = {child[0]: child[1] for child in condition.children()}
        key = condition.op
        if key in OP_FILTER:
            pass
        else:
            return val_lists
        for branch in branches:
            if type(kids[branch]) == pycparser.c_ast.ID:
                if kids[branch].name.lower() in BOOL_DICT:
                    val_lists.append(int(BOOL_DICT[kids[branch].name.lower()]))
            elif type(kids[branch]) in IF_EXPLORE.keys():
                val_lists = value_search(kids[branch], val_lists, depth)
                # val_lists.append(value)
            elif type(kids[branch]) == pycparser.c_ast.Constant:
                if kids[branch].value.startswith('0x'):
                    value = int(kids[branch].value, 16)
                else:
                    value = int(kids[branch].value)
                # return value
                val_lists.append(value)

        return val_lists

def encoder2(vectors):
    for vector in range(len(vectors)):
        for row in enumerate(vectors[vector]['Lines']):
            encodedline = ''
            if row[1][7:-5].lstrip().rstrip().startswith('}'):
                pass
            raw_line = row[1][7:-5].lstrip().rstrip().lstrip('}').lstrip()
            if raw_line.startswith('if') or raw_line.startswith('else'):
                else_flag = 0
                if raw_line.startswith('if'):
                    encodedline += '1'
                elif raw_line.startswith('else if'):
                    else_flag = 4
                    encodedline += '1'

                else:
                    encodedline += '0'

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
                    # if type(condition) == pycparser.c_ast.ID:
                    #     value = 1
                    # else:
                    value = value_search(condition, [], 0)[0]
                    value = str(bin(value))[2:]
                    value = value.count('1')
                    value = 1 if value <= HAMMING_WEIGHT else 0
                    encodedline += str(value) 
                    # encodedline += ('0' + '0'*(256 - len(value)) + value)
                    vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                    continue

                except:
                    pass

                if type(value) == str or value == None:
                    # encodedline += '0'*(257)
                    encodedline += '0'
                    vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                    # print(encodedline)

            else:
                encodedline += ('0'*2)
                vectors[vector]['Encoded Lines'][row[0]] = [eval(i) for i in encodedline]#tuple(encodedline)
                # vectors[vector]['Label'][row[0]] = 1
            if len(encodedline)>258:
                print('??')
    return vectors