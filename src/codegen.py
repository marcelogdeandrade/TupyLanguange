from __future__ import print_function
from lexer import Lexer
from parser import Parser
from llvmlite import ir, binding
from ctypes import CFUNCTYPE


text_input = """
var x;
x := 4 * 4 + 2;
SE (x = 17){
    x := 3;
} SENAO {
    x := 1;
}
print(x);
"""

# Initialize binding
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()


def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = binding.parse_assembly("")
    engine = binding.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = binding.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    fptr = engine.get_function_address("main")
    py_func = CFUNCTYPE(None)(fptr)
    print('--------------')
    py_func()
    print('\n --------------')
    engine.run_static_constructors()
    return mod


# Config LLVM
module = ir.Module(name=__file__)
module.triple = binding.get_default_triple()
func_type = ir.FunctionType(ir.VoidType(), [], False)
base_func = ir.Function(module, func_type, name="main")
block = base_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

# Declare Printf function
voidptr_ty = ir.IntType(8).as_pointer()
printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
printf = ir.Function(module, printf_ty, name="printf")

# Create lexer
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)
# Create parser
pg = Parser(builder, module, printf)
pg.parse()
parser = pg.get_parser()

parser.parse(tokens).eval()

builder.ret_void()

llvm_ir = str(module)
engine = create_execution_engine()
mod = compile_ir(engine, llvm_ir)

print(llvm_ir)

with open("output.ll", 'w') as output_file:
    output_file.write(str(module))
