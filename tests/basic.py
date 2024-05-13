import unittest
from pyparsing import ParseException

# Assuming the parser and other components are defined in a module named 'haruspecs_parser'
# from haruspecs_parser import rule  # Uncomment if your parser is in a separate module

# For now, we'll redefine the minimal needed part of the parser here for testing purposes.
from pyparsing import *

# Define basic elements
# u_integer = Word(nums).setParseAction(lambda t: int(t[0]))
s_integer = Combine(Optional('-') + Word(nums)).setParseAction((lambda t: int(t[0])))
s_float = Combine(Optional('-') + Optional(Word(nums)) + '.' + Word(nums)).setParseAction(lambda t: float(t[0]))
number = s_float | s_integer

energy_node = Word(alphas + '*', alphanums + '_-*')
node_identifier = Combine(energy_node + '/' + energy_node)

variable = Combine(node_identifier + '@' + Word(alphas, alphanums + '_'))
attribute = variable | number

comparison_op = oneOf("> < >= <= == !=")
boolean_op = oneOf("and or")

expr = Forward()
atom = attribute | Group('(' + expr + ')')

def binary_op_action(op_str):
    return lambda s, l, t: [op_str] + t[0][0::2]

def parse_dispatch_order(t):
    parts = t[0].split('=')
    return ['set', parts[0].strip(), float(parts[1].strip())]

dispatch_order = (node_identifier + Suppress("-->") + node_identifier + '=' + number)
dispatch_order.setParseAction(parse_dispatch_order)

expr <<= infixNotation(atom,
    [
        (not_op, 1, opAssoc.RIGHT, parse_not),
        (comparison_op, 2, opAssoc.LEFT, binary_op_action),
        (boolean_op, 2, opAssoc.LEFT, binary_op_action),
    ])

condition = expr
action = OneOrMore(dispatch_order)
rule = "if" + Group(condition)("condition") + "then" + Group(action)("action")


class TestHaruspecsParser(unittest.TestCase):
    def test_basic_rule(self):
        rule_text = "if (real_power@heila-001/inverter-001 > 500) then set_real_power-->heila-001/inverter-001 = 500"
        parsed = rule.parseString(rule_text)
        self.assertEqual(parsed.condition[0], ['>', 'real_power@heila-001/inverter-001', 500])
        self.assertEqual(parsed.action[0], ['set', 'set_real_power-->heila-001/inverter-001', 500])

    def test_wildcard_rule(self):
        rule_text = "if (voltage@heila-*/battery* < 240) then set_voltage-->heila-002/battery-001 = 250"
        parsed = rule.parseString(rule_text)
        self.assertEqual(parsed.condition[0], ['<', 'voltage@heila-*/battery*', 240])
        self.assertEqual(parsed.action[0], ['set', 'set_voltage-->heila-002/battery-001', 250])

    def test_logical_and_rule(self):
        rule_text = "if (temp@heila-001/inverter-001 >= 100 and temp@heila-001/inverter-002 <= 150) then set_cooling-->heila-001/inverter-001 = 1"
        parsed = rule.parseString(rule_text)
        self.assertEqual(parsed.condition[0], ['and', ['>=', 'temp@heila-001/inverter-001', 100], ['<=', 'temp@heila-001/inverter-002', 150]])
        self.assertEqual(parsed.action[0], ['set', 'set_cooling-->heila-001/inverter-001', 1])

    def test_logical_or_rule(self):
        rule_text = "if (status@heila-001/inverter-001 == 0 or status@heila-001/inverter-002 == 0) then set_restart-->heila-001/inverter-001 = 1"
        parsed = rule.parseString(rule_text)
        self.assertEqual(parsed.condition[0], ['or', ['==', 'status@heila-001/inverter-001', 0], ['==', 'status@heila-001/inverter-002', 0]])
        self.assertEqual(parsed.action[0], ['set', 'set_restart-->heila-001/inverter-001', 1])

    def test_complex_rule(self):
        rule_text = "if ((power@heila-001/inverter-001 > 300) and not (status@heila-001/inverter-001 == 0)) then set_power-->heila-001/inverter-001 = 300"
        parsed = rule.parseString(rule_text)
        self.assertEqual(parsed.condition[0], ['and', ['>', 'power@heila-001/inverter-001', 300], ['not', ['==', 'status@heila-001/inverter-001', 0]]])
        self.assertEqual(parsed.action[0], ['set', 'set_power-->heila-001/inverter-001', 300])

    def test_negative_numbers(self):
        rule_text = "if (efficiency@heila-001/inverter-003 < -0.85) then set_efficiency-->heila-001/inverter-003 = -0.80"
        parsed = rule.parseString(rule_text)
        self.assertEqual(parsed.condition[0], ['<', 'efficiency@heila-001/inverter-003', -0.85])
        self.assertEqual(parsed.action[0], ['set', 'set_efficiency-->heila-001/inverter-003', -0.80])

    def test_invalid_syntax(self):
        rule_text = "if power@heila-001/inverter-001 > 500 then set_power-->heila-001/inverter-001 = 500"
        with self.assertRaises(ParseException):
            rule.parseString(rule_text)

if __name__ == '__main__':
    unittest.main()
