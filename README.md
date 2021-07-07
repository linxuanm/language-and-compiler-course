# Programming Language and Compiler

This course provides an introductory insight into how programming languages and compilers work. Throughout the homework in this course, you will create a simple, dynamic language with a virtual runtime.

Due to the short length of this course, the main focus will be on understanding basic concepts such as compilation and runtime, creating a runtime VM, and implementing simple parsing algorithms. Type handling and inferences, as well as optimizations, will not be covered, but are encouraged if you have spare time.

## Source Language

The source language is a type-free language with C-like syntax:

```
(* Tokens *)
non_zero = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
digit = "0" | non_zero;
alpha = "A" | ... | "Z" | "a" | ... | "z";
operator = "=" | "<" | ">" | "==" | "<=" | ">=" | "+" | "-" | "*" | "/" | "&&" | "||";
symbol = "," | ";" | "(" | ")" | "{" | "}";

keyword = "if" | "else" | "while" | "return" | "break" | "continue" | "decl";
identifier = ((alpha | "_"), {alpha | digit | "_"}) - keyword;
int = digit {digit};
bool = "TRUE" | "FALSE";
none = "NONE";
string = '"', {any_char - '"'}, '"';
literal = string | none | int | bool;

(* Syntax *)
iden_list = [identifier, {",", identifier}];
stmt_list = {stmt};

declare = "decl", iden_list, ";";
assign = identifier, "=", exp, ";";
return = "return", exp, ";";
break = "break", ";";
continue = "continue", ";";

if = "if", "(", exp, ")", "{", stmt_list, "}", {"else", "{", stmt_list, "}"};
while = "while", "(", exp, ")", "{", stmt_list, "}";

stmt = if | while | declare | assign | return | break | continue;

decl_func = identifier, "(", iden_list, ")", "{", stmt_list, "}";

program = {decl_func | declare};
```

Here is some sample code:

```
decl my_global_var, other_var

add_func(a, b) {
    return a + b;
}

main() {
    my_global_var = 10;
    return NONE;
}
```

### Types

Our source language has 4 value types:
- `int`: an integer (the only numeric type in our language)
- `string`: a sequence of characters
- `bool`: a value of either `TRUE` or `FALSE`
- `NONE`: a placeholder value denoting the absence of a value

## Lexer

The lexer is responsible for tokenizing a piece of source language into a list of tokens to make parsing easier.

Our language has 6 token types:
- `KEYWORD`: reserved words used in the syntax' construct (`if`, `while`, `return`, etc)
- `IDENTIFIER`: names of values/functions defined by the programmer (`my_var`, `foo`, etc)
- `LITERAL`: literal representation of values (`76`, `NONE`, `"hello world"`, `FALSE`, etc)
- `SYMBOL`: special symbols used in the syntax' construct (`,`, `(`, `;`, `{`, etc)
- `OPERATOR`: symbols used for processing purposes (`=`, `+`, `<`, etc)
- `WHITESPACE`: a sequence of whitespace characters (` `, `\n`, `\t`)

Some notes:
- An `IDENTIFIER` cannot take the name of an existing `KEYWORD` (raises a SyntaxError)
- `SYMBOL` is for syntax structure only, which is why `=` classifies as an `OPERATOR`

## Virtual Machine

The runtime of our language consists of a simple stack-based virtual machine with a custom instruction set.

The virtual machine keeps track of the following structures:
- [Global Variable Table](#global-variable-table)
- [Local Frame](#local-frame)
- [Bytecode Structure](#bytecode-file-format)
- [Execution Stack](#execution-stack)
- [Native Functions](#native-functions)

### Bytecode Instruction Set

This virtual machine uses a simple custom instruction set:

```
gload <glob_var_index>: pushes global variable <glob_var_index> onto the stack
gstore <glob_var_index>: pops the top of the stack into global variable <glob_var_index>

lload <local_var_index>: pushes local variable <local_var_index> onto the stack
lstore <local_var_index>: pops the top of the stack into local variable <local_var_index>

add: pops two values off the stack, and pushes their sum onto the stack
subtract: pops <a> and <b> (in that order) off the stack, and pushes <b> - <a> onto the stack
mul: pops two values off the stack, and pushes their product onto the stack
div: pops <a> and <b> (in that order) off the stack, and pushes floor(<b> / <a>) onto the stack
not: pops a boolean value off the stack, and pushes its opposite onto the stack
and: pops two boolean values off the stack, and pushes their AND result (&&) onto the stack
or: pops two boolean values off the stack, and pushes their OR result (||) onto the stack

equal: pops two values off the stack and push true if then are equal, else false
nequal: pops two values off the stack and push true if then are not equal, else false
less: pops <a> and <b> off the stack and push true if <a> is less than <b>, else false
great: pops <a> and <b> off the stack and push true if <a> is greater than <b>, else false

jmp <code_index>: jumps to code <code_index>
cjmp <code_index>: pops a boolean value off the stack; if `TRUE`, jumps to code <code_index>
call <func_name>: invokes the function <func_name>
ncall <native_func_index>: invokes the native function <native_func_index>
```

### Global Variable Table

The global variable table's length is defined at the initialization phrase of the virtual machine. Global variables lose their names during compilation, and instead are referenced by their index during runtime.

```
Global Variable Table:
             ____________________
            |                    |
    index 0 |     glob_var_1     |
            |____________________|
            |                    |
    index 1 |     glob_var_2     |
            |____________________|
            |                    |
            |        ....        |
            |____________________|
            |                    |
index n - 1 |     glob_var_n     |
            |____________________|
```

### Local Frame

Each function call pushes a frame onto the frame stack. Each frame represents the context of the current function scope, and stores the following information:

- Local variable value (in a variable table identical to the [Global Variable Table](#GlobalVariableTable))
- Current instruction index

### Bytecode File Format

Each bytecode file `.bytecode` contains all the necessary information to execute the contained code. This includes function information and global variable information.

Each bytecode file is structured as such (indentation insensitive):

```
<global_var_count>
<function_count>

my_function_a <local_var_count>
    code
    code
    code
:my_function_a

my_function_b <local_var_count>
    code
    code
    code
:my_function_b
```

The loading of bytecode files is already written for you.

### Execution Stack

The execution stack is a stack that contains parameters, results or partial results of a series of instructions.

Demonstration of calculating `(5 + 8) * (7 - 2)` with the stack (pseudo-code):

```
push 5        // [5]
push 8        // [5, 8]
add           // [13]
push 7        // [13, 7]
push 2        // [13, 7, 2]
subtract      // [13, 5]
mul           // [65]
```

### Native Functions

To allow interaction with the low level functionalities, the virtual machine exposes certain native functions, such as basic IO. The native function table is similar to the various variable tables. Each native function behaves similarily to a normal function; parameters are popped of the stack in reverse order, and the return value is pushed onto the stack when the function returns.