import argparse
import io
import os
import sys
import tokenize


def remove_comments(source):
    """
    Removes comments from Python source code while preserving #TODO and # noqa.
    Uses tokenize for safe parsing (ignores hashes inside strings).
    """
    try:
        original_lines = source.splitlines(keepends=True)

        io_obj = io.StringIO(source)
        tokens = list(tokenize.generate_tokens(io_obj.readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return source

    to_remove = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            lowercased = tok.string.lower()
            # Exception check: preserve TODO and noqa
            if 'todo' not in lowercased and 'noqa' not in lowercased:
                to_remove.append(tok)

    for tok in reversed(to_remove):
        start_line, start_col = tok.start

        line_idx = start_line - 1

        if line_idx >= len(original_lines):
            continue

        line = original_lines[line_idx]
        prefix = line[:start_col]

        if prefix.strip() == '':
            original_lines.pop(line_idx)
        else:
            line_ending = ''
            if line.endswith('\r\n'):
                line_ending = '\r\n'
            elif line.endswith('\n'):
                line_ending = '\n'

            new_line = prefix.rstrip() + line_ending
            original_lines[line_idx] = new_line

    return ''.join(original_lines)


def process_file(path, dry_run=False):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return False

        cleaned_content = remove_comments(content)

        if content != cleaned_content:
            if dry_run:
                print(f'[DRY RUN] Would update: {path}')
            else:
                print(f'Updated: {path}')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
            return True
        return False
    except Exception as e:
        print(f'Error processing {path}: {e}')
        return False


def process_directory(directory, dry_run=False):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                if process_file(os.path.join(root, file), dry_run):
                    count += 1
    print(f'\nFinished. Total files modified: {count}')


def main():
    desc = ('Recursively remove comments from Python files '
            '(preserves #TODO and # noqa).')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('path', help='Target directory or file')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show changes without applying them')

    args = parser.parse_args()

    if os.path.exists(args.path):
        if os.path.isdir(args.path):
            process_directory(args.path, dry_run=args.dry_run)
        else:
            process_file(args.path, dry_run=args.dry_run)
    else:
        print(f'Error: {args.path} does not exist')
        sys.exit(1)


if __name__ == '__main__':
    main()
