import pandas as pd
import os
import platform
import re

def find_undefined_function_types(code_list):

    defined_types = set(['int', 'char', 'float', 'double', 'long', 'short', 'void'])
    undefined_types = set()
    
    # Regular expression pattern to match function declarations
    function_pattern = r'\b([a-zA-Z_]\w*\s*\**)\s+\w+\s*\([^)]*\)\s*{'
    
    temp_list = [i[1] for i in code_list]
    lines = "\n".join(temp_list)
    temp = lines
        # Find all function declarations in the content
    function_matches = re.findall(function_pattern, lines)
    # modified_lines = [lines]
    
    for return_type in function_matches:
        # Check if the return type is not in the set of defined types
        if return_type.strip('*') not in defined_types:
            undefined_types.add(return_type.strip('*'))

            temp = (temp.replace(return_type, 'int'))

    
    return list(undefined_types), temp

def find_undefined_types_in_variables(code_list, gpu_token):

    cpp_keywords = [
    "alignas",
    "alignof",
    "and",
    "and_eq",
    "asm",
    "auto",
    "bitand",
    "bitor",
    "bool",
    "break",
    "case",
    "catch",
    "char",
    "char16_t",
    "char32_t",
    "class",
    "compl",
    "const",
    "constexpr",
    "const_cast",
    "continue",
    "decltype",
    "default",
    "delete",
    "do",
    "double",
    "dynamic_cast",
    "else",
    "enum",
    "explicit",
    "export",
    "extern",
    "false",
    "float",
    "for",
    "friend",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "mutable",
    "namespace",
    "new",
    "noexcept",
    "not",
    "not_eq",
    "nullptr",
    "operator",
    "or",
    "or_eq",
    "private",
    "protected",
    "public",
    "register",
    "reinterpret_cast",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "static_assert",
    "static_cast",
    "struct",
    "switch",
    "template",
    "this",
    "thread_local",
    "throw",
    "true",
    "try",
    "typedef",
    "typeid",
    "typename",
    "union",
    "unsigned",
    "using",
    "virtual",
    "void",
    "volatile",
    "wchar_t",
    "while",
    "xor",
    "xor_eq",
    "%d",
    "%f",
    "%s"
]

    defined_types = {'int', 'char', 'float', 'double', 'long', 'short', 'void'}
    undefined_types = set()

    variable_pattern = r'\b((?:[a-zA-Z_]\w*\**)\s+\**\s*\**[a-zA-Z_]\w*\[*\w*\]*)\s*(?:,|\s*;|\s*=|\s*\))'

    for line in enumerate(code_list):
        # content = file.read()
        # Find all variable declarations in the content
        variable_matches = re.findall(variable_pattern, line[1][1])
        for variable_declaration in variable_matches:
            # Extract the data type from the variable declaration
            data_type = variable_declaration.split()[0]
            if data_type == 'd':
                # print(data_type)
                pass
            # Check if the data type is not in the set of defined types
            elif (data_type not in defined_types) and (data_type not in cpp_keywords):
                # print(variable_declaration.split()[0].replace(variable_declaration.split()[0], "int ") + variable_declaration.split()[1])

                undefined_types.add(data_type)
                code_list[line[0]][1] = (line[1][1].replace((variable_declaration.split()[0]+ ' '), 'int '))


    return list(undefined_types), code_list



def path_changes(gpu_token):
    if platform.machine() == 'arm64':
        pth = "/Users/saksh.menon/Documents/GitHub/C-RNN-approach/Labels/Labelling_Prateek_Guillermo.xlsx"
    elif platform.machine() == 'x86_64':
        if gpu_token:
            pth = "/home/ucdasec/Faulthunter-RNN-approach/Labels/Labelling_Prateek_Guillermo.xlsx"
        else:
            pth = "/home/sakshmeno/Documents/GitHub/C-RNN-approach/Labels/Labelling_Prateek_Guillermo.xlsx"
    dataframe = pd.read_excel(pth)
    return dataframe

