import numpy as np

def theta2s(theta):
    return -1.*np.cos(theta)

def calcKappaD_lifting_line(Ra,Rt,N=100, omega=None, CLa=2.*np.pi):
    
    bw = Ra
    cr = 2. / (1.+Rt)
    ct = 2.*Rt / (1.+Rt)
    
    #calulate different geometries with the wing as a function of span
    #=====================================================================================================================
    dtheta = np.pi / float(N-1)
    theta = np.zeros(N)
    
    c = np.zeros(N)
    
    z = np.zeros(N)
    dz = bw / float(N-1)
    
    toler = 1.e-12
    
    twist = np.zeros(N)
    
    for i in range(N):
        #cosine clustering
        theta[i] = np.pi * float(i) / float(N-1)
        z[i] = bw * theta2z(theta[i])
        # #even spacing
        # z[i] = -bw / 2. + dz * float(i)
        # theta[i] = np.arccos(-2.*z[i]/bw)
        
        if ct >= 0.:
            c[i] = interpolate(0.,bw/2.,abs(z[i]),cr,ct)
        else:
            c[i] = cr * sin(theta[i])
            print('using elliptic planform shape')
        if c[i] <= 0.: c[i] = 1.e-16
        
        if omega == None:
            twist[i] = 0.
        else:
            twist[i] = omega(z[i])
        
    
    #calulate the coefficient matrix and an vector
    #====================================================================================================================
    rhs1 = np.zeros(N)
    A = np.zeros((N,N))
    for i in range(N):
        rhs1[i] = 1.
        for j in range(N):
            n = float(j + 1)
            if i == 0:
                A[i,j] = n ** 2.
            elif i == N-1:
                A[i,j] = (-1.0) ** (n+1.) * n ** 2.
            else:
                A[i,j] = (4.*bw/CLa/c[i]+n/np.sin(theta[i]))*np.sin(n*theta[i])
    an = np.linalg.solve(A,rhs1)
    
    if omega != None:
        #calulate the bn vector
        #=================================================================================================================
        rhs2 = np.zeros(N)
        for i in range(N):
            #user given twist distribution
            rhs2[i] = twist[i]
        bn = np.linalg.solve(A,rhs2)
    
    #calulate the kappa values
    #=====================================================================================================================
    kappa_D = 0.
    kappa_DL = 0.
    kappa_DOmega = 0.
    for i in range(N):
        if i == 0:
            continue
        n = float(i+1)
        kappa_D += n * (an[i] / an[0]) ** 2.
        if omega != None:
            kappa_DL += 2.*bn[0]/an[0]*n*an[i]/an[0]*(bn[i]/bn[0]-an[i]/an[0])
            kappa_DOmega += (bn[0]/an[0])**2.*n*(bn[i]/bn[0]-an[i]/an[0])**2.
    kappa_L = (1.-(1.+np.pi*Ra/CLa)*an[0])/(1.+np.pi*Ra/CLa)/an[0]
    
    
    if omega != None:
        kappa_D0 = kappa_D - kappa_DL ** 2. / 4. / kappa_DOmega
        return kappa_D, kappa_L, kappa_DL, kappa_DOmega, kappa_D0
    else:
        return kappa_D, kappa_L

def calcChord(Rt, cw=1.0):
    return 2.*cw/(1.+Rt), 2.*Rt*cw/(1.+Rt)

def calcKappaL(Ra, CLa, CLa_sect=2.*np.pi):
    return CLa_sect/(1.+CLa_sect/np.pi/Ra)/CLa-1.

