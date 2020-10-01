from ZachsModules import IO
from ZachsModules.numericalMethods import nan

def test_csvLineWrite():
    assert 'csvLineWrite' in dir(IO)
    s = IO.csvLineWrite(12, 32, True, 'This is a test.')
    assert s == " 1.2000000000000000e+01, 3.2000000000000000e+01,True,This is a test.\n"

def test_csvLineRead():
    assert 'csvLineRead' in dir(IO)
    line = " 1.2000000000000000e+01, 3.2000000000000000e+01,True,                    nan,This is a test.\n"
    x = IO.csvLineRead(line, obj_type=(float,float,bool,float,str))
    temp = [12.0, 32.0, 'True', nan, 'This is a test.']
    for i in range(len(temp)):
        if i == 3:
            assert x[i] != temp[i]
            continue
        assert x[i] == temp[i]

def test_text():
    assert 'text' in dir(IO)

def test_oneLineText():
    assert 'oneLineText' in dir(IO)

def test_pause():
    assert 'pause' in dir(IO)

def test_stdout():
    assert 'stdout' in dir(IO)

def test_deleteLastLines():
    assert 'deleteLastLines' in dir(IO)

def test_Progress():
    assert 'Progress' in dir(IO)

def test_dt():
    assert 'dt' in dir(IO)

def test_td():
    assert 'td' in dir(IO)

def test_oneLineProgress():
    assert 'oneLineProgress' in dir(IO)

def test_mySplit():
    assert 'mySplit' in dir(IO)

def test_appendToFile():
    assert 'appendToFile' in dir(IO)

def test_tf():
    assert 'tf' in dir(IO)

def test_zemptyFile():
    assert 'zemptyFile' in dir(IO)

def test_colorText():
    assert 'colorText' in dir(IO)

def test_textAlternate():
    assert 'textAlternate' in dir(IO)

