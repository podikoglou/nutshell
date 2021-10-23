import os
import os.path
from typing import Callable, List
from dataclasses import dataclass

# custom exception
class NutshellException(BaseException):
    def __str__(self) -> str:
        return f'nutshell: {": ".join(self.args)}'


# builtins
@dataclass
class Builtin:

    aliases: List[str]
    function: Callable[[List[str]], int]

class CdBuiltin(Builtin):

    def __init__(self):
        self.aliases = ['cd']
        self.function = self.execute

    def execute(self, args: List[str]) -> int:
        if not args:
            return 1

        if os.path.isdir(args[0]):
            return 1

        os.chdir(args[0])
        return 0

# prompt
prompt: str

if 'PS1' in os.environ:
    prompt = os.environ['PS1']
else:
    prompt = '$ '
    os.environ['PS1'] = prompt

# PATH
def search_path(program: str):
    for entry in os.environ['PATH'].split(':'):
        path = os.path.join(entry, program)

        if os.path.exists(path) and os.path.isfile(path):
            return path

# REPL
if __name__ == '__main__':
    while True:
        line = input(prompt)

        if not line.strip(' '):
            continue

        program = line.split(' ')[0]
        binary: str

        try:
            # if the program is a path
            if os.path.sep in program:

                # if the path exists
                if os.path.exists(program) and os.path.isfile(program):
                    binary = program

                # if it doesn't
                else:
                    raise NutshellException(program, 'not found')

            # if it's not
            else:

                path = search_path(program)

                # if the binary path was not returned (which means it doesn't exist)
                if path == None:
                    raise NutshellException(program, 'not found')

                # if it did
                else:
                    binary = path

            print(binary)
        except NutshellException as exception:
            print(exception)
