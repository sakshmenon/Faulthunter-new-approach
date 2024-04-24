import os
import sys
sys.path.extend(['.', '..'])

os.chdir("/Users/saksh.menon/Documents/GitHub/C-RNN-approach")

from pycparser import c_parser, c_generator
import pycparser
from Utils.w2b_encoding_pt import *
from Utils.cparser_dataframe_gen import *

os.chdir("/Users/saksh.menon/Documents/GitHub/C-RNN-approach/dataset")

raw_code, comments = code_preprocessing('git 2.c') # remove comments
uvt, moded_code = find_undefined_types_in_variables(raw_code, gpu_token) # replacing undefined types in variables with 'int' 
uft, remoded_code = find_undefined_function_types(moded_code) # replacing undefined function types with 'int'

text = remoded_code.replace("  "," ").split('\n')
text = " ".join(text)
text

# text = remoded_code[152:]
parser = c_parser.CParser()
generator = c_generator.CGenerator()
ast = parser.parse(text, filename='??.c')
explore = {pycparser.c_ast.If: {'node': (),'key': 'cond', 'branches': ('iftrue', 'iffalse')}, 
                       pycparser.c_ast.FuncCall: {'node': (),'key' : 'name' , 'branches': ()},
                       pycparser.c_ast.FuncDef: {'node': (),'key' : 'decl', 'branches': ('body',)},
                       pycparser.c_ast.FileAST: {'node': (),'key' : 'ext[0]', 'branches': ()}
                       } 
                    #    pycparser.c_ast.Switch: (),
                    #    pycparser.c_ast.For: ()}

If_explore = {pycparser.c_ast.BinaryOp : {'branches': ('left', 'right')}}

HAMMING_WEIGHT = 4

print(ast)