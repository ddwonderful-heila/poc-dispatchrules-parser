from pyparsing import *

# Basic elements
integer = Word(nums).setParseAction(lambda t: int(t[0]))
floating = Combine(Optional('-') + Word(nums) + '.' + Word(nums)).setParseAction(lambda t: float(t[0]))
number = floating | integer

# Energy node identifiers with wildcard support
identifier = Word(alphas + '*', alphanums + '_-*')
node_identifier = Combine(identifier + '/' + identifier)

# Variables can have attributes using @
variable = Combine(node_identifier + '@' + Word(alphas, alphanums + '_'))
attribute = variable | number

# Define operators
comparison_op = oneOf("> < >= <= == !=")
boolean_op = oneOf("and or")
not_op = Literal("not")

# Forward declaration for recursive grammars
expr = Forward()

# An atom could be a number, a variable with an attribute, or a parenthesized expression
atom = attribute | Group('(' + expr + ')')

# Handle the 'not' unary operator
def parse_not(t):
    if len(t) == 2:
        return ['not', t[1]]
    return t[0]

# Create binary operator parse actions
def binary_op_action(op_str):
    return lambda s, l, t: [op_str] + t[0][0::2]

# Handle dispatch orders in action part
def parse_dispatch_order(t):
    parts = t[0].split('=')
    return ['set', parts[0].strip(), float(parts[1].strip())]

dispatch_order = (node_identifier + Suppress("-->") + node_identifier + '=' + number)
dispatch_order.setParseAction(parse_dispatch_order)

# Operations in precedence order
expr <<= infixNotation(atom,
    [
        (not_op, 1, opAssoc.RIGHT, parse_not),
        (comparison_op, 2, opAssoc.LEFT, binary_op_action),
        (boolean_op, 2, opAssoc.LEFT, binary_op_action),
    ])

# Complete condition and action parsing
condition = expr
action = OneOrMore(dispatch_order)

# Full rule parsing
rule = "if" + Group(condition)("condition") + "then" + Group(action)("action")

# Example parsing
rule_string = "if (real_power@heila-001/inverter* > 500) then set_real_power-->heila-001/inverter-001 = 500"

parsed_rule = rule.parseString(rule_string)

print("Parsed Rule:")
print(parsed_rule)