def code_preprocessing(file):
    
    comment_lines, raw_codeLines = comment_finder(file)
    comment_lines.reverse()
    for i in comment_lines:
        raw_codeLines.pop(i)

    def insert_space(string, index):
        string_copy = ""
        for i in range(len(string)):
            if i==(index):
                string_copy += " "
                string_copy += string[i]
                string_copy += " "
                continue
            string_copy += string[i]
        return string_copy

    def find_char_indices(input_string, char):
        indices = []
        replacement_token = 0
        for index, character in enumerate(input_string):
            if character == char:
                indices.append(index + 2*replacement_token)
                replacement_token+=1
        return indices

    def space_out(string, char):
        indices = find_char_indices(string, char)

        for i in indices:
            string = insert_space(string, i)
        return string

    for line_number in range(len(raw_codeLines)):
            placeHolder = raw_codeLines[line_number][1]
            placeHolder = space_out(placeHolder, ";")
            placeHolder = space_out(placeHolder, "(")
            placeHolder = space_out(placeHolder, ")")
            placeHolder = space_out(placeHolder, ",")
            raw_codeLines[line_number][1] = placeHolder

    return raw_codeLines, comment_lines.reverse()

def comment_finder(file):
    with open(file) as dataset_obj:
        codeLines = dataset_obj.read()
        comment_lines = []
        raw_codeLines = codeLines.replace("\t","").split("\n")
        raw_codeLines = [[i, raw_codeLines[i]] for i in range(len(raw_codeLines))]
        multi_line_flag = 0
        for line_number in range(len(raw_codeLines)):
            if multi_line_flag:
                if raw_codeLines[line_number][1].__contains__("*/"):
                    multi_line_flag = 0
                comment_lines.append(line_number)
            elif  raw_codeLines[line_number][1].startswith("#"):
                comment_lines.append(line_number)
            elif raw_codeLines[line_number][1].__contains__("/*"):
                if raw_codeLines[line_number][1].lstrip(' ').startswith("/*") and not(raw_codeLines[line_number][1].__contains__("*/")):
                    comment_lines.append(line_number)
                    multi_line_flag = 1
                elif raw_codeLines[line_number][1].__contains__("/*") and not(raw_codeLines[line_number][1].lstrip(' ').startswith("/*")):
                    if raw_codeLines[line_number][1].__contains__("*/"):
                        psuedo_multi_line_start = raw_codeLines[line_number][1].find("/*")
                        psuedo_multi_line_end = raw_codeLines[line_number][1].find("*/")
                        temporary_line = raw_codeLines[line_number][1][:psuedo_multi_line_start] + raw_codeLines[line_number][1][psuedo_multi_line_end+2:]
                        raw_codeLines[line_number][1] = temporary_line
                elif raw_codeLines[line_number][1].__contains__("/*") and (raw_codeLines[line_number][1].lstrip(' ').startswith("/*")):
                    if raw_codeLines[line_number][1].__contains__("*/") and raw_codeLines[line_number][1].endswith("*/"):
                        comment_lines.append(line_number)

            elif raw_codeLines[line_number][1].lstrip(' ').startswith("//"):
                comment_lines.append(line_number)
            elif raw_codeLines[line_number][1].__contains__("//"):
                comment_start = raw_codeLines[line_number][1].find('//')
                raw_codeLines[line_number][1] = raw_codeLines[line_number][1][:comment_start]
    return comment_lines, raw_codeLines

