# Rez
class ProgramBlock:

    def __init__(self):
        self.line = 0
        self.array = []
        self.insertDummy(1)

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

    def get_generated_code(self):
        mystr = ''
        for i in range(self.line):
            mystr += str(i) + ' ' + self.array[i].__str__() + '\n'
        return mystr

    def export_generated_code(self):
        text = self.get_generated_code()
        file = open('output.txt', 'w')
        file.write(text)
        file.close()


class Instruction:
    def __init__(self, op, opr1, opr2, dest):
        self.op = op
        self.operand1 = opr1
        self.operand2 = opr2
        self.dest = dest

    def __str__(self):
        s = [str(self.op), str(self.operand1), str(self.operand2), str(self.dest)]
        for a, i in enumerate([self.op, self.operand1, self.operand2, self.dest]):
            if i is None:
                s[a] = ''
        return "(" + s[0] + ", " + s[1] + ", " + s[2] + ", " + s[3] + ")"



