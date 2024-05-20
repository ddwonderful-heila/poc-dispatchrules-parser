import argparse
import sys
import json
import yaml
import os
from parser import parse_rules


def main():
    parser = argparse.ArgumentParser(description='Parse rules from a file')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the file containing the rules')
    parser.add_argument('-o', '--output', type=str, choices=['json', 'yaml'], default='json',
                        help='Output format (json or yaml, default: json)')

    args = parser.parse_args()

    file_path = os.path.abspath(args.file)

    # General error handling for file reading and parsing
    try:
        with open(file_path, 'r') as file:
            rules = file.readlines()

        parsed_rules = parse_rules(rules)

        if args.output == 'json':
            print(json.dumps(parsed_rules, indent=4))
        elif args.output == 'yaml':
            print(yaml.dump(parsed_rules, default_flow_style=False))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
