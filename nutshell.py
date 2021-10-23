import os
import os.path

# custom exception
class NutshellException(BaseException):
    message: str

    def __init__(self, *args):
        self.message = f'nutshell: {": ".join(args)}'

    def __str__(self) -> str:
        return self.message

# prompt
prompt: str

if 'PS1' in os.environ:
    prompt = os.environ['PS1']
else:
    prompt = '$ '
    os.environ['PS1'] = prompt

# PATH
def search_path(program: str):
    for entry in os.environ['PATH'].split(';'):
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
