
asm_lines = []
with open('FindMatrixDeterminant.asm', 'r') as f:
    for line in f:
        asm_lines.append(line)

#  Удаление комментарий
new_asm_lines = []
for i in range(len(asm_lines)):
    asm_lines[i] = asm_lines[i][:asm_lines[i].find(';')]
    if asm_lines[i] != "":
        new_asm_lines.append(asm_lines[i].replace('\t', ' ').strip())

asm_lines = new_asm_lines
memory_variables = {}
for i in range(len(asm_lines)):
    literals = asm_lines[i].split(' ')
    if len(literals) > 0 and literals[0] == "PUBLIC":
        memory_variables[literals[1]] = 0
    elif len(literals) > 1 and literals[1] == "SEGMENT":
        memory_variables[literals[0]] = 0
    else:
        for literal in literals:
            if literal in memory_variables:
                memory_variables[literal] += 1
print(asm_lines)