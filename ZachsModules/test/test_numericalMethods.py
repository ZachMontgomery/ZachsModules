from ZachsModules import numericalMethods as nm


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
    
    args = (1., 2.)
    kws = {'kw1': 3., 'kw2': 4.}
    stepSizes = [0.1, 0.01, 0.001]
    def f0(x, a1, a2, kw1=0., kw2=0.):
        return  a1*x[0] +  a2*x[1] + kw1*x[2] + kw2*sum(x)
    def f1(x, a1, a2, kw1=0., kw2=0.):
        return  a2*x[0] + kw1*x[1] + kw2*x[2] +  a1*sum(x)
    def f2(x, a1, a2, kw1=0., kw2=0.):
        return kw1*x[0] + kw2*x[1] +  a1*x[2] +  a2*sum(x)
    def f3(x, a1, a2, kw1=0., kw2=0.):
        return kw2*x[0] +  a1*x[1] +  a2*x[2] + kw1*sum(x)
    funcs = [f0, f1, f2, f3]
    x0 = [1.,1.,1.]
    
    assert nm.jacobian(funcs, x0, h=stepSizes, return_np=False, args=args, kwargs=kws) == nm.zList(4,3, val=(
                            5.0, 5.999999999999872, 6.999999999997897,
                            2.9999999999999893, 4.000000000000092, 4.999999999999005,
                            5.0, 5.999999999999872, 3.0000000000001137,
                            7.0000000000000195, 3.9999999999999147, 4.999999999999005))
        
    assert nm.jacobian(f0, x0, h=stepSizes, return_np=False, args=args, kwargs=kws) == nm.zList(3, val=(
                            5.0, 5.999999999999872, 6.999999999997897))

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

def test_zSort():
    assert 'zSort' in dir(nm)

