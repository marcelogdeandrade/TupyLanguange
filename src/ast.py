from llvmlite import ir


class Number():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i


class Text():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        b = bytearray(self.value)
        n = len(b)
        return ir.Constant(ir.ArrayType(ir.IntType(8), n), b)


class Identifier():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        var = self.module.get_global(self.value.value)
        return self.builder.load(var)


class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.left = left
        self.right = right
        self.builder = builder
        self.module = module


class Add(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i


class Mul(BinaryOp):
    def eval(self):
        i = self.builder.mul(self.left.eval(), self.right.eval())
        return i


class Div(BinaryOp):
    def eval(self):
        i = self.builder.sdiv(self.left.eval(), self.right.eval())
        return i


class Bigger(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed(">", self.left.eval(), self.right.eval())
        return i


class Smaller(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed("<", self.left.eval(), self.right.eval())
        return i


class Equal(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed("==", self.left.eval(), self.right.eval())
        return i


class Different(BinaryOp):
    def eval(self):
        i = self.builder.icmp_signed("!=", self.left.eval(), self.right.eval())
        return i


class Attribution(BinaryOp):
    def eval(self):
        identifier = self.module.get_global(self.left.value)
        value = self.right.eval()
        self.builder.store(value, identifier)


class VarDec():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        initializer = ir.Constant(ir.IntType(8), int(0))
        var = ir.GlobalVariable(self.module,
                                ir.IntType(8), self.value.value)
        var.initializer = initializer


class Statements():
    def __init__(self, builder, module, first_child):
        self.builder = builder
        self.children = [first_child]
        self.module = module

    def add_child(self, child):
        self.children.append(child)

    def eval(self):
        for i in self.children:
            i.eval()


class If():
    def __init__(self, builder, module, pred, block):
        self.builder = builder
        self.module = module
        self.pred = pred
        self.block = block

    def eval(self):
        with self.builder.if_then(self.pred.eval()):
            self.block.eval()


class IfElse():
    def __init__(self, builder, module, pred, block1, block2):
        self.builder = builder
        self.module = module
        self.pred = pred
        self.block1 = block1
        self.block2 = block2

    def eval(self):
        cond = self.pred.eval()
        print(cond)
        with self.builder.if_else(cond) as (then, otherwise):
            with then:
                self.block1.eval()
            with otherwise:
                self.block2.eval()


class Print():
    def __init__(self, builder, module, print_func, value):
        self.builder = builder
        self.module = module
        self.value = value
        self.print_func = print_func

    def eval(self):
        value = self.value.eval()

        # Declare argument list
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        # Call Print Function
        self.builder.call(self.print_func, [fmt_arg, value])
        pass
