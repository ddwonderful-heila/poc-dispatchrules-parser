# PoC Dispatch Rules Parser

The goal is a Heila-specific DSL for microgrid controls. The first iteration supports customizable rules for operating mode dispatch functions.

## Examples

### Single Condition
Check if some attribute at a single inverter is above some value. If so, run some command targeting that inverter.

```text
real_power@heila-001/inverter-001 > 500 -> set_real_power@heila-001/inverter-001:500
```
### Multiple Conditions
Check if multiple conditions are met using `and` and `or` logical operators.

```text
real_power@heila-001/inverter-001 > 500 and voltage@heila-001/something_else/inverter-001 < 300 or current@heila-001/something_else/inverter-001 == 50 -> send_some_command@heila-001/something_else/inverter-001:100,200
```

## Rule Format
### Condition
This part of the dispatch rule checks specific attributes:
```text
real_power@heila-001/inverter-001 > 500
```

### Command
This part of the dispatch order specifies the command to run and its inputs:
```text
set_real_power@heila-001/inverter-001:500
```

### Full Rule
Combines condition and command:
```text
real_power@heila-001/inverter-001 > 500 -> set_real_power@heila-001/inverter-001:500
```
## Usage
To use the parser, run the CLI tool with a file containing rules:

```sh
python dispatch_rules.py -f path/to/rule_file.txt -o json
```
The output format can be `json` (default) or `yaml`:

```sh
python dispatch_rules.py -f path/to/rule_file.txt -o yaml
```
