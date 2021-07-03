# Programming Language and Compiler

This course provides an introductory insight into how programming languages and compilers work. Throughout the homework in this course, you will create a simple, dynamic language with a virtual runtime.

## Virtual Machine

The runtime of our language consists of a simple stack-based virtual machine with a custom instruction set.

The virtual machine keeps track of the following structures:
- [Global Variable Table](#GlobalVariableTable)
- [Local Frame](#LocalFrame)
- [Bytecode Structure](#BytecodeFileFormat)
- [Execution Stack](#ExecutionStack)

### Bytecode Instruction Set

This virtual machine uses a simple custom instruction set:

```
gload <glob_var_index>: pushes the value of the global variable at index <glob_var_index> onto the stack
gstore <glob_var_index>: pops the value at the top of the stack to the global variable at index <glob_var_index>

lload <local_var_index>: pushes the value of the local variable at index <local_var_index> onto the stack
lstore <local_var_index>: pops the value at the top of the stack to the local variable at index <local_var_index>

add: pops two values off the stack, and pushes their sum back onto the stack
subtract: pops <a> and <b> (in that order) off the stack, and pushes <b> - <a> back onto the stack
mul: pops two values off the stack, and pushes their product back onto the stack
div: pops <a> and <b> (in that order) off the stack, and pushes floor(<b> / <a>) back onto the stack
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

my_function_a
    code
    code
    code
:my_function_a

my_function_b
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