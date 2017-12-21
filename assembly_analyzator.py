import re

ASM_COMMANDS = ["ADC", "ADD", "AND",
                "BSF", "BSR", "BT", "BTC", "BTR", 'BTS',
                'CALL', 'CBW', 'CLC', 'CLD', 'CLI', 'CMC', 'CDQ', 'CMP', 'CWD', 'CWDE',
                'DEC', 'DIV', 'IDIV','ENTER', 'IMUL', 'INC', 'J', 'JMP', 'LAHF', 'LEAVE',
                'LOOP', 'LOOPNZ', 'LOOPNE', 'LOOPZ', 'LOOPE', 'MOV', 'MOVSX', 'MOVZX', 'MUL',
                'NEG', 'NOP', 'NOT', 'OR', 'POP', 'POPA', 'POPAD', 'POPF', 'POPFD', 'PUSH',
                'PUSHA', 'PUSHAD', 'PUSHF', 'PUSHFD', 'RCL', 'RCR', 'RET', 'RETN', 'RETF',
                'ROL', 'ROR', 'SAHF', 'SAL', 'SAR', 'SBB', 'SHL', 'SHLD', 'STC', 'STD', 'STI',
                'SUB', 'TEST', 'XCHG', 'XOR']

ASM_TYPES = ['DB', 'DW', 'DQ', 'DD', 'DT']

asm_lines = []
with open('FindMatrixDeterminant.asm', 'r') as f:
    for line in f:
        asm_line = line
        asm_line = asm_line[:asm_line.find(';')].replace('\t', ' ').strip().split(' ')
        if asm_line != "":
            asm_lines.append(asm_line)

asm_command_counter = 0
variables = {}
procedures = {}
memory_request = 0
memory_request_line = []

command_blocks = {}
command_block = []

for asm_line in asm_lines:
    if len(asm_line) > 1 and asm_line[1] in ASM_TYPES:
        variables[asm_line[0]] = 0
        command_block = []
    elif len(asm_line) > 1 and asm_line[1] in ('PROC', 'ENDP'):
        procedures[asm_line[0]] = 0
        command_block = []
    elif len(asm_line) > 1 and asm_line[0] == 'EXTRN':
        extern_data = asm_line[1].split(':')
        if extern_data[1] == 'PROC':
            procedures[extern_data[0]] = 0
        else:
            variables[extern_data[0]] = 0
        command_block = []
    elif asm_line[0].upper() in ASM_COMMANDS:
            command_block.append(asm_line[0])
            if len(command_block) > 1:
                if tuple(command_block) not in command_blocks:
                    command_blocks[tuple(command_block)] = 1
                else:
                    command_blocks[tuple(command_block)] += 1
            asm_command_counter += 1
            counter = 0
            for literal in asm_line:
                if re.match(r'.*[[].+[]]', literal) or (literal in variables) or (literal in procedures):
                    counter += 1
                    memory_request += 1
                    memory_request_line.append(asm_line)
    else:
        command_block = []

print('Количество обращений к памяти в командах:', memory_request)
print('Количество команд:', asm_command_counter)
print('Отношение количества обращения к памяти в командах к общему количеству команд:',
      memory_request / asm_command_counter)
print()

max_block_count = max(command_blocks.values())
for command_block, count in command_blocks.items():
    if count > max_block_count / 5:
        print('Блок:', "".join([command+" " for command in command_block]))
        print('Количество повторений:', count)
        print('Устойчивость:', count / max_block_count)
        print()