from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('NUMBER', r'\d+')
        # Operators
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        # Comp
        self.lexer.add('BIGGER', r'\>')
        self.lexer.add('SMALLER', r'\<')
        self.lexer.add('EQUAL', r'\=')
        self.lexer.add('DIFF', r'\!=')
        self.lexer.add('OPEN_PARENS', r'\(')
        self.lexer.add('CLOSE_PARENS', r'\)')
        self.lexer.add('OPEN_BRACKETS', r'\{')
        self.lexer.add('CLOSE_BRACKETS', r'\}')
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('QUOTE', r'\"')
        # Vars
        self.lexer.add('ATTRIBUTION', r':=')
        self.lexer.add('VAR', r'var')
        # Else
        self.lexer.add('ELSE', r'SENAO')
        self.lexer.add('ELSE', r'senao')
        # If
        self.lexer.add('IF', r'SE')
        self.lexer.add('IF', r'se')
        # Print
        self.lexer.add('PRINT', r'PRINT')
        self.lexer.add('PRINT', r'print')
        # Identifier
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z_0-9]*')
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
