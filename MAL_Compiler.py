import os
import datetime

'''Author: Daniel Galarza'''

# Initializing global variables to keep track of amount of errors.
line_counter = 0          # Counter for line numbering.
ill_formed_labels = 0
opcode_errors = 0
too_few_operands = 0
too_many_operands = 0
ill_formed_operands = 0
wrong_operand_type = 0
label_problems = False
label_problems_count = 0

label_array = []            # Contains labels only
branch_label_array = []     # Contains labels that are being branched to.


# THIS FUNCTION
def main():

    # Declaring that I will use global variables in this function
    global line_counter
    global ill_formed_labels
    global opcode_errors
    global too_few_operands
    global too_many_operands
    global ill_formed_operands
    global wrong_operand_type
    global label_problems
    global label_problems_count
    global label_array
    global branch_label_array

    # Prompting the user for the name of the file, without the file extension, to compile.
    input_filename = input("Type the name of the file that you would like to compile. " +
                           "\nInclude the file extension: (Good Example: fileName.txt | BAD Example: fileName):  ")

    # Renaming and appending .mal extension to input file in the directory.
    os.rename(input_filename, os.path.splitext(input_filename)[0] + ".mal")

    # Renaming and appending .mal extension to input file in the program.
    input_filename = os.path.splitext(input_filename)[0] + ".mal"

    # The name of the output file.
    output_filename = os.path.splitext(input_filename)[0] + ".log"

    # Opening the input file in read mode. If the file doesn't exist, then it creates it.
    input_file = open(input_filename, 'r')

    # Opening the output file in write mode. If the file doesn't exist, then it creates it.
    output_file = open(output_filename, 'w')

    # Getting the system date as a string in MM-DD-YYYY HH:MM format.
    now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")

    comment = ';'            # Start of a comment.
    label = ':'              # End of a label.

    # Header for .log file.
    output_file.write("<Input File: " + input_filename + ", Output File: " + output_filename +
                      ", Date Processed: " + now + ", My Name: Daniel Galarza>\n\n" +
                      "--------------\n\n" + "MAL Program Listing\n\n")

    # Looping through the input file.
    for line in input_file:

        mal_line = line.strip(" ")    # A line from the MAL input file, without whitespace on the left side of string.
        line_counter += 1              # Keeping track of the line numbers.

        # Checking if there exists a comment.
        if comment in mal_line:
            mal_line = mal_line.split(";", 1)[0] + "\n"  # Splits line with comment into two. Tosses out the comment.
            mal_line.strip(" ")

        # Skips line if it's blank (including spaces, tabs, newline character etc.).
        if mal_line.isspace():
            print("Skipping line")
            continue

        # if label in line...
        if label in mal_line:
            temp_label = mal_line.split(":", 1)[0]
            rest_of_line = mal_line.split(":", 1)[1]
            label_array.append(temp_label)

            # if label length is greater that 5...
            if len(temp_label) > 5:
                ill_formed_labels += 1
                print("Invalid Label name (too long)")
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Label name is too long! **\n")
                continue

            # if label contains anything other than letters...
            elif (has_numbers(temp_label) or has_special_chars(temp_label)) is True:
                ill_formed_labels += 1
                print("Invalid Label name (contains characters that aren't letters!)")
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Label name can only contain letters!: " + temp_label + "**\n")
                continue

            # if not a valid opcode...
            elif is_valid_opcode(rest_of_line.lstrip(" ").split(" ", 1)[0].strip("\n").strip()) is False:

                if not rest_of_line.lstrip(" ").split(" ", 1)[0].strip("\n").strip():
                    print("nothing after label (whitespace)")
                    output_file.write(str(line_counter) + ". " + mal_line)
                    continue
                else:
                    opcode_errors += 1
                    print(";" + rest_of_line.lstrip(" ").split(" ", 1)[0].strip("\n").strip() + ";")
                    invalid_opcode = rest_of_line.lstrip(" ").split(" ", 1)[0].strip()
                    print("Opcode error found" + " '" + invalid_opcode + "' " + "inside")
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Contains an invalid instruction/opcode: " + invalid_opcode + " **\n")
                    continue

            # if label is valid and opcode is valid...
            elif not rest_of_line.isspace():
                opcode = rest_of_line.lstrip(" ").split(" ", 1)[0]

                if "\n" in opcode:
                    opcode = opcode.rstrip()

                if check_opcode_type(opcode, rest_of_line, mal_line, output_file) is True:  # had line_counter
                    output_file.write(str(line_counter) + ". " + mal_line)
                    continue
                else:
                    continue

        # if opcode is invalid...
        if not is_valid_opcode(mal_line.lstrip(" ").split(" ", 1)[0]) and label not in mal_line:
            opcode_errors += 1
            invalid_opcode = mal_line.lstrip(" ").split(" ", 1)[0]
            print("opcode error found" + " '" + invalid_opcode + "' " + "outside")
            output_file.write(str(line_counter) + ". " + mal_line)
            output_file.write("  ** Contains an invalid instruction/opcode: " + invalid_opcode + " **\n")
            continue

        # if line does not start with a label...
        if label not in mal_line:
            opcode = mal_line.lstrip(" ").split(" ", 1)[0]

            if opcode == "MOVEI" or opcode == "BEQ" or opcode == "BLT" or opcode == "BGT":
                whole_line = mal_line.strip(" ").strip("\n")
            else:
                whole_line = mal_line.strip(" ")

            if "\n" in opcode:
                opcode = opcode.rstrip()

            if check_opcode_type(opcode, whole_line, mal_line, output_file) is True:  # had line_counter
                output_file.write(str(line_counter) + ". " + mal_line)
                continue
            else:
                continue

        # Prints to the output file.
        output_file.write(str(line_counter) + ". " + mal_line)

    # Total number of errors in MAL.
    total_errors = ill_formed_labels + opcode_errors + too_few_operands + too_many_operands + \
        ill_formed_operands + wrong_operand_type + label_problems_count

    output_file.write("\n--------------\n")
    output_file.write("Total Errors: " + str(total_errors) + "\n")

    # This will check that branches are valid
    if has_valid_branches(list(set(branch_label_array)), label_array):
        print("valid branches")

    else:
        label_problems = True
        label_problems_count += 1
        print("invalid branches")

    # Error processing.
    if ill_formed_labels > 0:
        output_file.write("  " + str(ill_formed_labels) + " Ill-Formed Labels\n")

    if opcode_errors > 0:
        output_file.write("  " + str(opcode_errors) + " Invalid Opcode(s)\n")

    if too_few_operands > 0:
        output_file.write("  " + str(too_few_operands) + " Too Few Operands\n")

    if too_many_operands > 0:
        output_file.write("  " + str(too_many_operands) + " Too Many Operands\n")

    if ill_formed_operands > 0:
        output_file.write("  " + str(ill_formed_operands) + " Ill-Formed Operand(s)\n")

    if wrong_operand_type > 0:
        output_file.write("  " + str(wrong_operand_type) + " Wrong Operand Type(s)\n")

    if label_problems:
        output_file.write("  Label Problem(s) = " + str(label_problems) + "\n")
        output_file.write("       Invalid Branch(es): " + str(list(set(branch_label_array) - set(label_array))) + "\n")

    if total_errors > 0 and (label_problems is False):
        output_file.write("Processing Complete: MAL program is NOT valid!")
    else:
        output_file.write("Processing Complete: MAL program is valid!")

    print("Done processing.")
    output_file.close()
    input_file.close()


