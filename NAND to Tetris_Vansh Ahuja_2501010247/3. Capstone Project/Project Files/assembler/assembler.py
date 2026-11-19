
import sys

next_variable_address = 16
declared_labels = set()

# Predefined Hack symbols
symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

# Registers R0 to R15
for i in range(16):
    symbol_table[f"R{i}"] = i

# Destination codes
dest_table = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

# Computation codes
comp_table = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000",
    "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010",
    "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000", "!M": "1110001",
    "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}

# Jump codes
jump_table = {
    "": "000", "JGT": "001", "JEQ": "010",
    "JGE": "011", "JLT": "100", "JNE": "101",
    "JLE": "110", "JMP": "111"
}


# Remove comments and blank lines
def clean_lines(lines):
    cleaned = []

    for line in lines:
        line = line.split("//")[0].strip()

        if line:
            cleaned.append(line)

    return cleaned


# First pass: identify labels
def first_pass(lines):
    rom_address = 0

    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]

            if label in declared_labels:
                print(f"Warning: Duplicate label '{label}' declared!")
            else:
                declared_labels.add(label)
                symbol_table[label] = rom_address

        else:
            rom_address += 1


# Translate A-instructions
def translate_a_instruction(instruction):
    global next_variable_address

    symbol = instruction[1:]

    if symbol.isdigit():
        address = int(symbol)

    elif symbol in symbol_table:
        address = symbol_table[symbol]

    else:
        address = next_variable_address
        symbol_table[symbol] = address
        next_variable_address += 1

    return format(address, "016b")


# Translate C-instructions
def translate_c_instruction(instruction):
    dest = ""
    jump = ""

    if "=" in instruction:
        dest, instruction = instruction.split("=")

    if ";" in instruction:
        instruction, jump = instruction.split(";")

    comp = instruction

    return (
        "111"
        + comp_table[comp]
        + dest_table[dest]
        + jump_table[jump]
    )


# Second pass: generate machine code
def second_pass(lines):
    machine_code = []

    for line in lines:

        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            binary = translate_a_instruction(line)
        else:
            binary = translate_c_instruction(line)

        machine_code.append(binary)

    return machine_code


# Main assembler function
def assemble(input_file):
    global next_variable_address

    next_variable_address = 16
    declared_labels.clear()

    with open(input_file, "r") as file:
        lines = file.readlines()

    cleaned = clean_lines(lines)

    first_pass(cleaned)

    machine_code = second_pass(cleaned)

    output_file = input_file.rsplit(".", 1)[0] + ".hack"

    with open(output_file, "w") as file:
        file.write("\n".join(machine_code) + "\n")

    print(f"Assembly successful! Output: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
    else:
        assemble(sys.argv[1])
