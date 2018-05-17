from rply import ParserGenerator
from ast import (Number, Add, Sub, Mul, Div,
                 If, Statements, Bigger, Smaller,
                 Equal, Different, Attribution, VarDec,
                 Identifier)


class Parser():
    def __init__(self, builder, module):
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser.
            ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS',
             'PLUS', 'MINUS', 'MUL', 'DIV', 'IF',
             'BIGGER', 'SMALLER', 'EQUAL', 'DIFF',
             'OPEN_BRACKETS', 'CLOSE_BRACKETS', 'SEMI_COLON',
             'ATTRIBUTION', 'IDENTIFIER', 'VAR'
             ],
        )
        self.builder = builder
        self.module = module

    def parse(self):
        @self.pg.production('statement_list : statement SEMI_COLON')
        def statement_list_one(p):
            return Statements(self.builder, self.module, p[0])

        @self.pg.production('statement_list : statement_list statement SEMI_COLON')
        def statement_list_rest(p):
            p[0].add_child(p[1])
            return p[0]

        @self.pg.production('statement : IF OPEN_PARENS rel CLOSE_PARENS OPEN_BRACKETS statement_list CLOSE_BRACKETS')
        def statement_if(p):
            return If(self.builder, self.module, p[2], p[4])

        @self.pg.production('statement : VAR IDENTIFIER')
        def var_dec(p):
            return VarDec(self.builder, self.module, p[1])

        @self.pg.production('statement : IDENTIFIER ATTRIBUTION expr')
        def attribution(p):
            left = p[0]
            right = p[2]
            return Attribution(self.builder, self.module, left, right)

        @self.pg.production('rel : expr BIGGER expr')
        @self.pg.production('rel : expr SMALLER expr')
        @self.pg.production('rel : expr EQUAL expr')
        @self.pg.production('rel : expr DIFF expr')
        def rel(p):
            left = p[0]
            right = p[0]
            if p[1].gettokentype() == 'BIGGER':
                return Bigger(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'SMALLER':
                return Smaller(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'EQUAL':
                return Equal(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'DIFF':
                return Different(self.builder, self.module, left, right)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('statement : expr')
        def statement_expr(p):
            return p[0]

        @self.pg.production('expr : term PLUS term')
        @self.pg.production('expr : term MINUS term')
        def expr_binop(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'PLUS':
                return Add(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'MINUS':
                return Sub(self.builder, self.module, left, right)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('expr : term')
        def expr_term(p):
            return p[0]

        @self.pg.production('term : factor MUL factor')
        @self.pg.production('term : factor DIV factor')
        def term(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('term : factor')
        def term_factor(p):
            return p[0]

        @self.pg.production('factor : NUMBER')
        def factor_number(p):
            return Number(self.builder, self.module, p[0].getstr())

        @self.pg.production('factor : IDENTIFIER')
        def identifier(p):
            return Identifier(self.builder, self.module, p[0])

        @self.pg.production('factor : OPEN_PARENS expr CLOSE_PARENS')
        def expr_parens(p):
            return p[1]

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
