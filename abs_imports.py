import argparse
import ast
import os
import re
from pathlib import Path
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Tuple


class Visitor(ast.NodeVisitor):
    def __init__(self, parts: Sequence[str]) -> None:
        self.parts = parts
        self.to_replace: MutableMapping[int, Tuple[str, str]] = {}

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level
        if level == 0 and node.module is not None:
            self.generic_visit(node)
            return

        absolute_import = '.'.join(self.parts[:-level])

        if node.module is None:
            self.to_replace[
                node.lineno
            ] = (rf'(from\s+){"."*level}', f'\\1{absolute_import}')
        else:
            module = node.module
            self.to_replace[
                node.lineno
            ] = (
                rf'(from\s+){"."*level}{module}',
                f'\\1{absolute_import}.{module}',
            )

        self.generic_visit(node)


def absolute_imports(file: str, application_directories: str) -> None:
    srcs = application_directories.split(':')
    relative_path = file
    for i in srcs:
        if os.path.abspath(file).startswith(os.path.abspath(i)):
            relative_path = os.path.abspath(relative_path).replace(
                os.path.abspath(i), '',
            ).lstrip(os.sep)

    with open(file, encoding='utf-8') as fd:
        txt = fd.read()
    tree = ast.parse(txt)

    visitor = Visitor(Path(relative_path).parts)
    visitor.visit(tree)

    if not visitor.to_replace:
        return

    newlines = []
    with open(file, encoding='utf-8') as fd:
        for lineno, line in enumerate(fd, start=1):
            if lineno in visitor.to_replace:
                re1, re2 = visitor.to_replace[lineno]
                line = re.sub(re1, re2, line)
            newlines.append(line)
    with open(file, 'w', encoding='utf-8') as fd:
        fd.write(''.join(newlines))


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--application-directories', default=os.getcwd())
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(argv)
    for file in args.files:
        absolute_imports(file, args.application_directories)


if __name__ == '__main__':
    main()
