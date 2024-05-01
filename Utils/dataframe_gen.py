import pandas as pd
import os
import platform
import re
from pycparser import c_parser, c_generator
import pycparser

parser = c_parser.CParser()
DEF_DICT = {}
DEC_DICT = {}

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
        if placeHolder.endswith(";"):
            raw_codeLines[line_number][1] = "<start> " + placeHolder.replace(";","<end>")
        elif not(placeHolder.endswith(";")):
            raw_codeLines[line_number][1] = "<start> " + placeHolder + " <end>"

    return raw_codeLines

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
                    vulnerable_lines.append(int(df['Comment'][j].split('|')[0].split()[1]))
            if (not(pd.isna(df.at[j,'Lines Missed']))):
                if (not(pd.isna(df.at[j,'Branch.1']))):
                    line = df['Lines Missed'][j].split()
                    if (not(line[0].isnumeric())):
                        vulnerable_lines.append(int(line[1].strip(":")))
                    else:
                        vulnerable_lines.append(int(line[0].strip(":")))
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
        if file == 'SmartLock_HardwareDriver main.c':
            pass
        for vul_line in range(len(file_vulnerabilities[file])):
            if vul_line == 84:
                pass
            if len(comments) == 0:
                (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-1) #??
                # break
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

def cond_extract(else_flag, raw_line):
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
    return branch_line

def find_definition_statements(code):
    patterns = r'\w+\s*=\s*\d+'
    definition = []
    for line in code:
        matches = re.findall(patterns, line[1])
        if matches:
            definition.append([matches[0].split('=')[0],matches[0].split('=')[1]])
    return definition

def find_declaration_statements(code):
    variable_pattern = r'\b((?:[a-zA-Z_]\w*\**)\s+\**\s*\**[a-zA-Z_]\w*\[*\w*\]*)\s*(?:,|\s*;|\s*=|\s*\))'
    key_list = ['int', 'bool', 'char']
    declarations = []
    for line in code:
        statements = re.findall(variable_pattern, line[1])
        if statements:
            if statements[0].split()[0] in key_list:
                declarations.append([statements[0].split()[0],statements[0].split()[1]])
    return declarations

def gen_df(file_list, file_vulnerabilities):
    df_dict = {}
    labeled_dataset = pd.DataFrame(columns=['File', 'Line Number', 'Lines', 'Value', 'Original Line Number', 'Label'])
    LINE_NUMBER = 0
    for file in file_list:
        code = code_preprocessing(file)
        filewise_labeled_dataset = pd.DataFrame(columns=['File', 'Line Number', 'Lines', 'Value', 'Original Line Number', 'Label'])
        FILE_LINE_NUMBER = 0
        dec_matches = find_declaration_statements(code)
        def_matches = find_definition_statements(code)
        DEC_DICT[file] = dec_matches
        DEF_DICT[file] = def_matches
        for line in range(len(code)):
            if code[line][1]:
                if (line) in file_vulnerabilities[file]:
                    data = {'File': file,'Line Number': LINE_NUMBER, 'Lines': code[line][1], 'Value': "Not Defined",'Original Line Number': code[line][0], 'Label': 'Insecure'}
                else:
                    data = {'File': file, 'Line Number': LINE_NUMBER, 'Lines': code[line][1], 'Value': "Not Defined",'Original Line Number': code[line][0], 'Label': 'Secure'}
                labeled_dataset.loc[len(labeled_dataset)] = data
                filewise_labeled_dataset.loc[len(filewise_labeled_dataset)] = data
                LINE_NUMBER+=1
                FILE_LINE_NUMBER+=1
        df_dict[file] = filewise_labeled_dataset

    return labeled_dataset, df_dict

def dataframe_init(gpu_token):
    dataframe = path_changes(gpu_token)
    file_list, file_vulnerabilities = vulnerable_line_finder(dataframe)
    file_vulnerabilities = vulnerable_line_adjustment(file_list, file_vulnerabilities, gpu_token)
    labelled_dataset, df_dict = gen_df(file_list, file_vulnerabilities)
    labelled_dataset['Label']=labelled_dataset['Label'].map({"Secure" : 0, "Insecure": 1})
    return labelled_dataset, df_dict, DEF_DICT, DEC_DICT