# THIS FUNCTION CHECKS FOR THE RIGHT OPERANDS DEPENDING ON THE OPCODE.
def check_opcode_type(opcode, operands, mal_line, output_file):

    global line_counter
    global too_few_operands
    global too_many_operands
    global ill_formed_operands
    global wrong_operand_type
    global label_problems
    global label_array
    global branch_label_array


# ***********************  OPCODE: MOVE  ************************ #

    if opcode == "MOVE":

        if "," in operands:

            operand_one = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ").split(",", 1)[0]
            operand_two = operands.lstrip(" ").split(" ", 1)[1].split(",", 1)[1].strip(" ").strip("\n")
            print("opcode: " + opcode + "  operand 1: '" + operand_one + "'  operand 2: '" + operand_two + "'")

            if is_valid_register(operand_one) or is_valid_identifier(operand_one):
                print("operand 1 is valid register or is valid identifier")

                if operand_two.isspace() or not operand_two:
                    too_few_operands += 1
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Contains too few operands for 'MOVE' **\n")
                    print("operand 2 is invalid")
                    return False

                elif has_special_chars(operand_two):

                    if operand_two.split(",", 1)[1].isspace() or not operand_two.split(",", 1)[1]:
                        print("operand 2 has trailing comma")
                        return True

                    else:
                        too_many_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        output_file.write("  ** Contains too many operands for 'MOVE' **\n")
                        print("Contains too many operands for 'MOVE' ")
                        return False

                elif is_valid_register(operand_two) or is_valid_identifier(operand_two):
                    print("operand 2 is valid register or valid identifier")
                    return True

                else:
                    ill_formed_operands += 1
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Ill-formed operand (operand 2)- bad register or identifier **\n")
                    print("operand 2 is invalid")
                    return False

            else:
                ill_formed_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Ill-formed operand (operand 1)- bad register or identifier **\n")
                print("operand 1 is invalid")
                return False

        else:
            too_few_operands += 1
            output_file.write(str(line_counter) + ". " + mal_line)
            output_file.write("  ** This line contains too few operands for 'MOVE' **\n")
            print("need a comma to separate operands or too few operands")
            return False


