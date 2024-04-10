import pycparser
import platform
import os
from pycparser import c_parser, c_generator
import pandas as pd
import tensorflow as tf

gpu_token = tf.test.is_gpu_available('GPU')

def file_init(gpu_token):
    if platform.machine() == 'x86_64':
        if gpu_token:
            os.chdir('/home/ucdasec/Faulthunter-RNN-approach/manual_dataset')
        else:
            os.chdir("/home/sakshmeno/Documents/GitHub/C-RNN-approach/manual_dataset")
    elif platform.machine() == 'arm64':
        os.chdir("/Users/saksh.menon/Documents/GitHub/C-RNN-approach/manual_dataset")

    text=[]
    with open('saksh_branch_simple_insecure.c') as obj:
        temp = obj.read()
        obj.seek(0)
        while obj.tell()!=len(temp):
            try:
                line = obj.readline()
                if line.__contains__("#include"):
                    pass
                else:
                    text.append(line)
            except EOFError:
                break

    text = "".join(text)
    return text

#file constants

NODE_LIST = []
HAMMING_WEIGHT = 4
parser = c_parser.CParser()
generator = c_generator.CGenerator()
ast = parser.parse(file_init(gpu_token), filename='??.c')
explore = {pycparser.c_ast.If: {'node': (),'key': 'cond', 'branches': ('iftrue', 'iffalse')}, 
                    pycparser.c_ast.FuncCall: {'node': (),'key' : 'name' , 'branches': ()},
                    pycparser.c_ast.FuncDef: {'node': (),'key' : 'decl', 'branches': ('body',)},
                    pycparser.c_ast.FileAST: {'node': (),'key' : 'ext[0]', 'branches': ()}
                    } 
                    #    pycparser.c_ast.Switch: (),
                    #    pycparser.c_ast.For: ()}



def walk(parent_ast):
    if parent_ast.children():
        sub_ast = parent_ast.children()
        # if sub_ast[0][1].decl.name == 'main' and not(flag):
        #     walk(sub_ast[0][1], flag = 1)
        for node in sub_ast:
            if type(node[1]) in list(explore.keys()):
                node_attrs = list((explore[type(node[1])]['key'],) + explore[type(node[1])]['branches'])
                node_attr = {i: False for i in node_attrs}
                for sub_node in node[1].children():
                    node_attr[sub_node[0]] = sub_node
                node_attr['node'] = ('node', node[1],)

                print(type(node[1]), end = " : ")
                print(node_attr[explore[type(node[1])]['key']])
                NODE_LIST.append([('type',type(node_attr['node'][1])), node_attr[explore[type(node[1])]['key']], node_attr['node']])
                for sub_node in explore[type(node[1])]['branches']:
                    print(sub_node, " : {}".format(type(node_attr[sub_node][1].block_items[0]) if node_attr[sub_node] else node_attr[sub_node]))
                    if  node_attr[sub_node]:
                        walk(node_attr[sub_node][1])
            # elif (type(node[1]) == pycparser.c_ast.FuncCall):  

            else:
                print(type(node[1]))
                NODE_LIST.append([('type', type(node[1])), ('key', False), ('node', node[1])])
        
def start_end(text):
    START = 0
    for i in NODE_LIST:
        if i[1][1]:
            line = ((generator.visit(i[1][1])))
        else:
            line = ((generator.visit(i[2][1])))
        start = text.find(line, START)
        end = len(line) + start
        i.append((start,end))
        START=end

def w2b_dataframe_init(text):
    dataframe = pd.DataFrame(columns=['Type', 'Generated Line', 'Line', '(start, end)', 'Node', 'Encoded Line'])

    for i in NODE_LIST:
        row = {'Type': None, 'Generated Line': None, 'Line' : None, '(start, end)' : None, 'Node': None, 'Encoded Line' : None}
        #type
        row['Type'] = i[0][1]

        #generated line
        if i[1][1]:
            row['Generated Line'] = (generator.visit(i[1][1]))
        else:
            row['Generated Line'] = (generator.visit(i[2][1]))

        #line
        row['Line'] = text[i[3][0] : i[3][1]]

        #start, end
        row['(start, end)'] = (i[3])

        #node
        row['Node'] = i[2]
        dataframe.loc[len(dataframe)] = row

    return dataframe

def w2b_dataframe_encoding(dataframe):
    for i in dataframe.iloc():
        line = []
        if i.Type == pycparser.c_ast.If:
            line.append('0')
            node = i.Node[1]
            if type(node.cond.left) == pycparser.c_ast.Constant:
                value = int(node.cond.left.value)
            elif type(node.cond.right) == pycparser.c_ast.Constant:
                value = int(node.cond.right.value)
            else:
                print("Error")
                break
            
            value = str(bin(value))[2:]
            line.extend(list('0'*(256 - len(value)) + value))

        else:
            line.append('1')
            line.extend(list('1'*256))

        line = [eval(i) for i in line]
        i['Encoded Line'] = line

def W2B_init():
    text = file_init(gpu_token)
    walk(ast)
    start_end(text)
    dataframe = dataframe_init(text)
    w2b_dataframe_encoding(dataframe)
    return dataframe