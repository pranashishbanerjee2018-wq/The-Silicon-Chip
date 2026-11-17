import os
import re

js_files = []
for root, dirs, files in os.walk('static/js'):
    for f in files:
        if f.endswith('.js'):
            js_files.append(os.path.join(root, f))

print(f"Checking {len(js_files)} JS files for balanced braces and basic syntax...")

def check_brackets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Strip comments and strings to check structural brackets
    # Simple tokenizer
    i = 0
    n = len(code)
    stack = []
    line = 1
    col = 1

    while i < n:
        c = code[i]
        if c == '\n':
            line += 1
            col = 1
            i += 1
            continue

        # Single line comment
        if c == '/' and i + 1 < n and code[i+1] == '/':
            while i < n and code[i] != '\n':
                i += 1
            continue

        # Multi line comment
        if c == '/' and i + 1 < n and code[i+1] == '*':
            i += 2
            while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
                if code[i] == '\n':
                    line += 1
                    col = 1
                i += 1
            i += 2
            continue

        # String single quote
        if c == "'":
            i += 1
            while i < n and code[i] != "'":
                if code[i] == '\\':
                    i += 1
                elif code[i] == '\n':
                    line += 1
                    col = 1
                i += 1
            i += 1
            continue

        # String double quote
        if c == '"':
            i += 1
            while i < n and code[i] != '"':
                if code[i] == '\\':
                    i += 1
                elif code[i] == '\n':
                    line += 1
                    col = 1
                i += 1
            i += 1
            continue

        # Template literal
        if c == '`':
            i += 1
            while i < n and code[i] != '`':
                if code[i] == '\\':
                    i += 1
                elif code[i] == '\n':
                    line += 1
                    col = 1
                i += 1
            i += 1
            continue

        # Brackets
        if c in '({[':
            stack.append((c, line, col))
        elif c in ')}]':
            if not stack:
                return f"Unmatched closing '{c}' at line {line}, col {col}"
            last, l_line, l_col = stack.pop()
            matches = {')': '(', '}': '{', ']': '['}
            if matches[c] != last:
                return f"Mismatched bracket: expected '{last}' closed, got '{c}' at line {line}, col {col} (opened at line {l_line})"

        i += 1
        col += 1

    if stack:
        last, l_line, l_col = stack[-1]
        return f"Unclosed '{last}' opened at line {l_line}, col {l_col}"

    return "OK"

for jf in sorted(js_files):
    res = check_brackets(jf)
    print(f"[{'PASS' if res == 'OK' else 'FAIL'}] {jf}: {res}")