# ***********************  OPCODE: MOVEI  ************************ #

    elif opcode == "MOVEI":

        if "," in operands:

            operand_one = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ").split(",", 1)[0]
            operand_two = operands.lstrip(" ").split(" ", 1)[1].split(",", 1)[1].strip(" ").strip("\n")
            print("opcode: " + opcode + "  operand 1: '" + operand_one + "'  operand 2: '" + operand_two + "'")

            if is_valid_octal(operand_one):

                print("operand 1 is valid octal")

                if operand_two.isspace() or not operand_two:
                    too_few_operands += 1
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Contains too few operands for 'MOVEI' **\n")
                    print("operand 2 is invalid")
                    return False

                elif has_special_chars(operand_two):

                    if operand_two.split(",", 1)[1].isspace() or not operand_two.split(",", 1)[1]:
                        print("operand 2 has trailing comma")
                        return True

                    else:
                        too_many_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        output_file.write("  ** Contains too many operands for 'MOVEI' **\n")
                        print("Contains too many operands for 'MOVEI' ")
                        return False

                elif is_valid_register(operand_two) or is_valid_identifier(operand_two):
                    print("operand 2 is valid register or valid identifier")
                    return True

                else:
                    ill_formed_operands += 1
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Ill-formed operand (operand 2)- bad register or identifier **\n")
                    print("operand 2 is invalid")
                    return False

            else:
                ill_formed_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Ill-formed operand (operand 1)- bad octal **\n")
                print("operand 1 is invalid")
                return False

        else:
            too_few_operands += 1
            output_file.write(str(line_counter) + ". " + mal_line)
            output_file.write("  ** This line contains too few operands for 'MOVEI' **\n")
            print("need a comma to separate operands or too few operands")
            return False


