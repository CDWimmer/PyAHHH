# encoding: utf-8
"""
A Python implementation of an AHHH language interpreter originally concocted by Kyle Morgenstein, for some reason.
I wrote this because I don't know C++ or know how to compile C++ but I still need to scream.
Requires Python 3.6 or above.
I honestly have no idea if this meets the original spec, I spent maybe 5 hours on this.

Find the original AHHH here: https://github.com/KyleM73/AHHH

Like the original, feel free to edit/use as you like, but please do not sell this nonsense or its derivatives.
(This is predominantly life advice rather than a legal disclaimer but I suppose both can be true)
If you use this for some reason then attribution would be pretty cool. Link back to the Github repository maybe.
"""

import argparse
import os
from sys import stderr, exit

__author__ = "Charles D Wimmer"
__copyright__ = "Copyright 2021, Charles D Wimmer"
__credits__ = "Charles D Wimmer"
__licence__ = "GPL"
__version__ = "20210608"
__twitter__ = "@CharlesDWimmer"
__email__ = __twitter__  # yup
__status__ = "Stage 2: Bargaining"


REGISTER_1 = None  # "None" indicates that we have no value yet set to a register.
REGISTER_2 = None
PROGRAM_REGISTER = 0  # keeping track of which program instruction we're on.
POINTER_POS = 0
MEMORY_TAPE = [0]  # I don't know if this should start as totally empty or with an [0] = 0 but this made less errors
PROGRAM = []
CODES = {
    "hhhh": 0, "hhhH": 1, "hhHh": 2, "hhHH": 3, "hHhh": 4, "hHhH": 5, "hHHh": 6, "hHHH": 7, "Hhhh": 8, "HhhH": 9,
    "HhHh": 10, "HhHH": 11, "HHhh": 12, "HHhH": 13, "HHHh": 14, "HHHH": 15, "AHHH": 16, "hhh!": 17
}


def quit_ahhh(exit_code):
    if debug:
        print("== EXECUTION FINISHED. ==\n"
              f"Exit code: {exit_code}\n"
              f"MEMORY TAPE: {MEMORY_TAPE}\n"
              f"REGISTER 1: {REGISTER_1}\n"
              f"REGISTER 2: {REGISTER_2}\n"
              f"PROGRAM REGISTER: {PROGRAM_REGISTER}")
    exit(exit_code)


def throw_error(message):
    """This is probably a horrible way to do this"""
    print(f"Error: {message}", file=stderr)
    quit_ahhh(1)


def read_program(filepath):
    """Reads in the program line by line and converts it to instruction codes in the `PROGRAM` list."""
    if not os.path.exists(filepath):
        parser.error(f"The file {filepath} does not exist!")
    else:
        with open(filepath, 'r') as f:
            # If I understand the commenting rules correctly then a comment is anything after a space on a line.
            # So if we just cut off everything after a space on each line then we are left with just instructions
            lines = [line.split(' ')[0] for line in f.readlines()]
            # iterate through each line, break it down into chunks of 4 characters and freak out if it's not a multiple
            # of 4 long:
            for i, line in enumerate(lines):
                line = line.strip()  # no newlines >:(  - stripping empty lines or lines without comments
                if len(line) % 4 != 0:
                    throw_error(f"Instructions of wrong length (len % 4 != 0) on line {i+1}")
                elif len(line) == 0:
                    continue  # blank lines are allowed we just ignore them :)
                else:
                    # https://stackoverflow.com/questions/9475241/split-string-every-nth-character
                    n = 4  # instructions are length 4.
                    instructions = [line[i:i+n] for i in range(0, len(line), n)]
                    for instruction in instructions:
                        if instruction not in CODES.keys():
                            throw_error(f"Instruction `{instruction}` not recognised on line {i+1}.")
                        else:
                            # actually start turning it into codes!
                            PROGRAM.append(CODES[instruction])


