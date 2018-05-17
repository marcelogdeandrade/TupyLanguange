program
   : statement+
   ;

statement
   : 'SE' rel 'ENTAO' '{' statement+ '}'
   | 'SE' rel 'ENTAO' '{' statement+ '}' 'SENAO' '{' statement+ '}'
   | expr ';'
   ;

rel
   : expr '<' expr
   | expr '>' expr
   | expr '=' expr
   | expr '!=' expr
   ;

expr
   : term '+' term
   | term '-' term
   ;

term
   : factor '*' factor
   | factor '/' factor

factor
   : number
   | ide
   | '(' expr ')'

ide
   : STRING

number
   : FLOAT


STRING
   : [a-z]+


FLOAT
   : DIGIT+ [',' DIGIT+]

DIGIT
   : [0-9]