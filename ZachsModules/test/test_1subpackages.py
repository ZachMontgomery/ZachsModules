import ZachsModules as zm

def test_aero():
    assert 'aerodynamics' in dir(zm)

def test_io():
    assert 'io' in dir(zm)

def test_misc():
    assert 'misc' in dir(zm)

def test_nm():
    assert 'numericalMethods' in dir(zm)

def test_signals():
    assert 'signals' in dir(zm.numericalMethods)
