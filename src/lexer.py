import ast
import warnings

import rply


warnings.filterwarnings("ignore")


lg = rply.LexerGenerator()

lg.add("PRINT", r"\bprint\b")
lg.add("VAR", r"\b(?<!function )(?!(return|if|then|else|function|while)\b)[a-zA-Z]+\b")
lg.add("INT", r"\d+")
lg.add("ADD", r"\+")
lg.add("MINUS", r"-")
lg.add("MULTIPLY", r"\*")
lg.add("DIVIDE", r"/")
lg.add("MOD", r"%")

lg.add("LPAR", r"\(")
lg.add("RPAR", r"\)")

lg.add("FUNC", r"\bfunction\b")
lg.add("FUNC_NAME", r"(?<=function )[a-zA-Z|\d]*")
lg.add("IF", r"\bif\b")
lg.add("THEN", r"\bthen\b")
lg.add("ELSE", r"\belse\b")
lg.add("WHILE", r"\bwhile\b")
lg.add("RETURN", r"\breturn\b")


lg.add("LCB", r"[{]")
lg.add("RCB", r"[}]")

lg.add("ASSIGN", r":=")
lg.add("EQUAL", r"==")
lg.add("NEQUAL", r"!=")
lg.add("INF", r"<")
lg.add("SUP", r">")

lg.add("SEMI", r";")

lg.ignore(r"\s+")

lexer = lg.build()
