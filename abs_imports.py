import argparse
import ast
import re
from pathlib import Path
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Tuple


class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            parts: Sequence[str],
            keep_local_imports_relative: bool,
    ) -> None:
        self.parts = parts
        self.to_replace: MutableMapping[int, Tuple[str, str]] = {}
        self.keep_local_imports_relative = keep_local_imports_relative

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level
        if not self.keep_local_imports_relative and level == 0:
            # Already absolute import.
            self.generic_visit(node)
            return

        if self.keep_local_imports_relative and level == 1:
            # Should be relative, and already is.
            self.generic_visit(node)
            return

        if (
            self.keep_local_imports_relative
            and level == 0
            and node.module is not None
            and not node.module.startswith(self.parts[0])
        ):
            # Third-party import
            self.generic_visit(node)
            return

        should_be_relative = self.keep_local_imports_relative and level == 0
        if should_be_relative:
            if node.module == '.'.join(self.parts[:-1]):
                # e.g. from a.b import c -> from . import c
                replacement = '\\1.'
            else:
                # e.g. from a.b.c import d -> from .c import d
                replacement = '\\1'
            self.to_replace[node.lineno] = (
                rf'(from\s+){".".join(self.parts[:-1])}',
                replacement,
            )
            self.generic_visit(node)
            return

        absolute_import = '.'.join(self.parts[:-level])

        if node.module is None:
            # e.g. from . import b
            self.to_replace[
                node.lineno
            ] = (rf'(from\s+){"."*level}', f'\\1{absolute_import}')
        else:
            # e.g. from .b import c
            module = node.module
            self.to_replace[
                node.lineno
            ] = (
                rf'(from\s+){"."*level}{module}',
                f'\\1{absolute_import}.{module}',
            )

        self.generic_visit(node)


def absolute_imports(
        file: str,
        srcs: Sequence[str],
        *,
        keep_local_imports_relative: bool = False,
) -> None:
    relative_path = Path(file)
    for i in srcs:
        try:
            relative_path = relative_path.resolve().relative_to(i)
        except ValueError:
            # `relative_path` can't be resolved relative to `i`
            pass

    with open(file, encoding='utf-8') as fd:
        txt = fd.read()
    tree = ast.parse(txt)

    visitor = Visitor(relative_path.parts, keep_local_imports_relative)
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
    parser.add_argument('--application-directories', default='.:src')
    parser.add_argument('files', nargs='*')
    parser.add_argument('--keep-local-imports-relative', action='store_true')
    args = parser.parse_args(argv)

    srcs = [
        str(Path(i).resolve())
        for i in args.application_directories.split(':')
    ]

    for file in args.files:
        absolute_imports(
            file,
            srcs,
            keep_local_imports_relative=args.keep_local_imports_relative,
        )


if __name__ == '__main__':
    main()
