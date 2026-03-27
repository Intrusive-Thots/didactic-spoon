import os
import re

count = 0
for root, _, files in os.walk('src'):
    for f in files:
        if not f.endswith('.py'): continue
        path = os.path.join(root, f)
        
        with open(path, 'r', encoding='utf-8') as fobj:
            content = fobj.read()
            
        # Regex to strip `cursor="hand2"` or `cursor="xterm"` with or without commas and spaces
        new_content = re.sub(r',\s*cursor\s*=\s*[\"\'\\]+(hand2|xterm)[\"\'\\]+', '', content)
        new_content = re.sub(r'cursor\s*=\s*[\"\'\\]+(hand2|xterm)[\"\'\\]+\s*,', '', new_content)
        new_content = re.sub(r'cursor\s*=\s*[\"\'\\]+(hand2|xterm)[\"\'\\]+', '', new_content)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as fobj:
                fobj.write(new_content)
            count += 1
            print('Fixed:', path)

print(f'Done. Fixed {count} files.')
