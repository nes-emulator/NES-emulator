from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


class AddInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        carry_add = 1 if cpu.state.status.carry else 0

        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        old_value = cpu.state.a.get_value()

        new_calculated_value = cpu.state.a.get_value() + value + carry_add

        new_reg_value = new_calculated_value % 256
        cpu.state.a.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.carry = (new_calculated_value > 255)
        cpu.state.status.negative = (new_reg_value > 127)
        cpu.state.status.overflow = (old_value < 128 and value + carry_add < 128 and new_calculated_value > 128) or \
                                    (old_value > 127 and value + carry_add > 127 and new_calculated_value > 255)

class AddInstructionImmediateAddr(Instruction, ImmediateAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x69, cycles=1)

class AddInstructionZeroPageAddr(Instruction, ZeroPageAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x65, cycles=1)

class AddInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x75, cycles=1)

class AddInstructionAbsoluteAddr(Instruction, AbsoluteAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x60, cycles=1)

class AddInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x7D, cycles=1)

class AddInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x79, cycles=1)

class AddInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x61, cycles=1)

class AddInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x71, cycles=1)
