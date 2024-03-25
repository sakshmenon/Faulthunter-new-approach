import pandas as pd
import os
import platform

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
    with open(file) as dataset_obj:
        codeLines = dataset_obj.read()
    comment_lines = []
    raw_codeLines = codeLines.replace("\t","").split("\n")
    multi_line_flag = 0
    for line_number in range(len(raw_codeLines)):
        if multi_line_flag:
            if raw_codeLines[line_number].__contains__("*/"):
                multi_line_flag = 0
            comment_lines.append(line_number)
        elif raw_codeLines[line_number].__contains__("/*"):
            if raw_codeLines[line_number].startswith("/*") and not(raw_codeLines[line_number].__contains__("*/")):
                comment_lines.append(line_number)
                multi_line_flag = 1
            elif raw_codeLines[line_number].__contains__("/*") and not(raw_codeLines[line_number].startswith("/*")):
                if raw_codeLines[line_number].__contains__("*/"):
                    psuedo_multi_line_start = raw_codeLines[line_number].find("/*")
                    psuedo_multi_line_end = raw_codeLines[line_number].find("*/")
                    temporary_line = raw_codeLines[line_number][:psuedo_multi_line_start] + raw_codeLines[line_number][psuedo_multi_line_end+2:]
                    raw_codeLines[line_number] = temporary_line

        elif raw_codeLines[line_number].startswith("//"):
            comment_lines.append(line_number)
        elif raw_codeLines[line_number].__contains__("//"):
            comment_start = raw_codeLines[line_number].find('//')
            raw_codeLines[line_number] = raw_codeLines[line_number][:comment_start]
    
    

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
        placeHolder = raw_codeLines[line_number]
        placeHolder = space_out(placeHolder, ";")
        placeHolder = space_out(placeHolder, "(")
        placeHolder = space_out(placeHolder, ")")
        placeHolder = space_out(placeHolder, ",")
        if placeHolder.endswith(";"):
            raw_codeLines[line_number] = "<start> " + placeHolder.replace(";","<end>")
        elif not(placeHolder.endswith(";")):
            raw_codeLines[line_number] = "<start> " + placeHolder + " <end>"

    return raw_codeLines

def comment_finder(file):
    with open(file) as dataset_obj:
        codeLines = dataset_obj.read()
        comment_lines = []
        raw_codeLines = codeLines.replace("\t","").split("\n")
        multi_line_flag = 0
        for line_number in range(len(raw_codeLines)):
            if multi_line_flag:
                if raw_codeLines[line_number].__contains__("*/"):
                    multi_line_flag = 0
                comment_lines.append(line_number)
            elif raw_codeLines[line_number].__contains__("/*"):
                if raw_codeLines[line_number].startswith("/*") and not(raw_codeLines[line_number].__contains__("*/")):
                    comment_lines.append(line_number)
                    multi_line_flag = 1
                elif raw_codeLines[line_number].__contains__("/*") and not(raw_codeLines[line_number].startswith("/*")):
                    if raw_codeLines[line_number].__contains__("*/"):
                        psuedo_multi_line_start = raw_codeLines[line_number].find("/*")
                        psuedo_multi_line_end = raw_codeLines[line_number].find("*/")
                        temporary_line = raw_codeLines[line_number][:psuedo_multi_line_start] + raw_codeLines[line_number][psuedo_multi_line_end+2:]
                        raw_codeLines[line_number] = temporary_line

            elif raw_codeLines[line_number].startswith("//"):
                comment_lines.append(line_number)
            elif raw_codeLines[line_number].__contains__("//"):
                comment_start = raw_codeLines[line_number].find('//')
                raw_codeLines[line_number] = raw_codeLines[line_number][:comment_start]
    return comment_lines

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
        comments = comment_finder(file)
        for vul_line in range(len(file_vulnerabilities[file])):
            for num in range(len(comments)):
                if num == len(comments)-1:
                    (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-(len(comments)))
                elif comments[num] < (file_vulnerabilities[file][vul_line]):
                    None
                elif comments[num] > (file_vulnerabilities[file][vul_line]):
                    (file_vulnerabilities[file][vul_line]) = ((file_vulnerabilities[file][vul_line])-(num+1))
                    break
    return file_vulnerabilities

def gen_df(file_list, file_vulnerabilities):
    labeled_dataset = {'Line Number':[], 'Lines':[], 'Label':[]}
    labeled_dataset = pd.DataFrame(labeled_dataset)
    labeled_dataset
    LINE_NUMBER = 0
    for file in file_list:
        code = code_preprocessing(file)
        for line in range(len(code)):
            if (line) in file_vulnerabilities[file]:
                data = {'Line Number': LINE_NUMBER, 'Lines': code[line], 'Label': 'Insecure'}
            else:
                data = {'Line Number': LINE_NUMBER, 'Lines': code[line], 'Label': 'Secure'}
            labeled_dataset.loc[len(labeled_dataset)] = data
            LINE_NUMBER+=1

    raw_code = list(labeled_dataset['Lines'])

    return labeled_dataset

def dataframe_init(gpu_token):
    dataframe = path_changes(gpu_token)
    file_list, file_vulnerabilities = vulnerable_line_finder(dataframe)
    file_vulnerabilities = vulnerable_line_adjustment(file_list, file_vulnerabilities, gpu_token)
    labelled_dataset = gen_df(file_list, file_vulnerabilities)
    labelled_dataset['Label']=labelled_dataset['Label'].map({"Secure" : 0, "Insecure": 1})
    return labelled_dataset
