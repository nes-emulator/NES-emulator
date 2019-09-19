from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class CompareBaseInstruction(CalculateAddress):
    def compare(self, memory, cpu, params, base_reg_value):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated = base_reg_value - value
        new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.carry = (new_calculated >= 0)
        cpu.state.status.negative = (new_reg_value > 127)

class CPXBaseInstruction(CompareBaseInstruction, Executable):
    def execute(self, memory, cpu, params):
        self.compare(memory, cpu, params, cpu.state.x.get_value())

class CPXImmediateAddr(Instruction, ImmediateAddr, CPXBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xE0, cycles=2)

class CPXZeroPageAddr(Instruction, ZeroPageAddr, CPXBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xE4, cycles=3)

class CPXAbsoluteAddr(Instruction, AbsoluteAddr, CPXBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xEC, cycles=4)



class CPYBaseInstruction(CompareBaseInstruction, Executable):
    def execute(self, memory, cpu, params):
        self.compare(memory, cpu, params, cpu.state.y.get_value())

class CPYImmediateAddr(Instruction, ImmediateAddr, CPYBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xC0, cycles=2)

class CPYZeroPageAddr(Instruction, ZeroPageAddr, CPYBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xC4, cycles=3)

class CPYAbsoluteAddr(Instruction, AbsoluteAddr, CPYBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xCC, cycles=4)

