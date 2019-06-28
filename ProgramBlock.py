# Rez
class ProgramBlock:

    def __init__(self):
        self.line = 0
        self.array = []

    def addInstruction(self, inst):
        self.array.append(inst)
        self.line += 1

    def addInstruction(self, op, opr1, opr2, dest):
        inst = Instruction(op, opr1, opr2, dest)
        print(str(self.line) + ":\t" + str(inst))
        self.array.append(inst)
        self.line += 1

    def setInstruction(self, inst, i):
        self.array[i] = inst

    def setInstruction(self, op, opr1, opr2, dest, i):
        inst = Instruction(op, opr1, opr2, dest)
        print(str(i) + ":\t" + str(inst))
        self.array[i] = inst

    def insertDummy(self, num):
        for _ in range(num):
            self.addInstruction(None, None, None, None)


class Instruction:
    def __init__(self, op, opr1, opr2, dest):
        self.op = op
        self.operand1 = opr1
        self.operand2 = opr2
        self.dest = dest

    def __str__(self):
        return "(" + str(self.op) + ", " + str(self.operand1) + ", " + str(self.operand2) + ", " + str(self.dest) + ")"



