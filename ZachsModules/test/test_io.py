from ZachsModules import io
from ZachsModules.numericalMethods import nan

def test_csvLineWrite():
    assert 'csvLineWrite' in dir(io)
    s = io.csvLineWrite(12, 32, True, 'This is a test.')
    assert s == " 1.2000000000000000e+01, 3.2000000000000000e+01,True,This is a test.\n"

def test_csvLineRead():
    assert 'csvLineRead' in dir(io)
    line = " 1.2000000000000000e+01, 3.2000000000000000e+01,True,                    nan,This is a test.\n"
    x = io.csvLineRead(line, obj_type=(float,float,bool,float,str))
    temp = [12.0, 32.0, 'True', nan, 'This is a test.']
    for i in range(len(temp)):
        if i == 3:
            assert x[i] != temp[i]
            continue
        assert x[i] == temp[i]

def test_text():
    assert 'text' in dir(io)

def test_oneLineText():
    assert 'oneLineText' in dir(io)

def test_pause():
    assert 'pause' in dir(io)

def test_stdout():
    assert 'stdout' in dir(io)

def test_deleteLastLines():
    assert 'deleteLastLines' in dir(io)

def test_Progress():
    assert 'Progress' in dir(io)

def test_dt():
    assert 'dt' in dir(io)

def test_td():
    assert 'td' in dir(io)

def test_oneLineProgress():
    assert 'oneLineProgress' in dir(io)

def test_mySplit():
    assert 'mySplit' in dir(io)

def test_appendToFile():
    assert 'appendToFile' in dir(io)

def test_tf():
    assert 'tf' in dir(io)

def test_zemptyFile():
    assert 'zemptyFile' in dir(io)

def test_colorText():
    assert 'colorText' in dir(io)

def test_textAlternate():
    assert 'textAlternate' in dir(io)

