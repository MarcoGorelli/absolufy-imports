import argparse
import ast
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Tuple


def _find_relative_depth(parts: Sequence[str], module: str) -> int:
    depth = 0
    for n, _ in enumerate(parts, start=1):
        if module.startswith('.'.join(parts[:n])):
            depth += 1
            continue
    return depth


def _get_submodule(path: str, submodules: Iterable[str]) -> Optional[str]:
    submodule: Optional[str]
    for i in submodules:
        if path.startswith(i):
            submodule = i
            break
    else:
        submodule = None
    return submodule


class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            parts: Sequence[str],
            submodules: Iterable[str],
            *,
            keep_local_imports_relative: bool,
            keep_submodules_relative: bool,
    ) -> None:
        self.parts = parts
        self.submodules = submodules
        self.keep_local_imports_relative = keep_local_imports_relative
        self.keep_submodules_relative = keep_submodules_relative
        self.to_replace: MutableMapping[int, Tuple[str, str]] = {}

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level
        if (
            not self.keep_local_imports_relative
            and not self.keep_submodules_relative
            and level == 0
        ):
            # Should be absolute, already is.
            self.generic_visit(node)
            return

        if self.keep_local_imports_relative and level == 1:
            # Should be relative, and already is.
            self.generic_visit(node)
            return

        should_be_relative = False
        if self.keep_submodules_relative:
            absolute_import = '.'.join(self.parts[:-level])
            file_submodule = _get_submodule(
                '.'.join(self.parts), self.submodules,
            )
            if level == 0:
                assert node.module is not None  # can't have `from import`, but
                # mypy doesn't know that
                import_submodule = _get_submodule(node.module, self.submodules)
            else:
                import_submodule = _get_submodule(
                    absolute_import, self.submodules,
                )
            should_be_relative = (
                file_submodule is not None
                and file_submodule == import_submodule
            )

        if self.keep_submodules_relative and level > 0 and should_be_relative:
            # should be relative within submodule, already is
            self.generic_visit(node)
            return

        if (
            self.keep_submodules_relative
            and level == 0
            and not should_be_relative
        ):
            # should be absolute, already is
            self.generic_visit(node)
            return

        if self.keep_local_imports_relative:
            should_be_relative = (
                self.keep_local_imports_relative
                and level == 0
            )

        if (
            should_be_relative
            and level == 0
            and node.module is not None
            and not node.module.startswith(self.parts[0])
        ):
            # Third-party import
            self.generic_visit(node)
            return

        if should_be_relative:
            assert node.module is not None  # If the import
            # was already relative, we'd have returned already.
            # So it must be absolute, meaning that node.module can't
            # be None.
            depth = _find_relative_depth(self.parts, node.module)
            inverse_depth = len(self.parts) - depth
            if node.module == '.'.join(self.parts[:depth]):
                # e.g. from a.b import c -> import . import c
                n_dots = inverse_depth
            else:
                # e.g. from a.b.c import d -> from .. import c
                n_dots = inverse_depth - 1
            replacement = f'\\1{"."*n_dots}'

            self.to_replace[node.lineno] = (
                rf'(from\s+){".".join(self.parts[:depth])}',
                replacement,
            )
            self.generic_visit(node)
            return

        absolute_import = '.'.join(self.parts[:-level])

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
        submodules: Mapping[str, Iterable[str]],
        *,
        keep_local_imports_relative: bool = False,
        keep_submodules_relative: bool = False,
) -> None:
    relative_paths = []
    possible_srcs = []
    path = Path(file).resolve()
    for i in srcs:
        try:
            path_relative_to_i = path.relative_to(i)
        except ValueError:
            # `relative_path` can't be resolved relative to `i`
            pass
        else:
            relative_paths.append(path_relative_to_i)
            possible_srcs.append(i)
    relative_path = min(relative_paths, key=lambda x: len(x.parts))
    src = possible_srcs[relative_paths.index(relative_path)]

    with open(file, encoding='utf-8') as fd:
        txt = fd.read()
    tree = ast.parse(txt)

    visitor = Visitor(
        relative_path.parts,
        submodules[src],
        keep_local_imports_relative=keep_local_imports_relative,
        keep_submodules_relative=keep_submodules_relative,
    )
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
    parser.add_argument('--keep-submodules-relative', action='store_true')
    parser.add_argument('--submodules', required=False, type=json.loads)
    args = parser.parse_args(argv)

    srcs = {
        str(Path(i).resolve())
        for i in args.application_directories.split(':')
    }

    submodules = defaultdict(list)
    if args.keep_submodules_relative and not args.submodules:
        existing_srcs = (src for src in srcs if os.path.exists(src))
        packages = (
            (src, pkg)
            for src in existing_srcs
            for pkg in os.listdir(src)
            if os.path.isdir(pkg)
        )
        for src, package in packages:
            for submodule in os.listdir(package):
                submodules[src].append(f'{package}.{submodule}')
    elif args.keep_submodules_relative:
        for key, val in args.submodules.items():
            submodules[str(Path(key).resolve())] = val

    for file in args.files:
        absolute_imports(
            file,
            srcs,
            submodules,
            keep_local_imports_relative=args.keep_local_imports_relative,
            keep_submodules_relative=args.keep_submodules_relative,
        )


if __name__ == '__main__':
    main()
