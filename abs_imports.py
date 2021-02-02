import ast
import argparse
import os
import re
from pathlib import Path

class Visitor(ast.NodeVisitor):
    def __init__(self, parts) -> None:
        self.parts = parts
        self.to_replace = {}

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level
        if level == 0 and node.module is not None:
            self.generic_visit(node)
            return

        to_correct = '.'.join(self.parts[:-level])

        if node.module is None:
            self.to_replace[
                node.lineno
            ] = (rf'(from\s+){"."*level}', f'\\1{to_correct}')
        else:
            module = node.module
            self.to_replace[
                node.lineno
            ] = (rf'(from\s+){"."*level}{module}', f'\\1{to_correct}.{module}')

        self.generic_visit(node)



def one_files(path, src):
    try:
        relative_path = Path(path).resolve().relative_to(src)
    except ValueError as exc:
        # raise error here!
        raise ValueError(f"File {path} cannot be resolved relative to {src}")

    with open(path) as fd:
        txt = fd.read()
    tree = ast.parse(txt)

    visitor = Visitor(relative_path.parts)
    visitor.visit(tree)

    if not visitor.to_replace:
        return
    newlines = []
    with open(path) as fd:
        for lineno, line in enumerate(fd, start=1):
            if lineno in visitor.to_replace:
                re1, re2 = visitor.to_replace[lineno]
                line = re.sub(re1, re2, line)
            newlines.append(line)


    with open(path, 'w', encoding='utf-8') as fd:
        fd.write(''.join(newlines))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default=os.getcwd())
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args(argv)
    for path in args.paths:
        one_files(path, args.src)

if __name__ == '__main__':
    main()
