import os

target = r'c:\Users\josel\Downloads\Antigravity\INDICE Switch ES - The Goonies OS\src\ui.py'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# I will just write a very simple pass replacing all '{' with '{{'
# EXCEPT the ones that are Python format arguments
lines = content.split('\n')
in_f_string = False

for i, line in enumerate(lines):
    if 'html_template = f"""' in line:
        in_f_string = True
        continue
    if in_f_string and '"""' in line:
        in_f_string = False
        continue
        
    if in_f_string:
        # We need to escape single { and } to {{ and }}
        # But we MUST NOT touch python expressions. Let's find them first.
        expressions = ['{title_main}', '{title_sub}', '{json_data}', "{f'<img src=\"{avatar_b64}\" class=\"avatar\">' if avatar_b64 else ''}"]
        
        # Temp hide expressions
        for i_exp, exp in enumerate(expressions):
            if exp in line:
                line = line.replace(exp, f"__EXP_{i_exp}__")
                
        # Now we replace single { and } that are not already {{ or }}
        # Wait, the easiest way is to convert ALL to single, then ALL to double.
        line = line.replace('{{', '{').replace('}}', '}')
        line = line.replace('{', '{{').replace('}', '}}')
        
        # Restore expressions
        for i_exp, exp in enumerate(expressions):
            if f"__EXP_{i_exp}__" in line:
                line = line.replace(f"__EXP_{i_exp}__", exp)
                
        lines[i] = line

with open(target, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Fixed ui.py automatically!')
