#!/usr/bin/env python3
# Fix result.html template to use result.confidence instead of result.accuracy

content = open('templates/result.html', 'r', encoding='utf-8').read()

# Fix the broken line from the previous replacement
content = content.replace(
    "{% set acc_num = str(result.confidence)('%', '') | float %}", 
    "{% set acc_num = result.confidence | float %}"
)

open('templates/result.html', 'w', encoding='utf-8').write(content)
print('✓ Fixed result.html template')
