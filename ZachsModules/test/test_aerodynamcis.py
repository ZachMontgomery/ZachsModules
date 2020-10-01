from ZachsModules import aero


def test_theta2s():
    assert 'theta2s' in dir(aero)

def test_calcKappaD_lifting_line():
    assert 'calcKappaD_lifting_line' in dir(aero)

def test_calcChord():
    assert 'calcChord' in dir(aero)

def test_calcKappaL():
    assert 'calcKappaL' in dir(aero)

def test_Earth2BodyRot():
    assert 'Earth2BodyRot' in dir(aero)

def test_Body2EarthRot():
    assert 'Body2EarthRot' in dir(aero)

def test_airfoilDataFileCreator():
    assert 'airfoilDataFileCreator' in dir(aero)

def test_readMachUpDistFile():
    assert 'readMachUpDistFile' in dir(aero)

def test_sortMachUpDistFile():
    assert 'sortMachUpDistFile' in dir(aero)

def test_airfoilGeometry2Norms():
    assert 'airfoilGeometry2Norms' in dir(aero)

def test_airfoilPressureDist():
    assert 'airfoilPressureDist' in dir(aero)

