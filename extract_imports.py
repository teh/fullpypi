import ast
import os
import setuptools

def get_tli(dotted_path):
    """Returns the top-level import from the name."""
    return dotted_path.split('.', 2)[0]
    

def extract_tlis(root):
    tl_imports = set(
        get_tli(import_)
        for path in python_files(root)
        for import_ in extract_imports(path))
    provided = set(get_tli(x) for x in setuptools.find_packages(root))
    return tl_imports, provided


def main():
    tl_imports, provided = extract_tlis('/tmp/scipy-0.14.0')
    print tl_imports - provided
    

def extract_imports(path):
    try:
        tree = ast.parse(open(path).read())
    except SyntaxError:
        yield SyntaxError, None

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level > 0:
                continue
            yield node.module
        if isinstance(node, ast.Import):
            yield node.names[0].name

        
def python_files(root):
    for path, _, filenames in os.walk(root):
        for x in filenames:
            if not x.endswith('.py'):
                continue
            yield os.path.join(path, x)


if __name__ == '__main__':
    main()
