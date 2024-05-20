from pyparsing import *
ppc = pyparsing_common


# Basic elements
parameter = Word(alphanums + '_-')

# microgrid state key
segment = Word(alphanums + '-_/')
microgrid_state_id = Combine(segment + ZeroOrMore('/' + segment))
value = ppc.number

# Comparison operators
comparator = oneOf("> < >= <= == !=")

# Logical operators
and_op = Keyword("and")
or_op = Keyword("or")

# Command portion elements
command = Word(alphas, alphanums + '_')
values = Group(delimitedList(value))

# Define single condition
single_condition = parameter + Suppress('@') + microgrid_state_id + comparator + value

def _single_condition_parse_action(t):
    return {
        "parameter": t[0],
        "microgrid_state_id": t[1],
        "comparator": t[2],
        "value": t[3]
    }

single_condition.setParseAction(_single_condition_parse_action)

# Define combined conditions with logical operators
condition = infixNotation(single_condition, [
    (and_op, 2, opAssoc.LEFT, lambda t: {"and": t[0][0::2]}),
    (or_op, 2, opAssoc.LEFT, lambda t: {"or": t[0][0::2]})
])

# Define command expression
command_expr = Suppress('->') + command + Suppress('@') + microgrid_state_id + Suppress(':') + values

# Define parse action to structure the parsed tokens for command
def _command_parse_action(t):
    return {
        "command": t[0],
        "microgrid_state_id": t[1],
        "values": t[2].asList()
    }

command_expr.setParseAction(_command_parse_action)

# Full rule parsing
expression = condition + command_expr

# Function to parse a single rule string
def _parse_rule(rule_string):
    parsed_expression = expression.parseString(rule_string, parseAll=True)
    return {'conditions': parsed_expression[0], 'command': parsed_expression[1]}

def parse_rules(rules):
    """
    Parse a list of rules, each represented as a string.

    Args:
        rules (list of str): A list of strings, each containing a rule.

    Returns:
        list[dict]: A list of parsed rules, where each rule is represented as a dictionary.
    """
    parsed_rules = []
    for rule in rules:
        rule = rule.strip()
        if rule:
            parsed_rules.append(_parse_rule(rule))
    return parsed_rules


if __name__ == '__main__':
    test_expressions = [

    ]

    for test_expression in test_expressions:
        print(f"Expression: {test_expression}")
        print("\nParsed Expression")
        print(_parse_rule(test_expression))
        print("\n---\n")
