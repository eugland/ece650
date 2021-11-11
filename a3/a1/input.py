import shlex
import re
import sys
from sys import stderr
from .node import Node


RM = 'rm'
ADD = 'add'
MOD = 'mod'
GG = 'gg'
COMMAND = [RM, ADD, MOD, GG]


def get(l, idx):
    try:
        return l[idx]
    except IndexError:
        return None


class InputContent:

    def __init__(self) -> None:
        self.status, self.cmd, self.street_name, self.coordinates = [None] * 4


def process_input(line) -> InputContent:
    '''Process the command based on line
    return 
    status: wether this has been parsed successfully
    command: a valid command,
    street_name: a street name,
    coordinates: a list of coordiantes; 
    '''
    r = InputContent()

    sp = shlex.split(line)
    cmd, street_name, cord = get(sp, 0), get(sp, 1), ' '.join(sp[2:])
    # print(f'Command:{cmd}\nStreet:{street_name}\nCoordinates:{cord}\n')

    r.status = True

    # if command not valid then return
    if cmd not in COMMAND:
        print(
            f'Error: Your command "{cmd}" is not one of {COMMAND}, try again.', file=stderr)
        r.status = False
        return r

    r.cmd = cmd  # cmd must be valid here, put it in.

    # if the command is gg, then no need to parse street name or coordinates, nor any need to reject it
    if cmd == GG:
        # print(street_name, cord)
        if street_name is not None or cord != '':
            print(
                f'Error "gg" command cannot have parameters, try again.', file=stderr)
            r.status = False
        return r

    # if street name does not exist;
    street_name = street_name.strip().lower()
    if not street_name or street_name == '':
        print(
            f'Error: Your street_name: "{street_name}" for {cmd} is invalid, try again.', file=stderr)
        r.status = False
        return r
    elif not all(chre.isalpha() or chre.isspace() for chre in street_name):
        print('Error: Street name must contain only letters and spaces.', file=stderr)
        r.status = False
        return r


     # street name must be valid here
    r.street_name = street_name

    # rm does not need coordiates, exit here
    if cmd == RM:
        if cord != '':
            print('Error rm cannot have more than 2 arguments', file=stderr)
            r.status = False
        return r

    if not cord:
        print(
            f'Error: Your coordinates: "{cord}" for {cmd} is invalid, try again.', file=stderr)
        r.status = False
        return r

    # processing coordinates
    li = []
    for match in re.findall(r'(?<=\().*?(?=\))', cord):
        a, b = map(float, match.split(','))
        # li.append([a, b]) # return raw

        # return a list of Nodes
        li.append(Node(a, b))

    if cmd == ADD:
        if len(li) <= 1:
            print(f'Error: for adding {r.__dict__}, {li}, {cord} you cannot have only 1 coordinate. ', file=sys.stderr)
            r.status = False
            return r

    r.coordinates = li
    return r


# if __name__ == '__main__':
    # invalid test:

    # print('unrecognized anything')
    # test = process_input('dasdasdas')
    # print(test.__dict__)
    #
    # print('unrecognized command')
    # test = process_input('   inspect     "weeber street"    (1,2)(3,4)')
    # print(test.__dict__)
    #
    # print('missing street and coordinates')
    # test = process_input('   add         ')
    # print(test.__dict__)
    #
    # print('missing coordinates')
    # test = process_input('   add     "w"    ')
    # print(test.__dict__)
    #
    # print('missing spaces')
    # test = process_input('add"w"(1,2)')
    # print(test.__dict__)
    #
    # # Valid test
    # # rm
    # print('rm')
    # test = process_input('   rm     "w"    ')
    # print(test.__dict__)
    #
    # print('add')
    # test = process_input('   add     "weeber street"    (1,2)(3,4)')
    # print(test.__dict__)
    #
    # print('mod')
    # test = process_input('   mod     "weeber street"    (1,2)(3,4)')
    # print(test.__dict__)
