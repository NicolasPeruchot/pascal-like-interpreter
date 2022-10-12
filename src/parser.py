import ast

import rply


pg = rply.ParserGenerator(
    [
        "INT",
        "PRINT",
        "VAR",
        "LPAR",
        "RPAR",
        "ADD",
        "MINUS",
        "MULTIPLY",
        "DIVIDE",
        "MOD",
        "FUNC",
        "FUNC_NAME",
        "IF",
        "THEN",
        "ELSE",
        "WHILE",
        "RETURN",
        "LCB",
        "RCB",
        "ASSIGN",
        "EQUAL",
        "NEQUAL",
        "INF",
        "SUP",
        "SEMI",
    ],
    precedence=[
        (
            "left",
            [
                "WHILE",
            ],
        ),
        (
            "left",
            [
                "EQUAL",
            ],
        ),
        (
            "right",
            [
                "ELSE",
            ],
        ),
        (
            "left",
            [
                "SEMI",
            ],
        ),
        ("left", ["ASSIGN"]),
        ("left", ["PRINT"]),
        ("left", ["ADD", "MINUS"]),
        ("left", ["DIVIDE", "MULTIPLY"]),
        (
            "left",
            [
                "MOD",
            ],
        ),
    ],
)


# Point de départ : un programme est une liste d'instructions
@pg.production("program : list_inst")
def prod0(p):
    result = []

    def nested(L):
        for x in L:
            if type(x) != list:
                result.append(x)
            else:
                nested(x)
        return result

    if type(p[0]) == list:
        nested(p[0])
    else:
        result = [p[0]]
    for i in range(len(result)):
        if isinstance(result[i], ast.Constant):
            result[i] = ast.Expr(value=result[i])

    return ast.Module(body=result, type_ignores=[])


@pg.production("list_inst : VAR")
def expression(p):
    return ast.Name(id=p[0].getstr(), ctx=ast.Load())


@pg.production("list_inst : INT")
def expression(p):
    return ast.Constant(value=int(p[0].value))


@pg.production("list_inst : PRINT LPAR list_inst RPAR")
def expression(p):
    return ast.Expr(
        value=ast.Call(func=ast.Name(id="print", ctx=ast.Load()), args=[p[2]], keywords=[])
    )


@pg.production("list_inst : list_inst ADD list_inst")
def expression(p):
    return ast.BinOp(left=p[0], op=ast.Add(), right=p[2])


@pg.production("list_inst : list_inst MINUS list_inst")
def expression(p):
    return ast.BinOp(left=p[0], op=ast.Sub(), right=p[2])


@pg.production("list_inst : list_inst MULTIPLY list_inst")
def expression(p):
    return ast.BinOp(left=p[0], op=ast.Mult(), right=p[2])


@pg.production("list_inst : list_inst DIVIDE list_inst")
def expression(p):
    return ast.BinOp(left=p[0], op=ast.Div(), right=p[2])


@pg.production("list_inst : list_inst MOD list_inst")
def expression(p):
    return ast.BinOp(left=p[0], op=ast.Mod(), right=p[2])


@pg.production("list_inst : list_inst EQUAL list_inst")
def expression(p):
    return ast.Compare(left=p[0], ops=[ast.Eq()], comparators=[p[2]])


@pg.production("list_inst : list_inst NEQUAL list_inst")
def expression(p):
    return ast.Compare(left=p[0], ops=[ast.NotEq()], comparators=[p[2]])


@pg.production("list_inst : list_inst INF list_inst")
def expression(p):
    return ast.Compare(left=p[0], op=ast.Mod(), ops=[ast.Lt()], comparators=[p[2]])


@pg.production("list_inst : list_inst SUP list_inst")
def expression(p):
    return ast.Compare(left=p[0], op=ast.Mod(), ops=[ast.Gt()], comparators=[p[2]])


@pg.production("list_inst : list_inst ASSIGN list_inst")
def expression(p):
    return ast.Assign(targets=[ast.Name(id=p[0].id, ctx=ast.Store())], value=p[2])


@pg.production("list_inst : WHILE LPAR list_inst RPAR LCB list_inst RCB")
def expression(p):
    x = p[5] if type(p[5]) == list else [p[5]]
    return ast.While(test=p[2], body=x, orelse=[])


@pg.production("list_inst : list_inst SEMI list_inst")
def semi(p):
    return [p[0], p[2]]


@pg.production("list_inst : FUNC FUNC_NAME LPAR list_inst RPAR LCB list_inst RCB")
def expression(p):
    x = p[6] if type(p[6]) == list else [p[6]]
    return ast.FunctionDef(
        name=p[1].getstr(),
        args=ast.arguments(
            posonlyargs=[], args=[ast.arg(arg=p[3].id)], kwonlyargs=[], kw_defaults=[], defaults=[]
        ),
        body=x,
        decorator_list=[],
    )


@pg.production("list_inst : RETURN list_inst")
def expression(p):
    return ast.Return(value=p[1])


@pg.production("list_inst : IF LPAR list_inst RPAR THEN LCB list_inst RCB ELSE LCB list_inst RCB")
def expression(p):
    x = p[6] if type(p[6]) == list else [p[6]]
    y = p[10] if type(p[10]) == list else [p[10]]
    return ast.If(test=p[2], body=x, orelse=y)


@pg.production("list_inst : IF LPAR list_inst RPAR THEN LCB list_inst RCB ELSE LCB list_inst RCB")
def expression(p):
    x = p[6] if type(p[6]) == list else [p[6]]

    y = p[10] if type(p[10]) == list else [p[10]]

    return ast.If(test=p[2], body=x, orelse=p[10])


@pg.production("list_inst : IF LPAR list_inst RPAR THEN LCB list_inst RCB ")
def expression(p):
    x = p[6] if type(p[6]) == list else [p[6]]

    return ast.If(test=p[2], body=x, orelse=[])


parser = pg.build()