def Earth2BodyRot(vec,EulerAngles):
    phi,theta,psi = EulerAngles
    Cphi = np.cos(phi)
    Sphi = np.sin(phi)
    Ctheta = np.cos(theta)
    Stheta = np.sin(theta)
    Cpsi = np.cos(psi)
    Spsi = np.sin(psi)
    mat = np.zeros((3,3))
    mat[0,0] = Ctheta * Cpsi
    mat[0,1] = Sphi * Stheta * Cpsi - Cphi * Spsi
    mat[0,2] = Cphi * Stheta * Cpsi + Sphi * Spsi
    mat[1,0] = Ctheta * Spsi
    mat[1,1] = Sphi * Stheta * Spsi + Cphi * Cpsi
    mat[1,2] = Cphi * Stheta * Spsi - Sphi * Cpsi
    mat[2,0] = -Stheta
    mat[2,1] = Sphi * Ctheta
    mat[2,2] = Cphi * Ctheta
    return np.dot(mat,vec)

def Body2EarthRot(vec,EulerAngles):
    phi,theta,psi = EulerAngles
    Cphi = np.cos(phi)
    Sphi = np.sin(phi)
    Ctheta = np.cos(theta)
    Stheta = np.sin(theta)
    Cpsi = np.cos(psi)
    Spsi = np.sin(psi)
    mat = np.zeros((3,3))
    mat[0,0] = Ctheta * Cpsi
    mat[1,0] = Sphi * Stheta * Cpsi - Cphi * Spsi
    mat[2,0] = Cphi * Stheta * Cpsi + Sphi * Spsi
    mat[0,1] = Ctheta * Spsi
    mat[1,1] = Sphi * Stheta * Spsi + Cphi * Cpsi
    mat[2,1] = Cphi * Stheta * Spsi - Sphi * Cpsi
    mat[0,2] = -Stheta
    mat[1,2] = Sphi * Ctheta
    mat[2,2] = Cphi * Ctheta
    return np.dot(mat,vec)


def airfoilDataFileCreator(f, bnds, filename, step=0.1, maxCD=2., maxCm=0.5):
    N = int(180./step)
    AOA = np.linspace(-90,90,N)
    fil = open(filename, 'w')
    fil.write( csvLineWrite('aoa (deg)', 'CL', 'CD', 'Cm') )
    d2r = np.pi / 180.
    CL_l_bnd = f[0](bnds[0][0]*d2r)
    CL_u_bnd = f[0](bnds[0][1]*d2r)
    CD_l_bnd = f[1](bnds[1][0]*d2r)
    CD_u_bnd = f[1](bnds[1][1]*d2r)
    Cm_l_bnd = f[2](bnds[2][0]*d2r)
    Cm_u_bnd = f[2](bnds[2][1]*d2r)
    # dCL, dCD, dCm = [], [], []
    for aoa in AOA:
        #calc CL
        if aoa < bnds[0][0]:
            CL = CL_l_bnd/2. * (1. - np.cos(d2r*(180./(bnds[0][0]+90.)*(aoa+90.))))
        elif aoa > bnds[0][1]:
            CL = CL_u_bnd/2. * (1. + np.cos(d2r*(180./(90.-bnds[0][1])*(aoa-bnds[0][1]))))
        else:
            CL = f[0](aoa*d2r)
        #calc CD
        if aoa < bnds[1][0]:
            temp = (maxCD-CD_l_bnd)/2.
            CD = temp + CD_l_bnd + temp * np.cos(d2r*(180./(bnds[1][0]+90.)*(aoa+90.)))
        elif aoa > bnds[1][1]:
            temp = (maxCD-CD_u_bnd)/2.
            CD = temp + CD_u_bnd - temp * np.cos(d2r*(180./(90.-bnds[1][1])*(aoa-bnds[1][1])))
        else:
            CD = f[1](aoa*d2r)
        #calc Cm
        if aoa < bnds[2][0]:
            temp = (-maxCm-Cm_l_bnd)/2.
            Cm = temp + Cm_l_bnd + temp * np.cos(d2r*(180./(bnds[2][0]+90.)*(aoa+90.)))
        elif aoa > bnds[2][1]:
            temp = (maxCm-Cm_u_bnd)/2.
            Cm = temp + Cm_u_bnd - temp * np.cos(d2r*(180./(90.-bnds[2][1])*(aoa-bnds[2][1])))
        else:
            Cm = f[2](aoa*d2r)
        # dCL.append(CL)
        # dCD.append(CD)
        # dCm.append(Cm)
        fil.write( csvLineWrite(aoa,CL,CD,Cm) )
    fil.close()
    # return AOA, dCL, dCD, dCm