# ***********************  OPCODES: ADD, SUB, MUL, DIV  ************************ #

    elif opcode == "ADD" or opcode == "SUB" or opcode == "MUL" or opcode == "DIV":

        if "," in operands:

            operand_one = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ").split(",", 1)[0]
            operand_two = operands.lstrip(" ").split(" ", 1)[1].split(",", 1)[1].lstrip(" ").split(",", 1)[0]

            if "\n" in operand_two:
                too_few_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                if opcode == "ADD":
                    output_file.write("  ** Contains too few operands for 'ADD' **\n")
                elif opcode == "SUB":
                    output_file.write("  ** Contains too few operands for 'SUB' **\n")
                elif opcode == "MUL":
                    output_file.write("  ** Contains too few operands for 'MUL' **\n")
                elif opcode == "DIV":
                    output_file.write("  ** Contains too few operands for 'DIV' **\n")
                print("Too few operands")
                return False

            else:
                operand_three = operands.lstrip(" ").split(" ", 1)[1].split(",", 1)[1].lstrip(" ").split(",", 1)[1]\
                    .strip(" ").strip("\n")
                print("opcode: " + opcode + "  op1: '" + operand_one + "'  op2: '" + operand_two + "' op3: '" +
                      operand_three + "'")

            if is_valid_register(operand_one) or is_valid_identifier(operand_one):

                print("operand 1 is valid register or valid identifier")

                if is_valid_register(operand_two) or is_valid_identifier(operand_two):

                    print("operand 2 is valid register or valid identifier")

                    if operand_three.isspace() or not operand_three:
                        too_few_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        if opcode == "ADD":
                            output_file.write("  ** Contains too few operands for 'ADD' **\n")
                        elif opcode == "SUB":
                            output_file.write("  ** Contains too few operands for 'SUB' **\n")
                        elif opcode == "MUL":
                            output_file.write("  ** Contains too few operands for 'MUL' **\n")
                        elif opcode == "DIV":
                            output_file.write("  ** Contains too few operands for 'DIV' **\n")
                        print("operand 3 is invalid register or identifier")
                        return False

                    elif has_special_chars(operand_three):

                        if operand_three.split(",", 1)[1].isspace() or not operand_three.split(",", 1)[1]:
                            print("operand 3 has trailing comma, but valid")
                            return True

                        else:
                            too_many_operands += 1
                            output_file.write(str(line_counter) + ". " + mal_line)
                            if opcode == "ADD":
                                output_file.write("  ** Contains too many operands for 'ADD' **\n")
                                print("Contains too many operands for ADD")
                            elif opcode == "SUB":
                                output_file.write("  ** Contains too many operands for 'SUB' **\n")
                                print("Contains too many operands for SUB")
                            elif opcode == "MUL":
                                output_file.write("  ** Contains too many operands for 'MUL' **\n")
                                print("Contains too many operands for MUL")
                            elif opcode == "DIV":
                                output_file.write("  ** Contains too many operands for 'DIV' **\n")
                                print("Contains too many operands for DIV")
                            return False

                    elif is_valid_register(operand_three) or is_valid_identifier(operand_three):
                        print("operand 3 is valid register or valid identifier")
                        return True

                    else:
                        ill_formed_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        output_file.write("  ** Ill-formed operand (operand 3)- bad register or identifier **\n")
                        print("operand 3 is invalid")
                        return False

                else:
                    ill_formed_operands += 1
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Ill-formed operand (operand 2)- bad register or identifier  **\n")
                    print("operand 2 is invalid")
                    return False

            else:
                ill_formed_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Ill-formed operand (operand 1)- bad register or identifier **\n")
                print("operand 1 is invalid")
                return False

        else:
            too_few_operands += 1
            output_file.write(str(line_counter) + ". " + mal_line)
            if opcode == "ADD":
                output_file.write("  ** Contains too few operands for 'ADD' **\n")
            elif opcode == "SUB":
                output_file.write("  ** Contains too few operands for 'SUB' **\n")
            elif opcode == "MUL":
                output_file.write("  ** Contains too few operands for 'MUL' **\n")
            elif opcode == "DIV":
                output_file.write("  ** Contains too few operands for 'DIV' **\n")

            print("Needs a comma to separate operands or too few operands")
            return False


# ***********************  OPCODES: INC, DEC  ************************ #

    elif opcode == "INC" or opcode == "DEC":

        if len(operands.strip()) > 3:

            print(str(len(operands.strip())))
            operand_one = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ").split(" ", 1)[0].strip(" ").strip("\n")
            rest_of_line = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ")
            print("opcode: " + opcode + "  operand 1: '" + operand_one + "' rest of line: '" + rest_of_line + "'")

            if has_special_chars(operands):
                operand_one = operand_one.split(",", 1)[0]

                if is_valid_register(operand_one) or is_valid_identifier(operand_one):
                    print("operand 1 is valid register or is valid identifier")

                    if rest_of_line.split(",", 1)[1].isspace() or not rest_of_line.split(",", 1)[1].strip():
                        print("operand 1 has trailing comma")
                        return True

                    else:
                        too_many_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        if opcode == "INC":
                            output_file.write("  ** Contains too many operands for 'INC' **\n")
                        else:
                            output_file.write("  ** Contains too many operands for 'DEC' **\n")
                        print("Too many operands")
                        return False

            if is_valid_register(operand_one) or is_valid_identifier(operand_one):
                print("operand 1 is valid register or is valid identifier")
                return True

            elif operand_one.isspace() or not operand_one:
                too_few_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                if opcode == "INC":
                    output_file.write("  ** Contains too few operands for opcode 'INC' **\n")
                else:
                    output_file.write("  ** Contains too few operands for opcode 'DEC' **\n")
                print("operand 1 is invalid")
                return False

            else:
                ill_formed_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Ill-formed operand (operand 1)- bad register or identifier **\n")
                print("operand 1 is invalid")
                return False
        else:
            too_few_operands += 1
            output_file.write(str(line_counter) + ". " + mal_line)
            if opcode == "INC":
                output_file.write("  ** Contains too few operands for opcode 'INC' **\n")
            else:
                output_file.write("  ** Contains too few operands for opcode 'DEC' **\n")
            print("operand 1 is invalid")
            return False


