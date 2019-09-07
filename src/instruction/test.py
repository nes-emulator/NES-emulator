import unittest
from .collection import InstructionCollection
from .instruction import Instruction

class RegisterTest(unittest.TestCase):

    def test_get_instruction_add(self):
        inst = InstructionCollection.get_instruction('add')
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual('add', inst.opcode)

    def test_get_instruction_none(self):
        inst = InstructionCollection.get_instruction('inst-non-existent-bla-bla')
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual('none', inst.opcode)