def readMachUpDistFile(fn):
    f = open(fn, 'r')
    fdata = f.readlines()
    f.close()
    
    temp = mySplit(fdata[0], sep=' \n')
    data = {}
    for t in temp:
        data[t] = []
    
    types = [float]*(len(temp)-1)
    for line in fdata[1:]:
        vals = csvLineRead(line[20:], sep=' '*5, obj_type=types)
        data[temp[0]].append( line[:20].strip() )
        for j,t in enumerate(temp[1:]):
            data[t].append( vals[j] )
    
    return data

def splitMachUpDistFile(data):
    
    d = {}
    cols = [col for col in data if col != 'WingName']
    
    for i, wingname in enumerate(data['WingName']):
        if not wingname in d:
            d[wingname] = {}
            for col in cols:
                d[wingname][col] = []
        
        for col in cols:
            d[wingname][col].append( data[col][i] )
    
    return d


def sortMachUpDistFile(d, col='ControlPoint(y)', ascend=True):
    
    items = [d[i] for i in d if i != col]
    
    zSort(d[col], *items, ascend=ascend)
    
    dt = [d[col][i+1]-d[col][i] for i in range(len(d[col])-1)]
    
    sd, m = zStDev(dt)
    sd *= 4
    
    gaps = []
    for i,t in enumerate(dt):
        if not isClose(t, m, tol=sd):
            gaps.append(i+1)
    
    
    for gap in gaps:
        
        for i in d:
            d[i].insert(gap, None)



def airfoilGeometry2Norms(xx, yy, n):
    '''
    inputs:
    xx, yy = list of points describing the airfoil geometry with LE (0,0) and 
        TE (1,0) before any flap deflections
    n = number discertized points for normal vectors on surface of the 
        airfoil that are cosine clustered at the LE and TE (int)
    
    outputs:
    norms = list of normal angles around the surface of the airfoil with n 
        locations cosine clustered at the LE and TE
    X, Y = list of the point on the airfoil surface cooresponding to the 
        norm values
    '''
    
    x, y = list(xx), list(yy)
    pts = len(x)
    s = [i for i in range(pts)]
    
    N = [i for i in np.linspace(0, pts-1, n)]
    
    X = [interpolate_1D(s, x, i) for i in N]
    Y = [interpolate_1D(s, y, i) for i in N]
    
    norms = [None]*n
    h = 0.05e-2
    
    for i,I in enumerate(N):
        
        IL = I - h
        IH = I + h
        
        if IL < 0:
            IL = 0.
            IH += h
        if IH > pts-1:
            IH = pts-1.
            IL -= h
        
        x1 = interpolate_1D(s, x, IL)
        x2 = interpolate_1D(s, x, IH)
        y1 = interpolate_1D(s, y, IL)
        y2 = interpolate_1D(s, y, IH)
        
        surfGradAngle = np.arctan2(y2-y1, x2-x1)
        norms[i] = surfGradAngle + np.pi / 2.
        if norms[i] > np.pi:
            norms[i] -= 2.*np.pi
        elif norms[i] < -np.pi:
            norms[i] += 2.*np.pi
    
    return norms, X, Y

