from src.instruction.instruction import *
from src.instruction.addressing import *

class DEX(Instruction):
    def __init__(self):
        super().__init__(opcode=202, cycles=1)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.x.get_value() - 1

        new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))
        cpu.state.x.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

class DEY(Instruction):
    def __init__(self):
        super().__init__(opcode=136, cycles=1)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.y.get_value() - 1

        new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))
        cpu.state.y.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

# TODO Review thsi 136
class DEC(Instruction):
    def __init__(self):
        super().__init__(opcode='dec', cycles=1)

    def execute(self, memory, cpu, params):

        pass