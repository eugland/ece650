#!/usr/bin/env python3
import sys
from input import process_input, InputContent
from street import Street

# YOUR CODE GOES HERE


def main():
    streets = Street()

    line = 'a'
    while True:
        print('Please input your command or help for a list of options:')
        line = sys.stdin.readline().strip()
        if line == '':
            sys.stderr.write('Program exiting on empty string')
            break

        # process the input and perform logic
        input: InputContent = process_input(line)
        print(input.__dict__)  # debug input

        if input.status == False:
            continue

        if input.cmd == 'gg':
            streets.generate_graph()
        elif input.cmd == 'add':
            streets.add(input.street_name, input.coordinates)
        elif input.cmd == 'mod':
            streets.modify(input.street_name, input.coordinates)
        elif input.cmd == 'rm':
            streets.modify(input.street_name)
        else:
            print(f'Sorry, your command "{line}" was not understood')


if __name__ == "__main__":
    main()
