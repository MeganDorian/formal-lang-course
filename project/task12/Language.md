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

lambda -> LP lambda RP
          | LAMBDA elems ARROW expr

elems -> var
         | LB elems (COMMA elems)* RB

expr -> var
        | val
        | SET_START list FOR expr
        | SET_FINAL list FOR expr
        | ADD_START expr FOR expr
        | ADD_FINAL expr FOR expr
        | GET_START expr
        | GET_FINAL expr
        | GET_REACHABLE expr
        | GET_VERTICES expr
        | GET_EDGES expr
        | GET_LABELS expr
        | MAP lambda FOR expr
        | FILTER lambda FOR expr
        | LOAD STR
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
        | LP V (COMMA V)* RP

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
LAMBDA -> '\_'
ARROW -> '=>'

INTER -> '&'
CONCAT -> '++'
UNION -> '|'
SKLEENE -> '*'
SWITCH -> '<<'
IN -> 'in'

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
LOAD -> 'load'
MAP -> 'map'
FILTER -> 'filter'
GET_START -> 'get_start'
GET_FINAL -> 'get_final'
GET_REACHABLE -> 'get_reachable'
GET_VERTICES -> 'get_verices'
GET_EDGES -> 'get_edges'
GET_LABELS -> 'get_labels'
```

## Примеры

В приведенном примере происходит загрузка графа в переменную ``graph``, далее задаются начальные и добавляется финальная
вершина загруженному графу:

```
let graph = load "path_to_graph/graph.dot"
let graphWithOtherStarts = set_start (2,4,6) FOR graph
let graphWithAddedFinal = add_final (1,3) FOR graph
```

Далее приведены примеры получения ребер графа, применения ``map`` (инвертирует ребра), ``filter`` (оставляет ребра, у
которых метки входят в список) и вывода результата:

```
let edges = get_edges graph
let mapped = map (\_ {a, label, b} -> {b, label, a}) edges

let labelsList = ("l", "a", "b")
let filtered = filter (\_ {a, label, b} -> {label in labelsList}) mapped

print filtered

```
