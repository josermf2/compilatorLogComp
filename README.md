# Compilador - LogComp

Diagrama Atual:

<img src=Roteiro3.jpg>

EBNF Atual:

EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;

Desenvolvedor:
- José Rafael Martins Fernandes

![git status](http://3.129.230.99/svg/josermf2/compilatorLogComp/)
