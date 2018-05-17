from llvmlite import ir


class Number():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        i = ir.Constant(ir.IntType(32), int(self.value))
        return i


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
        ir.GlobalVariable(self.module,
                          ir.IntType(32), self.value.value)


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
