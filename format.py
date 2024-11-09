import re

contents = []
while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)
unformatted = '\n'.join(contents)

formatted = re.sub(r'(?<!\n)\n(?!\n)', '\\n\\n', unformatted)
formatted = formatted.replace('\n','\\n')
print(f'"{formatted}"')