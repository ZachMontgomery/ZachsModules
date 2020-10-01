from ZachsModules import nm


def test_nan():
    assert 'nan' in dir(nm)

def test_interpolate():
    assert 'interpolate' in dir(nm)

def test_interpolate_1D():
    assert 'interpolate_1D' in dir(nm)

def test_interpolate_2D():
    assert 'interpolate_2D' in dir(nm)

def test_trap():
    assert 'trap' in dir(nm)

def test_centralDifference():
    assert 'centralDifference' in dir(nm)

def test_newtonsMethod():
    assert 'newtonsMethod' in dir(nm)

def test_mathText2float():
    assert 'mathText2float' in dir(nm)

def test_zachSolve():
    assert 'zachSolve' in dir(nm)

def test_zList():
    assert 'zList' in dir(nm)

def test_jacobian():
    assert 'jacobian' in dir(nm)

def test_newtonsMethodSystem():
    assert 'newtonsMethodSystem' in dir(nm)

def test_isClose():
    assert 'isClose' in dir(nm)

def test_quadratic():
    assert 'quadratic' in dir(nm)

def test_zStDev():
    assert 'zStDev' in dir(nm)

def test_zMean():
    assert 'zMean' in dir(nm)

def test_odeEULER():
    assert 'odeEULER' in dir(nm)

def test_odeTRAP():
    assert 'odeTRAP' in dir(nm)

def test_odeRK4Old():
    assert 'odeRK4Old' in dir(nm)

def test_odeRK4():
    assert 'odeRK4' in dir(nm)

def test_signals():
    assert 'signals' in dir(nm)

def test_runningAverage():
    assert 'runningAverage' in dir(nm.signals)

def test_lowpassFilter():
    assert 'lowpassFilter' in dir(nm.signals)

def test_highpassFilter():
    assert 'highpassFilter' in dir(nm.signals)

