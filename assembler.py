import csv
import struct
import os
import sys

def parse_asm(input_text):
    input_text=input_text.splitlines()
    if len(input_text)==0:
        print('файл пустой')
        exit(1)
    commands = []
    for i in range(len(input_text)):
        line = input_text[i].strip()
        args = line.split()
        if len(line) == 0:
            continue
        if args[0] == 'LOAD':
            if len(args)==2:
                symbol = args[1][0]
                args[1] = args[1][1:]
                if not symbol == '#':
                    print(f'в строке {i + 1} нарушен синтаксис, вместо {symbol+args[1]} нужно #{symbol+args[1]}')
                    exit(1)
                elif not (args[1].isdigit() or (args[1][0] == '-' and args[1][1:].isdigit())):
                    print(f'в строке {i + 1} аргумент - не число')
                    exit(1)
                elif not (-32768 <= int(args[1]) <= 32767):
                    print(f'в строке {i + 1} ошибка из-за переполнения 16-битной разрядной сетки ({(-1) * 2**15} <= a <= {2 ** 15 - 1})')
                    exit(1)
                else:
                    commands += [f'49 {args[1]}']
            else:
                print(f'в строке {i+1} неверное число аргументов')
                exit(1)
        elif args[0] == 'READ':
            if len(args)==2:
                f = args[1][0]
                l = args[1][-1]
                param = args[1][1:-1]
                if not (f == '[' and l == ']'):
                    print(f'в строке {i + 1} нарушен синтаксис, вместо {args[1]} нужно [{args[1]}]')
                    exit(1)
                if not param.isdigit():
                    print(f'в строке {i + 1} аргумент - не число')
                    exit(1)
                elif not (0 <= int(param) < 2**28):
                    print(f'в строке {i + 1} ошибка из-за переполнения 28-битной разрядной сетки (0 <= a <= {2 ** 28 - 1})')
                    exit(1)
                else:
                    commands += [f'41 {param}']
            else:
                print(f'в строке {i+1} неверное число аргументов')
                exit(1)
        elif args[0] == 'WRITE':
            if len(args)==2:
                f = args[1][0]
                l = args[1][-1]
                param = args[1][1:-1]
                if not (f == '[' and l == ']'):
                    print(f'в строке {i + 1} нарушен синтаксис, вместо {args[1]} нужно [{args[1]}]')
                    exit(1)
                if not param.isdigit():
                    print(f'в строке {i + 1} аргумент - не число')
                    exit(1)
                elif not (0 <= int(param) < 2**28):
                    print(f'в строке {i + 1} ошибка из-за переполнения 28-битной разрядной сетки (0 <= a <= {2 ** 28 - 1})')
                    exit(1)
                else:
                    commands += [f'23 {param}']
            else:
                print(f'в строке {i+1} неверное число аргументов')
                exit(1)
        elif args[0] == 'MINUS':
            if len(args)==1:
                commands += ['42']
            else:
                print(f'в строке {i+1} неверное число аргументов')
                exit(1)
        else:
            print(f'в строке {i + 1} неизвестная команда')
            exit(1)
    return commands



def writeLog(commands, log_path):
    with open(log_path, "w", newline='') as log_file:
        log = csv.writer(log_file, delimiter='\t')
        for command in commands:
            if command.startswith('49'):
                log.writerow(["LOAD", "A=49", f"B={command.split()[1]}"])
            elif command.startswith('41'):
                log.writerow(["READ", "A=41", f"B={command.split()[1]}"])
            elif command.startswith('23'):
                log.writerow(["WRITE", "A=23", f"B={command.split()[1]}"])
            else:
                log.writerow(["MINUS", "A=42"])

def writeBin(commands, bin_path):
    with open(bin_path, 'wb') as bin_file:
        for command in commands:
            parts = command.split()
            a = int(parts[0])
            if a == 49:
                b = int(parts[1])
                if b < 0:
                    b = (2**16 + b)
                b = bin(b)[2:].zfill(16)
                first_part = int(b[-2:] + bin(a)[2:].zfill(6), 2)
                second_part = int(b[:-2], 2)
                byte = struct.pack('<BH', first_part, second_part)
            elif a == 42:
                first_part = a
                byte = struct.pack('<B', first_part)
            else:
                b = int(parts[1])
                b = bin(b)[2:].zfill(16)
                first_part = int(b[-2:] + bin(a)[2:].zfill(6), 2)
                second_part = int(b[:-2], 2)
                byte = struct.pack('<BI', first_part, second_part)
            bin_file.write(byte)


def assemble(source_path, bin_path, log_path):
        with open(source_path, 'r') as source:
            text = source.read()
            commands = parse_asm(text)
            writeLog(commands, log_path)
            writeBin(commands, bin_path)
            print('бинарный файл сформирован')

def main():
    source_path = sys.argv[1]
    bin_path = sys.argv[2]
    log_path = sys.argv[3] if len(sys.argv)==4 else "log.csv"
    if not os.path.exists(source_path):
        print(f'нет такого файла - {source_path}')
        exit(1)
    elif not bin_path.endswith('.bin'):
        print(f'файл {bin_path} - не бинарный')
        exit(1)
    else:
        assemble(source_path, bin_path, log_path)

if __name__ == '__main__':
    main()