def vulnerable_line_finder(df):
    file_start = {}
    for i in range(len(df['File'])):
        if pd.isnull(df['File'][i]) == False:
            file_start[df['File'][i]] = i

    BOTTOM_LINE = file_start['TOTAL NO. OF FILES']
    file_list = list(file_start.keys())[:-1]
    file_vulnerabilities = {}

    for i in range(len(file_list)-1):
        vulnerable_lines=[]
        for j in range(file_start[file_list[i]],file_start[file_list[i+1]]-1):
            if (df['Comment'][j].split('|')[1].split()[0]) == "BRANCH:":
                if (pd.isna(df.at[j,'False Positive'])):
                    line_number = int(df['Comment'][j].split('|')[0].split()[1])
                    vulnerable_lines.append([line_number,line_number])

            if (not(pd.isna(df.at[j,'Lines Missed']))):
                if (not(pd.isna(df.at[j,'Branch.1']))):
                    line = df['Lines Missed'][j].split()
                    if (not(line[0].isnumeric())):
                        line_number = int(line[1].strip(":"))
                        vulnerable_lines.append([line_number,line_number])
                    else:
                        line_number = int(line[0].strip(":"))
                        vulnerable_lines.append([line_number,line_number])
            
        vulnerable_lines.sort()

        file_vulnerabilities[file_list[i]]=vulnerable_lines

    file_list = file_list[:-1]
    return file_list, file_vulnerabilities

def vulnerable_line_adjustment(file_list, file_vulnerabilities, gpu_token):

    if platform.machine() == 'arm64':
        pth = "/Users/saksh.menon/Documents/GitHub/C-RNN-approach/dataset"
    elif platform.machine() == 'x86_64':
        if gpu_token:
            pth = "/home/ucdasec/Faulthunter-RNN-approach/dataset"
        else:
            pth = "/home/sakshmeno/Documents/GitHub/C-RNN-approach/dataset"

    os.chdir(pth)
    for file in file_list:
        comments, raw_code = comment_finder(file)
        # if file == 'SmartLock_HardwareDriver main.c':
        #     pass
        for vul_line in range(len(file_vulnerabilities[file])):
            # if vul_line == 84:
            #     pass
            if len(comments) == 0:
                (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-1) 
                continue
            for num in range(len(comments)):
                if num == len(comments)-1:
                    if comments[num] > file_vulnerabilities[file][vul_line]:
                        (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-(num+1)) #??
                    else:
                        (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-(len(comments)+1))
                elif comments[num] < (file_vulnerabilities[file][vul_line]):
                    None
                elif comments[num] > (file_vulnerabilities[file][vul_line]):
                    (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-(num+1)) #??
                    break
    return file_vulnerabilities

def gen_df(file_list, file_vulnerabilities):
    df_dict = {}
    for file in file_list:
        labeled_dataset = pd.DataFrame(columns=['File', 'Line Number', 'Lines', 'Original Line Number', '(start, end)', 'Label'])
        code, comments = code_preprocessing(file)
        # labeled_dataset = {'File': None, 'Line Number': None, 'Lines': None, 'Original Line Number': None, ('start, end'): None, 'Label':None}
        LINE_NUMBER = 0
        CHAR_SUM = 0
        with open(file) as raw_code_obj:
            raw_code = raw_code_obj.readlines()
        for line in range(len(code)):
            if code[line][1]:
                start = raw_code[code[line][0]].find(code[line][1]) + CHAR_SUM
                end = start + len(code[line][1])
                if (line) in file_vulnerabilities[file]:
                    data = {'File': file,'Line Number': LINE_NUMBER, 'Lines': code[line], 'Original Line Number': code[line][0], '(start, end)':  (start, end), 'Label': 'Insecure'}
                else:
                    data = {'File': file, 'Line Number': LINE_NUMBER, 'Lines': code[line], 'Original Line Number': code[line][0], '(start, end)':  (start, end), 'Label': 'Secure'}
                labeled_dataset.loc[len(labeled_dataset)] = data
                LINE_NUMBER+=1
                CHAR_SUM += len(raw_code[code[line][0]])
        df_dict[file] = labeled_dataset

    # raw_code = list(labeled_dataset['Lines'])

    return df_dict

def dataframe_init(gpu_token):
    dataframe = path_changes(gpu_token)
    file_list, file_vulnerabilities = vulnerable_line_finder(dataframe)
    file_vulnerabilities = vulnerable_line_adjustment(file_list, file_vulnerabilities, gpu_token)
    df_dictionary = gen_df(file_list, file_vulnerabilities)
    # labelled_dataset['Label']=labelled_dataset['Label'].map({"Secure" : 0, "Insecure": 1})
    return df_dictionary