# ***********************  OPCODES: BEQ, BLT, BGT  ************************ #

    elif opcode == "BEQ" or opcode == "BLT" or opcode == "BGT":

        if "," in operands:

            operand_one = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ").split(",", 1)[0]
            operand_two = operands.lstrip(" ").split(" ", 1)[1].split(",", 1)[1].lstrip(" ").split(",", 1)[0]

            if "\n" in operand_two:
                too_few_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                if opcode == "BEQ":
                    output_file.write("  ** Contains too few operands for 'BEQ' **\n")
                    print("Contains too few operands for BEQ")
                elif opcode == "BLT":
                    output_file.write("  ** Contains too few operands for 'BLT' **\n")
                    print("Contains too few operands for BLT")
                elif opcode == "BGT":
                    output_file.write("  ** Contains too few operands for 'BGT' **\n")
                    print("Contains too few operands for BGT")
                return False

            else:
                operand_three = operands.lstrip(" ").split(" ", 1)[1].split(",", 1)[1].lstrip(" ").split(",", 1)[1]\
                    .strip(" ").strip("\n")
                print("opcode: " + opcode + "  op1: '" + operand_one + "'  op2: '" + operand_two + "' op3: '" +
                      operand_three + "'")

            if is_valid_register(operand_one) or is_valid_identifier(operand_one):

                print("operand 1 is valid register or valid identifier")

                if is_valid_register(operand_two) or is_valid_identifier(operand_two):

                    print("operand 2 is valid register or valid identifier")

                    if operand_three.isspace() or not operand_three:
                        too_few_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        if opcode == "BEQ":
                            output_file.write("  ** Contains too few operands for 'BEQ' **\n")
                            print("Contains too few operands for BEQ")
                        elif opcode == "BLT":
                            output_file.write("  ** Contains too few operands for 'BLT' **\n")
                            print("Contains too few operands for BLT")
                        elif opcode == "BGT":
                            output_file.write("  ** Contains too few operands for 'BGT' **\n")
                            print("Contains too few operands for BGT")
                        return False

                    elif has_special_chars(operand_three):

                        if operand_three.split(",", 1)[1].isspace() or not operand_three.split(",", 1)[1]:
                            print("operand 3 has trailing comma, but valid")
                            branch_label_array.append(operand_three)
                            return True

                        else:
                            too_many_operands += 1
                            output_file.write(str(line_counter) + ". " + mal_line)
                            if opcode == "BEQ":
                                output_file.write("  ** Contains too many operands for 'BEQ' **\n")
                                print("Contains too many operands for BEQ")
                            elif opcode == "BLT":
                                output_file.write("  ** Contains too many operands for 'BLT' **\n")
                                print("Contains too many operands for BLT")
                            elif opcode == "BGT":
                                output_file.write("  ** Contains too many operands for 'BGT' **\n")
                                print("Contains too many operands for BGT")
                            return False

                    elif is_valid_identifier(operand_three):
                        print("operand 3 is valid label")
                        branch_label_array.append(operand_three)
                        return True

                    else:
                        ill_formed_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        output_file.write("  ** Ill-formed operand (operand 3)- bad label **\n")
                        print("operand 3 is invalid")
                        return False

                else:
                    ill_formed_operands += 1
                    output_file.write(str(line_counter) + ". " + mal_line)
                    output_file.write("  ** Ill-formed operand (operand 2)- bad register or identifier  **\n")
                    print("operand 2 is invalid")
                    return False

            else:
                ill_formed_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Ill-formed operand (operand 1)- bad register or identifier **\n")
                print("operand 1 is invalid")
                return False

        else:
            too_few_operands += 1
            output_file.write(str(line_counter) + ". " + mal_line)
            if opcode == "BEQ":
                output_file.write("  ** Contains too few operands for 'BEQ' **\n")
            elif opcode == "BLT":
                output_file.write("  ** Contains too few operands for 'BLT' **\n")
            elif opcode == "BGT":
                output_file.write("  ** Contains too few operands for 'BGT' **\n")
            print("Needs a comma to separate operands or too few operands")
            return False

