import ast

from src.lexer import lexer
from src.parser import parser


def translation(prog):
    expr = parser.parse(lexer.lex(prog))
    ast.fix_missing_locations(expr)
    exe = compile(expr, "<AST>", "exec")
    return exe
