import pytest
from parser import parse_rules

def test_single_rule():
    rules = ["real_power@heila-001/inverter-001 > 500 -> set_real_power@heila-001/inverter-001:500"]
    expected_output = [
        {
            'conditions': {
                'parameter': 'real_power',
                'microgrid_state_id': 'heila-001/inverter-001',
                'comparator': '>',
                'value': 500
            },
            'command': {
                'command': 'set_real_power',
                'microgrid_state_id': 'heila-001/inverter-001',
                'values': [500.0]
            }
        }
    ]
    assert parse_rules(rules) == expected_output

def test_multiple_rules():
    rules = [
        "real_power@heila-001/inverter-001 > 500 -> set_real_power@heila-001/inverter-001:500",
        "voltage@heila-001/something_else/inverter-001 < 300 -> send_some_command@heila-001/something_else/inverter-001:100,200"
    ]
    expected_output = [
        {
            'conditions': {
                'parameter': 'real_power',
                'microgrid_state_id': 'heila-001/inverter-001',
                'comparator': '>',
                'value': 500
            },
            'command': {
                'command': 'set_real_power',
                'microgrid_state_id': 'heila-001/inverter-001',
                'values': [500.0]
            }
        },
        {
            'conditions': {
                'parameter': 'voltage',
                'microgrid_state_id': 'heila-001/something_else/inverter-001',
                'comparator': '<',
                'value': 300
            },
            'command': {
                'command': 'send_some_command',
                'microgrid_state_id': 'heila-001/something_else/inverter-001',
                'values': [100.0, 200.0]
            }
        }
    ]
    assert parse_rules(rules) == expected_output

def test_complex_rule():
    rules = [
        "real_power@heila-001/inverter-001 > 500 and voltage@heila-001/something_else/inverter-001 < 300 or current@heila-001/something_else/inverter-001 == 50 and param_xyz@heila-001/something_else/inverter-001 >= 69 -> send_some_command@heila-001/something_else/inverter-001:100,200"
    ]
    expected_output = [
        {
            'conditions': {
                'or': [
                    {
                        'and': [
                            {
                                'parameter': 'real_power',
                                'microgrid_state_id': 'heila-001/inverter-001',
                                'comparator': '>',
                                'value': 500
                            },
                            {
                                'parameter': 'voltage',
                                'microgrid_state_id': 'heila-001/something_else/inverter-001',
                                'comparator': '<',
                                'value': 300
                            }
                        ]
                    },
                    {
                        'and': [
                            {
                                'parameter': 'current',
                                'microgrid_state_id': 'heila-001/something_else/inverter-001',
                                'comparator': '==',
                                'value': 50
                            },
                            {
                                'parameter': 'param_xyz',
                                'microgrid_state_id': 'heila-001/something_else/inverter-001',
                                'comparator': '>=',
                                'value': 69
                            }
                        ]
                    }
                ]
            },
            'command': {
                'command': 'send_some_command',
                'microgrid_state_id': 'heila-001/something_else/inverter-001',
                'values': [100.0, 200.0]
            }
        }
    ]
    assert parse_rules(rules) == expected_output

if __name__ == '__main__':
    pytest.main()
