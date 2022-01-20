import argparse
import ast
import os
import re
from pathlib import Path
from typing import Iterable
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Tuple


def _find_relative_depth(parts: Sequence[str], module: str) -> int:
    depth = 0
    for n, _ in enumerate(parts, start=1):
        if module.startswith('.'.join(parts[:n])):
            depth += 1
        else:
            break
    return depth


class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            parts: Sequence[str],
            srcs: Iterable[str],
            *,
            never: bool,
    ) -> None:
        self.parts = parts
        self.srcs = srcs
        self.to_replace: MutableMapping[int, Tuple[str, str]] = {}
        self.never = never

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level
        is_absolute = level == 0
        absolute_import = '.'.join(self.parts[:-level])

        should_be_relative = bool(self.never)
        if is_absolute ^ should_be_relative:
            self.generic_visit(node)
            return

        def is_python_file_or_dir(path: str) -> bool:
            return os.path.exists(path+'.py') or os.path.isdir(path)

        if should_be_relative:
            assert node.module is not None  # help mypy
            if not any(
                is_python_file_or_dir(
                    os.path.join(src, *node.module.split('.')),
                ) for src in self.srcs
            ):
                # Can't convert to relative, might be third-party
                return
            depth = _find_relative_depth(self.parts, node.module)
            if depth == 0:
                # don't attempt relative import beyond top-level package
                return
            inverse_depth = len(self.parts) - depth
            if node.module == '.'.join(self.parts[:depth]):
                n_dots = inverse_depth
            else:
                # e.g. from a.b.c import d -> from ..c import d
                n_dots = inverse_depth - 1
            replacement = f'\\1{"."*n_dots}'

            self.to_replace[node.lineno] = (
                rf'(from\s+){".".join(self.parts[:depth])}',
                replacement,
            )
            self.generic_visit(node)
            return

        if node.module is None:
            # e.g. from . import b
            self.to_replace[
                node.lineno
            ] = (rf'(from\s+){"."*level}\s*', f'\\1{absolute_import} ')
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
        srcs: Iterable[str],
        *,
        never: bool = False,
) -> int:
    relative_paths = []
    possible_srcs = []
    path = Path(file).resolve()
    for src in srcs:
        try:
            path_relative_to_i = path.relative_to(src)
        except ValueError:
            # `relative_path` can't be resolved relative to `i`
            pass
        else:
            relative_paths.append(path_relative_to_i)
            possible_srcs.append(src)
    if not relative_paths:
        raise ValueError(
            f'{file} can\'t be resolved relative to the current directory.\n'
            'Either run absolufy-imports from the project root, or pass\n'
            '--application-directories',
        )
    relative_path = min(relative_paths, key=lambda x: len(x.parts))

    with open(file, 'rb') as fb:
        contents_bytes = fb.read()
    try:
        contents_text = contents_bytes.decode()
    except UnicodeDecodeError:
        print(f'{file} is non-utf-8 (not supported)')
        return 1
    try:
        tree = ast.parse(contents_text)
    except SyntaxError:
        return 0

    visitor = Visitor(
        relative_path.parts,
        srcs,
        never=never,
    )
    visitor.visit(tree)

    if not visitor.to_replace:
        return 0

    newlines = []
    for lineno, line in enumerate(
        contents_text.splitlines(keepends=True), start=1,
    ):
        if lineno in visitor.to_replace:
            re1, re2 = visitor.to_replace[lineno]
            line = re.sub(re1, re2, line)
        newlines.append(line)
    with open(file, 'w', encoding='utf-8', newline='') as fd:
        fd.write(''.join(newlines))
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--application-directories', default='.:src')
    parser.add_argument('files', nargs='*')
    parser.add_argument('--never', action='store_true')
    args = parser.parse_args(argv)

    srcs = [
        str(Path(i).resolve())
        for i in args.application_directories.split(':')
    ]
    ret = 0
    for file in args.files:
        ret |= absolute_imports(
            file,
            srcs,
            never=args.never,
        )
    return ret


if __name__ == '__main__':
    main()