def airfoilPressureDist(norms, X, Y, CL, CD, Cm, alpha=0.):
    '''
    inputs:
    norms = list of normal angles around the surface of the airfoil with n 
        locations cosine clustered at the LE and TE clockwise rotation
    X, Y = list of the point on the airfoil surface cooresponding to the 
        norm values, normalized by the section chord length
    CL = section lift coefficient (float)
    CD = section drag coefficient (float)
    Cm = section pitching moment coefficient (float)
    alpha = optional, section angle of attack, default of 0 (degree)
    
    outputs:
    CP = list of the coefficient of pressure values at the X,Y locations 
        that satisfy the net CL, CD, and Cm values for the airfoil section
    '''
    
    n = len(X)
    S = [i for i in range(n)]
    
    alpha *= np.pi/180.
    Cz = -CL*np.cos(alpha) - CD*np.sin(alpha)
    Cx =  CL*np.sin(alpha) - CD*np.cos(alpha)
    
    CPdes = (0.05, 0.1, -0.5, -0.05) #(0.5, 0.1, -0.1, -3.0)
    bnds = (0, 0.25, 0.5, 0.75, 1) #(1,0.75,0.5,0.25,0)
    
    # CP = [None]*n
    # for i in range(n):
        # s = S[i] / (n-1)
        # for j in range(4):
            # if s <= bnds[j+1]:
                # CP[i] = CPdes[j]
                # break
        # if CP[i] == None: CP[i] = 0.
    
    # CPdes = CP[:]
    CP = [-0.5]*n
    CPdes = [-0.5]*n
    
    def Cz_cons(cp):
        # z = 0.
        # for i in S:
            # if norms[i] >= 0: #top surface in normal-axial reference
                # z += -cp[i] * np.sin(norms[i])
            # else:
                # z += cp[i] * np.sin(norms[i])
        
        Fz = trap(X, cp)
        
        return (Fz-Cz)*1.
    
    def Cx_cons(cp):
        # x = 0.
        # for i in S:
            # if isClose(norms[i], 0., tol=np.pi/2.): #rear surface in normal-axial reference
                # x += -cp[i] * np.cos(norms[i])
            # else:
                # x += cp[i] * np.cos(norms[i])
        p = [-i for i in cp]
        
        Fx = trap(Y, p)
        
        return (Fx-Cx)*1.
    
    def Cm_cons(cp):
        # m = 0.
        # for i in S:
            
            # if isClose(norms[i], 0., tol=np.pi/2.):
                # Fx = -cp[i] * np.cos(norms[i])
            # else:
                # Fx = cp[i] * np.cos(norms[i])
            
            # if norms[i] >= 0:
                # Fz = -cp[i] * np.sin(norms[i])
            # else:
                # Fz = cp[i] * np.sin(norms[i])
            
            # m += -Fx*Y[i] + Fz*(X[i]-0.25)
        
        # for i in range(n):
            # fx[i] = 
        
        # x = [i-0.25 for i in X]
        # m = trap(x, 
        
        return 0#(m-Cm)*1.
    
    cons = ({'type' : 'eq', 'fun': Cz_cons},
            {'type' : 'eq', 'fun': Cx_cons})#,
            # {'type' : 'eq', 'fun': Cm_cons})
    
    def PressureError(cp):
        er = 0.
        for i in range(n):
            er += abs(cp[i] - CPdes[i])
        return er
    
    bnds = tuple([(None, 1.)]*n)
    
    from scipy.optimize import minimize
    sol = minimize(PressureError, CP, method = 'SLSQP',
        options = {'ftol': 1.0e-10, 'disp': True, 'maxiter' : 250 },
        constraints = cons,
        bounds = bnds)
    
    
    
    return sol.x, Cz_cons(sol.x)+Cz, Cx_cons(sol.x)+Cx, Cm_cons(sol.x)+Cm
    
    

def quat2euler(e):
    
    e0, ex, ey, ez = e
    
    temp = e0*ey - ex*ez
    
    if abs(temp) == 0.5:
        theta = np.pi / 2 * np.sign(temp)
        psi = 0
        phi = 2*np.arcsin(ex / np.cos(pi/4)) + psi * np.sign(temp)
    else:
        phi = np.arctan2(2*(e0*ex + ey*ez), e0**2+ez**2-ex**2-ey**2)
        theta = np.arcsin(2*temp)
        psi = np.arctan2(2*(e0*ez + ex*ey), e0**2+ex**2-ey**2-ez**2)
    
    return phi, theta, psi

