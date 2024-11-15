import csv
import sys
import os

global REGISTER_AC
global MEMORY

def readBin(bin_path):
    result = []
    with open(bin_path, 'rb') as file:
        byte = file.read(1)
        while byte:
            command = bin(int(byte.hex(), 16))[2:].zfill(8)[2:]
            last_data = bin(int(byte.hex(), 16))[2:].zfill(8)[:2]
            if int(command, 2) == 49:
                data = [file.read(1), file.read(1)]
                data = (bin(int(data[1].hex(), 16))[2:].zfill(8)[2:] + bin(int(data[0].hex(), 16))[2:].zfill(8) + last_data)
                if data[0] == '1': data = int(data[1:], 2) - 2**15
                else: data = int(data, 2)
                result += [[int(command, 2), data]]
            elif int(command, 2) == 41 or int(command, 2) == 23:
                data = [file.read(1), file.read(1), file.read(1), file.read(1)]
                data = (bin(int(data[3].hex(), 16))[2:].zfill(8)[6:] + bin(int(data[2].hex(), 16))[2:].zfill(8) + bin(int(data[1].hex(), 16))[2:].zfill(8) + bin(int(data[0].hex(), 16))[2:].zfill(8) + last_data)
                data = int(data, 2)
                result += [[int(command, 2), data]]
            elif int(command, 2) == 42:
                result += [[int(command, 2), None]]
            byte=file.read(1)
        return result


def execute(commands):
    global MEMORY, REGISTER_AC
    for i in range(len(commands)):
        command = commands[i]
        code = command[0]
        data = command[1]
        if code == 49:
            REGISTER_AC = data
        elif code == 41:
            if data >= len(MEMORY):
                print(f'обращение к несуществующей ячейке - {data}, размер памяти - {len(MEMORY)}, команда {i+1} пропущена')
                continue
            elif MEMORY[data] is None:
                print(f'в ячейке {data} не инициализировано значение, команда {i+1} пропущена')
                continue
            else:
                REGISTER_AC = MEMORY[data]
        elif code == 23:
            if data >= len(MEMORY):
                print(f'обращение к несуществующей ячейке - {data}, размер памяти - {len(MEMORY)}, команда {i+1} пропущена')
                continue
            else:
                MEMORY[data] = REGISTER_AC
        elif code == 42:
            REGISTER_AC *= -1

def showResults(result_log, start, end):
    with open(result_log, "w", newline='') as log_file:
        for i in range(start, end):
            log = csv.writer(log_file, delimiter='\t')
            log.writerow([f"MEMORY[{i}]", MEMORY[i] if MEMORY[i] else "EMPTY"])

def interpret(bin_path, result_log, start, end, size=1024):
    global MEMORY, REGISTER_AC
    MEMORY = [None] * size
    REGISTER_AC = None
    commands = readBin(bin_path)
    execute(commands)
    showResults(result_log, start, end)

def main():
    bin_path = sys.argv[1]
    result_log = sys.argv[2]
    result_start = int(sys.argv[3])
    result_end = int(sys.argv[4])
    if not bin_path.endswith('.bin') or not os.path.exists(bin_path):
        print(f'ошибка при чтении {bin_path}')
        exit(1)
    interpret(bin_path, result_log, result_start, result_end)
    print(f"результаты выполнения программы записаны в файл {result_log}")

if __name__ == '__main__':
    main()