def run():
    """All AHHH program execution happens in here"""
    global POINTER_POS  # I don't understand why it wants this but the snake lang must feed on tears
    global PROGRAM_REGISTER
    global MEMORY_TAPE
    global REGISTER_1, REGISTER_2

    if len(PROGRAM) == 0 or PROGRAM[0] != 16:
        throw_error("Program is empty or does not start with 'AHHH'")
    while True:
        try:
            instruction = PROGRAM[PROGRAM_REGISTER]
        except IndexError:
            # instruction counter is out of range of the program. We're finished executing.
            break
        if debug:
            print(f"== INSTRUCTION: {instruction} ==")
        # hhhh
        if instruction == 0:
            """Searching in reverse, skip the first preceding command, and then jump back to matching HHHH command and 
            begin execution from that HHHH command (end loop)."""
            level = 1
            PROGRAM_REGISTER -= 1
            while level > 0:
                if PROGRAM_REGISTER == 1:
                    throw_error("Cannot end loop as first instruction!")
                PROGRAM_REGISTER -= 1

                if PROGRAM[PROGRAM_REGISTER] == 0:
                    level += 1

                elif PROGRAM[PROGRAM_REGISTER] == 15:
                    level -= 1
            if level != 0:
                throw_error("Loop error")
            continue  # avoid incrementing the program register at the end of the main run() while.

        # hhhH
        elif instruction == 1:
            """Move the pointer right one cell."""
            POINTER_POS += 1
            if POINTER_POS > len(MEMORY_TAPE) - 1:
                MEMORY_TAPE.append(0)
        # hhHh
        elif instruction == 2:
            """Move the pointer left one cell."""
            POINTER_POS -= 1
            if POINTER_POS < 0:
                throw_error(f"Memory pointer position set to less than zero! Instruction number: {PROGRAM_REGISTER}")
        # hhHH
        elif instruction == 3:
            """Print the current memory cell as an integer."""
            if debug:
                print(f"== PRINT INT FROM {POINTER_POS}: {MEMORY_TAPE[POINTER_POS]}==")
            print(str(MEMORY_TAPE[POINTER_POS]), end='', flush=True)
        # hHhh
        elif instruction == 4:
            """If Register 1 is empty, copy the current memory cell to the register. Otherwise, write the Register 1 
            value to the current memory cell."""
            if REGISTER_1 is None:
                REGISTER_1 = MEMORY_TAPE[POINTER_POS]
            else:  # register has value
                MEMORY_TAPE[POINTER_POS] = REGISTER_1
                REGISTER_1 = None

        # hHhH
        elif instruction == 5:
            """If Register 2 is empty, copy the current memory cell to the register. Otherwise, write the Register 2 
            value to the current memory cell."""
            if REGISTER_2 is None:
                REGISTER_2 = MEMORY_TAPE[POINTER_POS]
            else:
                MEMORY_TAPE[POINTER_POS] = REGISTER_2
                REGISTER_2 = None

        # hHHh
        elif instruction == 6:
            """Add the current memory cell to the value of Register 1 and store the sum in Register 1. The memory cell 
            is unchanged."""
            REGISTER_1 = REGISTER_1 + MEMORY_TAPE[POINTER_POS]
        # hHHH
        elif instruction == 7:
            """Add the current memory cell to the value of Register 2 and store the sum in Register 2. The memory cell 
            is unchanged."""
            REGISTER_2 = REGISTER_2 + MEMORY_TAPE[POINTER_POS]
        # Hhhh
        elif instruction == 8:
            """If the current memory cell is nonzero, print the cell as an ASCII character. Otherwise, read in an 
            ASCII character from the console."""
            if MEMORY_TAPE[POINTER_POS] > 0:  # not zero and not less than zero. - negs are invalid for ascii!
                if debug:
                    print(f"== PRINT CHAR FROM {POINTER_POS}: {MEMORY_TAPE[POINTER_POS]} -> "
                          f"{chr(MEMORY_TAPE[POINTER_POS])} ==")
                print(chr(MEMORY_TAPE[POINTER_POS]), end='', flush=True)
            else:
                if debug:
                    print(f"== INPUTTING ASCII CHAR TO MEMORY POSITION {POINTER_POS} ==")
                inputting = True
                while inputting:
                    try:
                        MEMORY_TAPE[POINTER_POS] = ord(input("ASCII character input: "))
                    except TypeError:
                        print("Please enter a valid ASCII character. ")
        # HhhH
        elif instruction == 9:
            """Increment the current memory cell by one."""
            MEMORY_TAPE[POINTER_POS] += 1
        # HhHh
        elif instruction == 10:
            """Decrement the current memory cell by one."""
            MEMORY_TAPE[POINTER_POS] -= 1
        # HhHH
        elif instruction == 11:
            """Read in an integer from the console and store it in the current memory cell (overwrites current cell)."""
            if MEMORY_TAPE[POINTER_POS] != 0:
                print(chr(MEMORY_TAPE[POINTER_POS]), end='', flush=True)
            else:
                if debug:
                    print(f"== INPUTTING INT TO MEMORY POSITION {POINTER_POS} ==")
                inputting = True
                while inputting:
                    try:
                        MEMORY_TAPE[POINTER_POS] = ord(input("Integer input: "))
                    except TypeError:
                        print("Please enter a valid integer. ")
        # HHhh
        elif instruction == 12:
            """Set the current memory cell to zero."""
            MEMORY_TAPE[POINTER_POS] = 0
        # HHhH
        elif instruction == 13:
            """Double the value of the current memory cell and store it in the current memory cell."""
            MEMORY_TAPE[POINTER_POS] = MEMORY_TAPE[POINTER_POS] * 2
        # HHHh
        elif instruction == 14:
            """Square the value of the current memory cell and store it in the current memory cell."""
            MEMORY_TAPE[POINTER_POS] = MEMORY_TAPE[POINTER_POS]**2
        # HHHH
        elif instruction == 15:
            if MEMORY_TAPE[POINTER_POS] == 0:  # if non-zero then we skip the loop, otherwise do nothing.
                level = 1
                prev = 0
                PROGRAM_REGISTER += 1
                if PROGRAM_REGISTER >= len(PROGRAM) - 1:
                    throw_error("Loop error, EOF while searching for end of loop")
                while level > 0:
                    prev = PROGRAM[PROGRAM_REGISTER]
                    PROGRAM_REGISTER += 1
                    if PROGRAM_REGISTER == len(PROGRAM) - 1:
                        break
                    elif PROGRAM[PROGRAM_REGISTER] == 15:
                        level += 1
                    elif PROGRAM[PROGRAM_REGISTER] == 0:
                        # found a hhhh
                        level -= 1
                        if prev == 15:
                            level -= 1
                if level != 0:
                    throw_error("Loop error, EOF while searching for end of loop")
        # AHHH
        elif instruction == 16:
            """Start program."""
            pass  # not sure what to do if this is encountered in the wrong place?
        # hhh!
        elif instruction == 17:
            """Print new line (useful after printing ASCII characters, which otherwise don't print a new line)."""
            print("")  # prints newline automatically.

        if debug:
            print(f"-> MEM: {MEMORY_TAPE}\tREG1: {REGISTER_1}\tREG2: {REGISTER_2}\t MPOS: {POINTER_POS}")
        PROGRAM_REGISTER += 1
        # end of while
    quit_ahhh(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='An AHHH interpreter written in Python.', epilog='Ahhhhhhh!')
    parser.add_argument('filepath', type=str, help='filepath for a .ahhh script.')
    parser.add_argument('-d', '--debug', help='Debug mode flag', action='store_true')
    args = parser.parse_args()
    debug = False
    if args.debug:
        print("== DEBUG MODE IS ON. ==")
        debug = True

    # read program
    read_program(args.filepath)
    if debug:
        print(f"PROGRAM CODE:\n{', '.join(str(x) for x in PROGRAM)}")

    # RUN
    run()
