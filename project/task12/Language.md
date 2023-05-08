# Задача 12. Язык запросов к графам

## Описание абстрактного синтаксиса языка запросов

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Label of label
  | Vertex of vertex
  | Edge of edge
  | Graph of graph

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = Lambda of List<var> * expr
```

## Описание конкретного синтаксиса языка запросов

```
program -> (stmt DELIM)* *EOF

stmt -> PRINT
        | bind

print -> print expr
bind -> LET var ASSIGN expr

expr -> var
        | val
        | SET_START list FOR expr
        | SET_FINAL list FOR expr
        | ADD_START expr FOR expr
        | ADD_FINAL expr FOR expr
        | GET_START
        | GET_FINAL
        | GET_REACHABLE
        | GET_VERTICES
        | GET_EDGES
        | GET_LABELS
        | MAP
        | FILTER
        | LOAD
        | expr INTER expr
        | expr CONCAT expr
        | expr UNION expr
        | SKLEENE espr
        | expr SWITCH expr
        | LP expr RP

var -> CHAR*
val -> STR
       | INT
       | BOOL
       | vertex
       | edge
       | graph
       | list

list -> LP RP
        | LP V (COMMA V)* RB

vertex -> INT

label -> STR

edge -> LB vertex COMMA label COMMA vertex RB

graph -> LB list COMMA list RB

DELIM -> ';'
FOR -> 'for'
LET -> 'let'
ASSIGN -> '='
LP -> '('
RP -> ')'
LB -> '{'
RB -> '}'
COMMA -> ','
INTER -> '&'
CONCAT -> '++'
UNION -> '|'
SKLEENE -> '*'
SWITCH -> '<<'

INT -> [0-9]+
CHAR -> [a-zA-Z]
STR -> '"' (CHAR | INT | ' ')* '"'
BOOL -> 'true'
        | 'false'
V -> BOOL
     | INT
     | STR
     | CHAR

PRINT -> 'print'
SET_START -> 'set_start'
SET_FINAL -> 'set_final'
ADD_START -> 'add_start'
ADD_FINAL -> 'add_final'
```

## Примеры

```

```
