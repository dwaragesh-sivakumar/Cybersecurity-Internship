# Python Variable Collector Program
# The purpose of the program is:
# 1. Ask for user input to get a path
# 2. Take the path and use it to accumulate all TPL or all PHP files
# 3. Go through all the conditions that are available to extract all the defined variables from TPL/PHp files
# 4. Output as a separate TXT file for each type of document

import os
import pprint
import sys

# user input that allows any type of file to be used (web applications)
# in order to figure out what types of variables are used
# and where they are used
user_name = input("Please enter your user_name:\n")
extract_location = input("Please enter the location of where the file is extracted: \n")
library = input("Please enter your web application master folder name:\n")
sub_library = input("Please enter your web application sub folder name:\n")
tpl_php = input("Please enter whether you wanted to access tpl files or php files:\n")


# function that helps configure the path that you are looking your web application at
def find_path(user_name, extract_location, library, sub_library, tpl_php):
    path = "C:\\Users\\{}\\{}\\{}\\{}\\{}".format(user_name, extract_location, library, sub_library, tpl_php)
    return path


# Prompt for the path
print("\n")
print("Your path is:", find_path(user_name, extract_location, library, sub_library, tpl_php))
print("\n")


# Accumulate all tpl files
def get_all_tpl_files(dirpath):
    tpl_files = []
    if dirpath[-4:] == ".tpl":
        return [dirpath]
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file[-4:] == ".tpl":
                tpl_files.append(os.path.join(root, file))
    return tpl_files


# Accumulating all php files
def get_all_php_files(directory_path):
    php_files = []
    if directory_path[-4:] == ".php":
        return [directory_path]
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file[-4:] == ".php":
                php_files.append(os.path.join(root, file))
    return php_files


if tpl_php == "templates":
    # Open a tpl file (for testing purposes)
    sys.stdout = open("tpl.txt", "w")
    # call to get all the tpl files
    tpl_files = get_all_tpl_files(find_path(user_name, extract_location, library, sub_library, tpl_php))

    for tpl_file in tpl_files:
        print("\n")
        print(tpl_file)
        f = open(tpl_file)

        tpl_code_array = f.readlines()
        tpl_variable_names_array = []
        tpl_output = []

        # make a list that shows all usage of variables in code
        # determined based on length, the initiation on '$' symbol and figures where all tpl files end
        for line in tpl_code_array:
            length = len(line)
            index = line.find("$")
            if index != -1:
                tpl_output.append(line)

        # make a list with only variables
        for lines in tpl_output:
            location = lines.find("$")
            while location != -1:
                variable = ""
                variable += "$"
                for index in range(location + 1, len(lines)):
                    if ((lines[index].isalnum()) or (lines[index] == "_") or (lines[index] == ".")
                            or (lines[index] == "(") or (lines[index] == ")") or (lines[index] == "'")
                            or (lines[index] == "#") or (lines[index] == "$") or (lines[index] == '-')
                            or (lines[index] == "{") or (lines[index] == "}") or (lines[index] == '"')
                            or (lines[index] == ">") or (lines[index] == "<") or (lines[index] == ":")
                            or (lines[index] == "|") or (lines[index] == "@") or (lines[index] == " ")
                            or (lines[index] == ",") or (lines[index] == "\\")):

                        if (lines[index] == ")") and (variable.find("(")) == -1:
                            break
                        if (lines[index] == "}") and (variable.find("{")) == -1:
                            break
                        variable += lines[index]
                    else:
                        break
                tpl_variable_names_array.append(variable)
                location = lines.find("$", location + 1, len(lines))  # While loop in case one line has >1 variable

        # Remove redundant duplicates that are in the tpl files
        variables = list(dict.fromkeys(tpl_variable_names_array))
        final_output_tpl_list = []

        for l in variables:
            v = ""
            if l.find(" eq") != -1:
                for loop in range(0, l.find(" eq")):
                    v += l[loop]
            elif l.find(" and") != -1:
                for loop in range(0, l.find(" and")):
                    v += l[loop]
            elif l.find(" or") != -1:
                for loop in range(0, l.find(" or")):
                    v += l[loop]
            elif l.find(" neq") != -1:
                for loop in range(0, l.find(" neq")):
                    v += l[loop]
            elif l.find(", ") != -1:
                for loop in range(0, l.find(", ")):
                    v += l[loop]
            elif l.find(" item") != -1:
                for loop in range(0, l.find(" item")):
                    v += l[loop]
            elif (l[-1] == ">") or (l[-1] == "<"):
                for loop in range(0, len(l) - 1):
                    v += l[loop]
            elif (l[-1] == "{") or (l[-1] == "("):
                for loop in range(0, len(l) - 2):
                    v += l[loop]
            elif l.find(",$") != -1:
                for loop in range(0, l.find(",$")):
                    v += l[loop]
            elif l.find(" || ") != -1:
                for loop in range(0, l.find(" || ")):
                    v += l[loop]
            elif l.find(" && ") != -1:
                for loop in range(0, l.find(" && ")):
                    v += l[loop]
            else:
                v = l
            final_output_tpl_list.append(v)

        variables = list(dict.fromkeys(final_output_tpl_list))

        # line number location code block
        line_number = 0
        tpl_array = []
        for line in tpl_code_array:
            line_number += 1
            for local in variables:
                if line.find(local) != -1:
                    temp = str(local) + ' ' + str(line_number)
                    tpl_array.append(temp)

        # For a neat print
        print("Variable name : line number")
        for local in variables:
            for line in tpl_array:
                if line.find(local) != -1:
                    print(line)
                    print("\n")
                    pprint.pprint(locals())
        print("\n")
        f.close()
    sys.stdout.close()

if tpl_php == "www":
    # Open a php file (for testing purposes)
    sys.stdout = open("php.txt", "w")
    # call to get all the php files
    php_files = get_all_php_files(find_path(user_name, extract_location, library, sub_library, tpl_php))
    # browse all php files that are required to read in the array:
    for php_file in php_files:
        print(php_file)
        g = open(php_file)

        # Creating different arrays to access data from the php files:
        php_code_array = g.readlines()
        php_assign_lines = []
        php_variable_names_array = []
        php_output = []
        line_count = 0
        file_count = 0

        # browsing each line in the php folder
        # browsing how many times the class method assign is used in order to get the variable names
        for line in php_code_array:
            line_count += 1
            if line.find("$smarty->assign") != -1:
                php_assign_lines.append(line)
                php_output.append(line_count)

        for lines in php_assign_lines:
            locate = lines.find("'")
            while locate != -1:
                relative_var = ''
                for index in range(locate + 1, len(lines)):
                    if lines[index] == "'":
                        break
                    else:
                        relative_var += lines[index]
                php_variable_names_array.append(relative_var)
                locate = lines.find("'", locate + 2 + len(relative_var), len(lines))

        # Remove redundant duplicates that are in the php files
        assigned_var = list(dict.fromkeys(php_variable_names_array))

        # For a neat print
        print("Variable name : line number")
        for l in assigned_var:
            print(l, php_output[file_count])  # combine php and tpl files to find related templates.
            print("\n")
            pprint.pprint(locals())
        print("\n")
        g.close()
    sys.stdout.close()
