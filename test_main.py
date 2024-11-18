import assembler
import interpreter
import pytest


@pytest.fixture
def setup(tmp_path):
    source_path = tmp_path / "source.asm"
    bin_path = tmp_path / "main.bin"
    log_path = tmp_path / "log.csv"
    result_log = tmp_path / "result.csv"
    return source_path, bin_path, log_path, result_log

def test_load(setup):
    source_path, bin_path, log_path, result_log = setup
    asm_code = "LOAD #100"
    with open(source_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(source_path, bin_path, log_path)
    interpreter.interpret(bin_path, result_log, 0, 4)
    assert interpreter.REGISTER_AC == 100

def test_write(setup):
    source_path, bin_path, log_path, result_log = setup
    asm_code = '''
        LOAD #100
        WRITE [100]
    '''
    with open(source_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(source_path, bin_path, log_path)
    interpreter.interpret(bin_path, result_log, 0, 4)
    assert interpreter.MEMORY[100] == 100

def test_read(setup):
    source_path, bin_path, log_path, result_log = setup
    asm_code = '''
        LOAD #100
        WRITE [1]
        LOAD #200
        READ [1]
    '''
    with open(source_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(source_path, bin_path, log_path)
    interpreter.interpret(bin_path, result_log, 0, 4)
    assert interpreter.REGISTER_AC == 100

def test_minus(setup):
    source_path, bin_path, log_path, result_log = setup
    asm_code = '''
        LOAD #100
        MINUS
    '''
    with open(source_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(source_path, bin_path, log_path)
    interpreter.interpret(bin_path, result_log, 0, 4)
    assert interpreter.REGISTER_AC == -100

def test_prog(setup):
    source_path, bin_path, log_path, result_log = setup
    asm_code = '''
        LOAD #-100
        WRITE [0]
        LOAD #-200
        WRITE [1]
        LOAD #300
        WRITE [2]
        LOAD #400
        WRITE [3]
        READ [0]
        MINUS
        WRITE [0]
        READ [1]
        MINUS
        WRITE [1]
        READ [2]
        MINUS
        WRITE [2]
        READ [3]
        MINUS
        WRITE [3]
    '''
    with open(source_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(source_path, bin_path, log_path)
    interpreter.interpret(bin_path, result_log, 0, 4)
    assert interpreter.MEMORY[0] == 100
    assert interpreter.MEMORY[1] == 200
    assert interpreter.MEMORY[2] == -300
    assert interpreter.MEMORY[3] == -400

def test_binary(setup):
    source_path, bin_path, log_path, result_log = setup
    asm_code = '''
        LOAD #909
        READ [168]
        WRITE [394]
        MINUS
    '''
    with open(source_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(source_path, bin_path, log_path)
    with open(bin_path, 'rb') as f:
        byte = f.read()
    assert byte[0:3] == b'\x71\xe3\x00'
    assert byte[3:8] == b'\x29\x2a\x00\x00\x00'
    assert byte[8:13] == b'\x97\x62\x00\x00\x00'
    assert byte[13:14] == b'\x2a'