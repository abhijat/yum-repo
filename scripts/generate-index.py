import os.path

HEADER = """<!DOCTYPE html>
<html>
<body>
"""

FOOTER = """</body>
</html>
"""

SKIP = {".gitignore", "./.github", "./.git", "./scripts", "index.html"}


def parse_gitignore():
    with open(".gitignore") as f:
        for row in f.readlines():
            SKIP.add(f"./{row.strip()}")


def build_index(dirpath):
    target = os.path.join(dirpath, "index.html")
    with open(target, 'w') as f:
        f.write(HEADER.format(dir=dirpath))
        for item in sorted(os.listdir(dirpath)):
            if any(item in x for x in SKIP):
                continue
            name = item + "/" if os.path.isdir(os.path.join(dirpath, item)) else item
            f.write(f"""<a href="{item}">{name}</a><br>\n""")
        f.write(FOOTER)


def recurse_dir(root):
    for root, dirs, _ in os.walk(root):
        if not any(root.startswith(x) for x in SKIP):
            build_index(root)


if __name__ == '__main__':
    parse_gitignore()
    recurse_dir(".")
