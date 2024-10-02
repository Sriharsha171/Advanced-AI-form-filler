# knowledge_base_parser.py

import re

def parse_knowledge_base(file_path):
    knowledge_base = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.match(r'(.+?):\s*(.+)', line)
            if match:
                key, value = match.groups()
                knowledge_base[key.strip()] = value.strip()
    return knowledge_base
