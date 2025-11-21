import argparse
import sys
from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional
from typing import Set


def get_files_recursive(
    directory: Path,
    exclude_dirs: Set[str]
) -> Generator[Path, None, None]:
    try:
        for item in directory.iterdir():
            if item.is_dir():
                if item.name in exclude_dirs:
                    continue
                yield from get_files_recursive(item, exclude_dirs)
            elif item.is_file():
                yield item
    except PermissionError:
        pass


def collect_files(
    root_dir: Path,
    output_file: Path,
    extensions: Optional[List[str]],
    exclude_dirs: Optional[List[str]]
) -> None:
    excludes = set(exclude_dirs) if exclude_dirs else set()
    valid_extensions = None

    if extensions:
        valid_extensions = {
            f".{ext.lstrip('.')}" for ext in extensions
        }

    with output_file.open('w', encoding='utf-8') as outfile:
        for file_path in get_files_recursive(root_dir, excludes):
            if valid_extensions and file_path.suffix not in valid_extensions:
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                outfile.write(f'{file_path}\n')
                outfile.write('===\n')
                outfile.write(content)
                outfile.write('\n===\n\n')
            except (UnicodeDecodeError, PermissionError):
                continue


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'root',
        type=Path
    )

    parser.add_argument(
        '-o',
        '--output',
        type=Path,
        default=None
    )

    parser.add_argument(
        '-e',
        '--extension',
        action='append',
        dest='extensions',
        default=[]
    )

    parser.add_argument(
        '-x',
        '--exclude',
        action='append',
        dest='exclude',
        default=[]
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    root_path: Path = args.root.resolve()

    if not root_path.exists():
        sys.exit(1)

    output_path: Path
    if args.output:
        output_path = args.output
    else:
        output_path = root_path.with_name(f'{root_path.name}.txt')

    collect_files(
        root_path,
        output_path,
        args.extensions,
        args.exclude
    )


if __name__ == '__main__':
    main()
