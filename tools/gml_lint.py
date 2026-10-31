"""
gml_lint.py - static checks for the project's GML (no compiler is available without a licence).

Checks every scripts/*/*.gml and objects/*/*.gml file for:
  * unbalanced (), [], {} and unterminated strings/comments
  * calls to functions that are neither GML built-ins (runtime GmlSpec.xml), project script
    functions, nor local method variables
  * argument counts outside the built-in / script signature (variadic "..." respected)
  * bare resource-looking identifiers (spr_/snd_/obj_/rm_/fnt_/ts_/seq_) that are not resources
  * unparenthesised chained ternaries (a ? b : c ? d : e), a GML parse error
  * duplicate script function names
This is not a compiler: it cannot prove type correctness or runtime behaviour.

  python tools/gml_lint.py            -> prints findings, exit 1 when any error exists
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
import gmyy  # noqa: E402

P = gmyy.PROJ
SPEC = r"C:\ProgramData\GameMakerStudio2-LTS2026\Cache\runtimes\runtime-2026.0.0.23\GmlSpec.xml"
KEYWORDS = {"if", "else", "while", "for", "do", "until", "repeat", "switch", "case", "default", "break",
            "continue", "return", "exit", "with", "var", "globalvar", "function", "new", "delete", "try",
            "catch", "finally", "throw", "enum", "static", "and", "or", "not", "xor", "div", "mod", "begin", "end",
            "then", "self", "other", "all", "noone", "global", "true", "false", "undefined", "pointer_null",
            "infinity", "NaN", "constructor"}
RES_PREFIX = ("spr_", "snd_", "obj_", "rm_", "fnt_", "ts_", "seq_", "mus_")


def load_spec():
    root = ET.parse(SPEC).getroot()
    funcs = {}
    for f in root.iter("Function"):
        params = f.findall("Parameter")
        req = 0
        mx = 0
        var = False
        for p in params:
            if p.get("Name") == "...":
                var = True
                continue
            mx += 1
            if p.get("Optional") != "true":
                req += 1
        funcs[f.get("Name")] = (req, None if var else mx)
    names = set(funcs)
    for c in root.iter("Constant"):
        names.add(c.get("Name"))
    for v in root.iter("Variable"):
        names.add(v.get("Name"))
    return funcs, names


def strip(code):
    """remove comments and string contents (keeps quotes) while keeping line structure."""
    out = []
    i, n = 0, len(code)
    errs = []
    line = 1
    while i < n:
        c = code[i]
        if c == "\n":
            line += 1
        if code.startswith("//", i):
            j = code.find("\n", i)
            j = n if j < 0 else j
            i = j
            continue
        if code.startswith("/*", i):
            j = code.find("*/", i + 2)
            if j < 0:
                errs.append((line, "unterminated block comment"))
                break
            out.append("\n" * code.count("\n", i, j))
            line += code.count("\n", i, j)
            i = j + 2
            continue
        if c in "\"'":
            q = c
            j = i + 1
            while j < n and code[j] != q:
                if code[j] == "\\":
                    j += 1
                if code[j] == "\n":
                    errs.append((line, "newline in string"))
                    break
                j += 1
            out.append(q + q)
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out), errs


def split_args(s, start):
    """s[start] is '(' ; returns (argcount, end_index)."""
    depth = 0
    count = 0
    seen = False
    i = start
    while i < len(s):
        c = s[i]
        if c in "([{":
            depth += 1
            if depth > 1:
                seen = True
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                return (count + 1 if seen else 0), i
        elif c == "," and depth == 1:
            count += 1
            seen = True
        elif depth == 1 and not c.isspace():
            seen = True
        i += 1
    return count, i


def main():
    funcs, builtin_names = load_spec()
    with open(gmyy.YYP, encoding="utf-8") as f:
        yyp = gmyy.gm_loads(f.read())
    resources = {r["id"]["name"] for r in yyp["resources"]}
    files = sorted(glob.glob(os.path.join(P, "scripts", "*", "*.gml")) +
                   glob.glob(os.path.join(P, "objects", "*", "*.gml")) +
                   glob.glob(os.path.join(P, "rooms", "*", "*.gml")))
    stripped = {}
    errors, warnings = [], []
    user = {}
    macros = set()
    enums = set()
    for fp in files:
        code = open(fp, encoding="utf-8").read()
        s, errs = strip(code)
        for ln, e in errs:
            errors.append("%s:%d: %s" % (fp, ln, e))
        stripped[fp] = s
        for m in re.finditer(r"#macro\s+(\w+)", code):
            macros.add(m.group(1))
        for m in re.finditer(r"\benum\s+(\w+)", s):
            enums.add(m.group(1))
        if "/scripts/" in fp.replace("\\", "/"):
            for m in re.finditer(r"^function\s+(\w+)\s*\(([^)]*)\)", s, re.M):
                name = m.group(1)
                params = [p.strip() for p in m.group(2).split(",") if p.strip()]
                req = sum(1 for p in params if "=" not in p)
                if name in user:
                    errors.append("%s: duplicate function %s" % (fp, name))
                user[name] = (req, len(params))
    known_calls = set(funcs) | set(user)
    for fp, s in stripped.items():
        rel = os.path.relpath(fp, P)
        # balance
        stack = []
        line = 1
        pairs = {")": "(", "]": "[", "}": "{"}
        for ch in s:
            if ch == "\n":
                line += 1
            elif ch in "([{":
                stack.append((ch, line))
            elif ch in ")]}":
                if not stack or stack[-1][0] != pairs[ch]:
                    errors.append("%s:%d: unbalanced '%s'" % (rel, line, ch))
                    break
                stack.pop()
        if stack:
            errors.append("%s:%d: unclosed '%s'" % (rel, stack[-1][1], stack[-1][0]))
        locals_ = set(re.findall(r"\bvar\s+(\w+)", s))
        locals_ |= set(re.findall(r"\bfunction\s*\w*\s*\(([^)]*)\)", s) and
                       [p.split("=")[0].strip() for grp in re.findall(r"\bfunction\s*\w*\s*\(([^)]*)\)", s) for p in grp.split(",")])
        # calls
        for m in re.finditer(r"(?<![\w.$#])([A-Za-z_]\w*)\s*\(", s):
            name = m.group(1)
            if name in KEYWORDS or name in locals_:
                continue
            ln = s.count("\n", 0, m.start()) + 1
            if name not in known_calls:
                if name in resources or name in macros:
                    continue
                errors.append("%s:%d: unknown function '%s'" % (rel, ln, name))
                continue
            argc, _ = split_args(s, m.end() - 1)
            if name in funcs and name not in user:
                req, mx = funcs[name]
            else:
                req, mx = user[name]
            if argc < req or (mx is not None and argc > mx):
                errors.append("%s:%d: %s() takes %s..%s args, got %d" % (rel, ln, name, req, mx, argc))
        # bare resource identifiers
        for m in re.finditer(r"(?<![\w.\"$])((?:spr|snd|obj|rm|fnt|ts|seq|mus)_\w+)", s):
            name = m.group(1)
            if name in resources or name in macros or name in known_calls:
                continue
            ln = s.count("\n", 0, m.start()) + 1
            errors.append("%s:%d: unknown resource '%s'" % (rel, ln, name))
        # chained ternary without parentheses (heuristic on single statements)
        for ln_i, ln_txt in enumerate(s.split("\n"), 1):
            if re.search(r"\?[^;:()]*:[^;()]*\?", ln_txt):
                warnings.append("%s:%d: possible unparenthesised chained ternary" % (rel, ln_i))
        # enum member references
        for m in re.finditer(r"\b(MODE|OV|CELL)\.(\w+)", s):
            pass
    for e in errors:
        print("ERROR", e)
    for w in warnings:
        print("WARN ", w)
    print("files: %d, script functions: %d, errors: %d, warnings: %d" % (len(files), len(user), len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
