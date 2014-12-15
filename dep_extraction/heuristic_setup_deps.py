import re
import ast

OP_RE = re.compile(r'(<|<=|==|>=|>)')

def name_from_requirement(r):
    return OP_RE.split(r)[0]


def extract(setup_data, known_packages):
    for x in ast.walk(ast.parse(setup_data)):
        if not isinstance(x, ast.Str):
            continue
        name = name_from_requirement(x.s)
        if name in known_packages:
            yield name


def test_parse_requirements():
    in_ = [
        "requests", "pycrypto>=2.6.1", "pyjwkest>=0.5.1",
        "mako", "beaker", "alabaster", "pyOpenSSL"
    ]
    expected = [
        "requests", "pycrypto", "pyjwkest",
        "mako", "beaker", "alabaster", "pyOpenSSL"
    ]
    for x, exp in zip(in_, expected):
        assert exp == name_from_requirement(x)