# ***********************  OPCODE: BR  ************************ #

    elif opcode == "BR":

        if len(operands.strip()) > 3:

            print(str(len(operands.strip())))
            operand_one = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ").split(" ", 1)[0].strip(" ").strip("\n")
            rest_of_line = operands.lstrip(" ").split(" ", 1)[1].lstrip(" ")
            print("opcode: " + opcode + "  operand 1: '" + operand_one + "' rest of line: '" + rest_of_line + "'")

            if has_special_chars(operands):
                operand_one = operand_one.split(",", 1)[0]

                if is_valid_register(operand_one) or is_valid_identifier(operand_one):
                    print("operand 1 is valid label")

                    if rest_of_line.split(",", 1)[1].isspace() or not rest_of_line.split(",", 1)[1].strip():
                        print("operand 1 has trailing comma")
                        branch_label_array.append(operand_one)
                        print(str(branch_label_array) + " **********")
                        return True

                    else:
                        too_many_operands += 1
                        output_file.write(str(line_counter) + ". " + mal_line)
                        output_file.write("  ** Contains too many operands for opcode 'BR' **\n")
                        print("Too many operands")
                        return False

            if is_valid_identifier(operand_one):
                print("operand 1 is valid label")
                branch_label_array.append(operand_one)
                print(str(branch_label_array) + " **********")
                return True

            elif operand_one.isspace() or not operand_one:
                too_few_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Contains too few operands for opcode 'BR' **\n")
                print("operand 1 is invalid")
                return False

            else:
                ill_formed_operands += 1
                output_file.write(str(line_counter) + ". " + mal_line)
                output_file.write("  ** Ill-formed operand (operand 1)- bad label **\n")
                print("operand 1 is invalid")
                return False
        else:
            too_few_operands += 1
            output_file.write(str(line_counter) + ". " + mal_line)
            output_file.write("  ** Contains too few operands for opcode 'BR' **\n")
            print("operand 1 is invalid")
            return False

    elif opcode == "END" or opcode == "END\n":
        print("END reached")
        return True


# THIS FUNCTION RETURNS TRUE IF THE INPUT STRING HAS AT LEAST ONE NUMBER IN IT.
def has_numbers(input_string):
    return any(character.isdigit() for character in input_string)


# THIS FUNCTION RETURN TRUE IF BRANCHES ARE VALID
def has_valid_branches(list_one, list_two):
    len_list_one = len(list_one)
    return any(list_one == list_two[i:len_list_one + i] for i in range(len(list_two) - len_list_one + 1))


# THIS FUNCTION RETURNS TRUE IF THE INPUT STRING CONTAINS AT LEAST ONE SPECIAL CHARACTER.
def has_special_chars(input_string):
    special_chars = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"

    for char in input_string:
        if char in special_chars:
            return True
    return False


# THIS FUNCTION RETURNS TRUE IF THE INSTRUCTION IS VALID.
def is_valid_opcode(opcode):
    # print(instr)
    instruction = {
        "MOVE": True,
        "MOVEI": True,
        "ADD": True,
        "INC": True,
        "SUB": True,
        "DEC": True,
        "MUL": True,
        "DIV": True,
        "BEQ": True,
        "BLT": True,
        "BGT": True,
        "BR": True,
        "END": True,
        "\n": True
    }
    return instruction.get(opcode.strip(), False)


# THIS FUNCTION CHECKS IF THE OPERAND IS A VALID REGISTER. RETURNS TRUE IF IT IS.
def is_valid_register(operand):
    registers = {
        "R0": True,
        "R1": True,
        "R2": True,
        "R3": True,
        "R4": True,
        "R5": True,
        "R6": True,
        "R7": True
    }
    return registers.get(operand.strip(), False)


# THIS FUNCTION RETURNS TRUE IF THE OCTAL IS VALID.
def is_valid_octal(input_string):

    if input_string.isdigit():
        if "8" in input_string or "9" in input_string:
            return False
        else:
            return True
    else:
        return False


# THIS FUNCTION RETURNS TRUE IF THE IDENTIFIER IS VALID.
def is_valid_identifier(input_string):
    input_string = input_string.strip()

    if len(input_string) <= 5 and not input_string.isspace():

        if has_numbers(input_string) is False:

            if has_special_chars(input_string) is False:
                return True
    return False


# Calling the main function.
main()
