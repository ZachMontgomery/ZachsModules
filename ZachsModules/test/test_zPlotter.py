from ZachsModules import zPlotter as zp


def test_rcParams():
    assert 'rcParams' in dir(zp)

def test_plt():
    assert 'plt' in dir(zp)

def test_createBasePlot():
    assert 'createBasePlot' in dir(zp)

def test_updateRCParams():
    assert 'updateRCParams' in dir(zp)

def test_formatAxis():
    assert 'formatAxis' in dir(zp)

def test_saveFigEMF():
    assert 'saveFigEMF' in dir(zp)

def test_minorTickStep():
    assert 'minorTickStep' in dir(zp)

