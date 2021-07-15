from ..io import oneLineProgress, Progress, appendToFile
from ..misc import isIterable
# import numpy as np
from ..aerodynamics import np
from multiprocessing import Pool, cpu_count

nan = float('nan')

def interpolate(x1,x2,x,y1,y2):
    return (y2-y1)/(x2-x1)*(x-x1)+y1

def interpolate_1D(x,data,xval,returnIndex=False):
    x = list(x)
    imax = None
    imin = None
    if xval in x:
        i = x.index(xval)
        if i == len(x)-1:
            imax = i
            imin = i-1
        else:
            imin = i
            imax = i+1
    else:
        for i in range(len(x)-1):
            if x[i] < xval and xval < x[i+1]:
                imin = i
                imax = i+1
                break
    if imax == None: raise ValueError('xval is not in the bounds of x')
    val = interpolate(x[imin],x[imax],xval,data[imin],data[imax])
    if returnIndex:
        return val, [imin,imax]
    else:
        return val

def interpolate_2D(x,y,data,xval,yval,returnIndex=False,fixHoles=(False,)):
    x = list(x)
    y = list(y)
    imax = None
    imin = None
    if xval in x:
        i = x.index(xval)
        if i == len(x)-1:
            imax = i
            imin = i-1
        else:
            imin = i
            imax = i+1
    else:
        for i in range(len(x)-1):
            if x[i] < xval and xval < x[i+1]:
                imin = i
                imax = i+1
                break
    if imax == None: raise ValueError('xval of {} is not in the bounds of xmax {} and xmin {}'.format(xval,max(x),min(x)))
    jmax = None
    jmin = None
    if yval in y:
        j = y.index(yval)
        if j == len(y)-1:
            jmax = j
            jmin = j-1
        else:
            jmin = j
            jmax = j+1
    else:
        for j in range(len(y)-1):
            if y[j] < yval and yval < y[j+1]:
                jmin = j
                jmax = j+1
                break
    if jmax == None: raise ValueError('yval of {} is not in the bounds of ymax {} and ymin {}'.format(yval,max(y),min(y)))
    if fixHoles[0]:
        
        Imin,Imax,Jmin,Jmax = imin,imax,jmin,jmax                           #store original indices
        test = [True] * 4
        iminFlag,imaxFlag,jminFlag,jmaxFlag = True,True,True,True
        while True in test:                                                 #loop until no holes are found
            uu = data[imax,jmax]
            ul = data[imax,jmin]
            lu = data[imin,jmax]
            ll = data[imin,jmin]
            pts = [ll,lu,ul,uu]
            test = [False]*4
            for k,pt in enumerate(pts):
                if pt == None or pt != pt: test[k] = True
            if True in test:                                                #found a hole, need fixing
                if fixHoles[1] == 0:                                        #update the i values to fix holes
                    if (test[0] or test[1]) and (test[2] or test[3]):       #both sides need fixing
                        if imin > 0 and iminFlag and imax < len(x)-1 and imaxFlag:      #still room to move both sides
                            imin -= 1                                       #decrement bottom side
                            imax += 1                                       #increment upper side
                        elif imin > 1 and iminFlag:                         #if room to lower bottom but not raise upper
                            imaxFlag = False                                #trip upper flag
                            imax = imin - 1                                 #set imax to 1 lower than imin
                            imin -= 2                                       #decrement imin by 2
                        elif imax < len(x)-2 and imaxFlag:                  #if room to raise upper but not lower bottom
                            iminFlag = False                                #trip bottom flag
                            imin = imax + 1                                 #set imin to 1 higher than imax
                            imax += 2                                       #increment imax by 2
                        else:                                               #no room to move either side
                            raise ValueError('update i values, both sides, error')
                    elif test[0] or test[1]:                                #only bottom side needs fixing
                        if imin > 0 and iminFlag:                           #still room to lower bottom side
                            imin -= 1                                       #decrement bottom side
                        elif imax < len(x)-1:                               #no room to lower bottom side
                            iminFlag = False                                #trip flag to False
                            if imin < imax:                                 #check if first time after no room to lower
                                imin = imax+1                               #initialize imin for extrapolation
                            else:                                           #if not first time after no room to lower
                                imin += 1                                   #increment imin for extrapolation
                        else:                                               #no room on either side
                            raise ValueError('update i values, only min side, error')
                    elif test[2] or test[3]:                                #only top side needs fixing
                        if imax < len(x)-1 and imaxFlag:                    #still room to raise upper side
                            imax += 1                                       #increment upper side
                        elif imin > 0:                                      #no room to raise upper side
                            imaxFlag = False                                #trip flag to False
                            if imax > imin:                                 #check if firt time after no room to raise
                                imax = imin-1                               #initialize imax for extrapolation
                            else:                                           #if not first time after no room to raise
                                imax -= 1                                   #decrement imax for extrapolation
                        else:                                               #no room on either side
                            raise ValueError('update i values, only max side, error')
                else:                                                       #update the j values to fix holes
                    if (test[0] or test[1]) and (test[2] or test[3]):       #both sides need fixing
                        if jmin > 0 and jminFlag and jmax < len(y)-1 and jmaxFlag:      #still room to move both sides
                            jmin -= 1                                       #decrement bottom side
                            jmax += 1                                       #increment upper side
                        elif jmin > 1 and jminFlag:                         #if room to lower bottom but not raise upper
                            jmaxFlag = False                                #trip upper flag
                            jmax = jmin - 1                                 #set imax to 1 lower than imin
                            jmin -= 2                                       #decrement imin by 2
                        elif jmax < len(y)-2 and jmaxFlag:                  #if room to raise upper but not lower bottom
                            jminFlag = False                                #trip bottom flag
                            jmin = jmax + 1                                 #set imin to 1 higher than imax
                            jmax += 2                                       #increment imax by 2
                        else:                                               #no room to move either side
                            raise ValueError('update j values, both sides, error')
                    elif test[0] or test[1]:                                #only bottom side needs fixing
                        if jmin > 0 and jminFlag:                           #still room to lower bottom side
                            jmin -= 1                                       #decrement bottom side
                        elif jmax < len(y)-1:                               #no room to lower bottom side
                            jminFlag = False                                #trip flag to False
                            if jmin < jmax:                                 #check if first time after no room to lower
                                jmin = jmax+1                               #initialize imin for extrapolation
                            else:                                           #if not first time after no room to lower
                                jmin += 1                                   #increment imin for extrapolation
                        else:                                               #no room on either side
                            raise ValueError('update j values, only min side, error')
                    elif test[2] or test[3]:                                #only top side needs fixing
                        if jmax < len(y)-1 and jmaxFlag:                    #still room to raise upper side
                            jmax += 1                                       #increment upper side
                        elif jmin > 0:                                      #no room to raise upper side
                            jmaxFlag = False                                #trip flag to False
                            if jmax > jmin:                                 #check if firt time after no room to raise
                                jmax = jmin-1                               #initialize imax for extrapolation
                            else:                                           #if not first time after no room to raise
                                jmax -= 1                                   #decrement imax for extrapolation
                        else:                                               #no room on either side
                            raise ValueError('update j values, only max side, error')
        
        if fixHoles[1] == 0:
            u = interpolate(x[imin],x[imax],xval,lu,uu)
            l = interpolate(x[imin],x[imax],xval,ll,ul)
            val = interpolate(y[jmin],y[jmax],yval,l,u)
        else:
            u = interpolate(y[jmin],y[jmax],yval,ul,uu)
            l = interpolate(y[jmin],y[jmax],yval,ll,lu)
            val = interpolate(x[imin],x[imax],xval,l,u)
        
        if returnIndex:
            return val, [imin,imax,jmin,jmax]
        else:
            return val
        
        
    else:
        uu = data[imax,jmax]
        ul = data[imax,jmin]
        lu = data[imin,jmax]
        ll = data[imin,jmin]
        u = interpolate(x[imin],x[imax],xval,lu,uu)
        l = interpolate(x[imin],x[imax],xval,ll,ul)
        val = interpolate(y[jmin],y[jmax],yval,l,u)
        if returnIndex:
            return val, [imin,imax,jmin,jmax]
        else:
            return val

def trap(x,y):
    n = len(x)
    total = 0.
    for i in range(n-1):
        dx = x[i+1] - x[i]
        h = .5 * (y[i+1] + y[i])
        total += dx * h
    return total


def centralDifference(f, x, h = 0.5e-2, args = (), kwargs = {}):
    '''
    Computes the derivative using central differencing
    
    inputs
    ======
        f : callable
            function of the form f(x, *args, **kwargs). Object that f
            returns must be able to + and - itself, and divide by float as
            well as type(h). Object returned is typically float
        
        x : user defined
            independent variable(s). Must be able to add and subtract
            type(h). Typically float.
        
        h : user defined, optional
            step size used for the differencing. Must be albe to add and
            subtract with type(x) and divide with object that f returns.
            Typically a float. Defaults to 0.5e-2
        
        args : tuple, optional
            additional arguments to be passed to f
        
        kwargs : dictionary, optional
            additional keyword arguments to be passed to f
    
    returns
    =======
        user defined by f
            derivative of f with respect to x by central differencing with
            step size h
    '''
    if isIterable(h): return (f(x+h, *args, **kwargs)-f(x-h, *args, **kwargs))/2./sum(h)
    return (f(x+h, *args, **kwargs)-f(x-h, *args, **kwargs))/2./h

def newtonsMethod(f, val, xo, tol=1.0e-12, h=0.5e-2, maxIter=200, args=(), kwargs = {}, derivative=centralDifference, display=False, bounds = (None,None), relaxationFactor=1.0):
    ea = 1.
    count = 0
    # print('initial guess is ',xo)
    while ea > tol:
        count += 1
        
        if display: print('{:4d}  {:23.16e}'.format(count, xo))
        
        if bounds[0] != None and xo < bounds[0]: xo = bounds[0]
        if bounds[1] != None and xo > bounds[1]: xo = bounds[1]
        
        df = derivative(f, xo, h=h, args=args, kwargs=kwargs)
        if df == 0.:
            if display: text('0 derivative calc in newtonsMethod')
            df = 1.0e-10
        # print('df is ',df)
        xn = xo - (f(xo, *args, **kwargs) - val) / df * relaxationFactor
        ea = abs(xn-xo)
        # print(count,xo,xn)
        xo = xn
        if xn != xn:
            print('xn is a nan, ',xn)
        if count >= maxIter:
            if display: print('Too many iterations in newtonsMethod with an approximate error of {:.12e}'.format(ea))
            return None
    if display: print('newtonsMethod converged with {:.0f} iterations and an approximate error of {:.12e}'.format(count,ea))
    return xn

def mathText2float(t):
    items = ('(',')','^','*','/','+','-')  #maybe add trig stuff
    
    t = t.replace(' ', '')
    t = t.replace('\t', '')
    t = t.replace('\n', '')
    t = t.replace('**', '^')
    
    # counts = [None] * len(items)
    # for i,item in enumerate(items):
        # counts[i] = t.count(item)
    # print(counts)
    
    # l = []
    # for i,count in enumerate(counts):
        # for j in range(count):
            
    # ans = t.partition(
    
    l = []
    s = ''
    for c in t:
        if c in items:
            
            
            if s != '':
                
                if s[-1] == 'e' or s[-1] == 'E':
                    s += c
                    continue
                
                
                l.append(float(s))
                s = ''
            l.append(c)
        else:
            s += c
    if s != '':
        l.append(float(s))
    
    if l.count('(') < l.count(')'):
        raise ValueError('Too many end parenthesis ")"')
    while l.count('(') > l.count(')'):
        l.append(')')
    
    return zachSolve(l)

def zachSolve(l):
    
    # numbs = len([1 for i in l if type(i) == float])
    if len(l) == 3:
        
        a = l[0]
        o = l[1]
        b = l[2]
        if type(a) != float or type(o) != str or type(b) != float: raise ValueError('Inproper Math Format')
        if o == '+':
            return a+b
        elif o == '-':
            return a-b
        elif o == '*':
            return a*b
        elif o == '/':
            return a/b
        elif o == '^':
            return a**b
        else:
            raise ValueError('Inproper Math Operator')
        
    elif len(l) == 2:
        return float( str(l[0]) + str(l[1]) )
    elif len(l) == 1:
        return float(l[0])
    else:
        
        
        
        
        if l[0] == '+':
            return zachSolve(l[1:])
        elif l[0] == '-':
            return zachSolve([0.]+l)
        
        
        par1 = l.count('(')
        if par1 > 0:
            i = None
            par2 = -1
            for j,item in enumerate(l):
                if type(item) == float:
                    continue
                elif item == '(':
                    par2 += 1
                    if i == None: i = j+1
                elif item == ')':
                    if par2 > 0:
                        par2 -= 1
                    else:
                        temp = zachSolve( l[i:j] )
                        return zachSolve( l[:i-1] + [temp] + l[j+1:] )
            raise ValueError('Improper use of parenthesis')
        else:
            
            for i in range(len(l)):
                if i%2 == 0 and type(l[i]) != float: raise ValueError('Improper Math Format')
                if i%2 == 1 and type(l[i]) == float: raise ValueError('Improper Math Format')
            
            # levels = []
            # for i in range(1,len(l),2):
                # if l[i] == '^':
                    # levels.append(1)
                # elif l[i] in ['*','/']:
                    # levels.append(2)
                # elif l[i] in ['+','-']:
                    # levels.append(3)
                # else:
                    # raise ValueError('Unknown operator {}'.format(l[i]))
            
            # for j in range(len(levels)):
                
                # if level
            
            for i in range(len(l)):
                if i%2 == 0: continue
                if l[i] == '^':
                    temp = zachSolve( l[i-1:i+2] )
                    return zachSolve( l[:i-1] + [temp] + l[i+2:] )
            for i in range(len(l)):
                if i%2 == 0: continue
                if l[i] in ['*','/']:
                    temp = zachSolve( l[i-1:i+2] )
                    return zachSolve( l[:i-1] + [temp] + l[i+2:] )
            for i in range(len(l)):
                if i%2 == 0: continue
                if l[i] in ['+','-']:
                    temp = zachSolve( l[i-1:i+2] )
                    return zachSolve( l[:i-1] + [temp] + l[i+2:] )
            raise ValueError('This should never display: {}'.format(l))



class zList():
    
    def __init__(self, *Nvec, val=None):
        
        self.__Nvec = Nvec
        self.shape = self.__Nvec[:]
        self.__V = len(self.__Nvec)
        self.ndim = self.__V
        # self.__J = 1
        # for n in Nvec:
            # self.__J *= n
        self.__calcJ()
        
        if val == 'ascend':
            self.__matrix = [i for i in range(self.__J)]
        elif val == 'descend':
            self.__matrix = [i for i in range(self.__J,0,-1)]
        elif isIterable(val):
            if len(val) == self.__J:
                self.__matrix = [i for i in val]
            else:
                raise ValueError('\n'*3+'zList Error: optional val argument doesn\'t agree with previous sizing arguments'+'\n'*3)
        else:
            self.__matrix = [val]*self.__J
    
    def __calcJ(self):
        self.__J = 1
        for n in self.__Nvec:
            self.__J *= n
    
    def __len__(self):
        return self.__J
    
    # def shape(self):
        # return self.__Nvec
    
    def compose_j(self, index):
        j = 0
        for v in range(1,self.__V+1):
            prod = 1
            for w in range(v+1,self.__V+1):
                prod *= self.__Nvec[w-1]
            j += index[v-1] * prod
        return j
    
    def decompose_j(self, j):
        n = [None]*self.__V
        for v in range(self.__V,0,-1):
            denom = 1
            for w in range(v+1,self.__V+1):
                denom *= self.__Nvec[w-1]
            summ = 0
            for u in range(v+1,self.__V+1):
                prod = 1
                for s in range(u+1,self.__V+1):
                    prod *= self.__Nvec[s-1]
                summ += n[u-1] * prod
            n[v-1] = int(round( ((j-summ)/denom)%(self.__Nvec[v-1])))
        return n
    
    def __getitem__(self, index):
        
        if type(index) == tuple:
            
            shape = []
            indices = []
            for i,ind in enumerate([i for i in index if i != None]):
                indices.append([])
                if type(ind) == slice:
                    count = 0
                    step = ind.step
                    start = ind.start
                    stop = ind.stop
                    if step == None: step = 1
                    if start == None: start = 0
                    if stop == None: stop = self.__Nvec[i]
                    for j in range(start, stop, step):
                        count += 1
                        indices[i].append(j)
                    shape.append(count)
                    
                elif type(ind) == int:
                    shape.append(1)
                    indices[i].append(ind)
                else:
                    raise ValueError('\n\nUnexpected item in index for zList. Expected an int or slice not {}'.format(type(ind)))
                
                if indices[i] == []: raise ValueError('Slice on axis {} is invalid'.format(i))
            
            reshaped = [i for i in shape if i > 1]
            if reshaped == []: return self.__matrix[ self.compose_j(index) ]
            
            z = zList(*reshaped)
            J = len(z)
            
            dummy = zList(*shape)
            
            for j in range(J):
                nv = dummy.decompose_j(j)
                temp = [None] * len(nv)
                for i,n in enumerate(nv):
                    temp[i] = indices[i][n]
                z[j] = self.__matrix[ self.compose_j(temp) ]
            return z
            
        elif type(index) in (slice, int):
            temp = self.__matrix[ index ]
            if type(index) == int:
                return temp
            else:
                start, stop, step = index.start, index.stop, index.step
                if start == None: start = 0
                if step == None: step = 1
                if stop == None: stop = self.__J
                
                if stop < 0: stop += self.__J
                if start < 0: start += self.__J
                
                count = (stop - start) // abs(step)
                if count == 1: return temp
            
            z = zList(len(temp))
            for i,t in enumerate(temp):
                z[i] = t
            return z
    
    def __str__(self):
        if self.__V == 1:
            return str(self.__matrix)
        elif self.__V == 2:
            s = ''
            for i in range(self.__Nvec[0]):
                l = []
                for j in range(self.__Nvec[1]):
                    l.append( self[i,j] )
                s += str(l) + '\n'
            return s[:-1]
        else:
            return '{} dimensional matrix\nwith a size {}\nand {} total entries'.format(self.__V,self.__Nvec,self.__J)
    
    def __setitem__(self, index, value):
        
        if type(index) == tuple:
            
            shape = []
            indices = []
            for i,ind in enumerate(index):
                indices.append([])
                if type(ind) == slice:
                    count = 0
                    step = ind.step
                    start = ind.start
                    stop = ind.stop
                    if step == None: step = 1
                    if start == None: start = 0
                    if stop == None: stop = self.__Nvec[i]
                    for j in range(start, stop, step):
                        count += 1
                        indices[i].append(j)
                    shape.append(count)
                    
                elif type(ind) == int:
                    shape.append(1)
                    indices[i].append(ind)
                else:
                    raise ValueError('\n\nUnexpected item in index for zList. Expected an int or slice not {}'.format(type(ind)))
                
                if indices[i] == []: raise ValueError('Slice on axis {} is invalid'.format(i))
            
            reshaped = [i for i in shape if i > 1]
            if reshaped == []: self.__matrix[ self.compose_j(index) ] = value
            
            try:
                blah = iter(value)
                iterable = True
            except:
                iterable = False
            
            if iterable:
                dummy = zList(*shape)
                J = len(dummy)
                for j, val in zip(range(J), value):
                    nv = dummy.decompose_j(j)
                    temp = [None] * len(nv)
                    for i,n in enumerate(nv):
                        temp[i] = indices[i][n]
                    self.__matrix[ self.compose_j(temp) ] = val
            else:
                dummy = zList(*shape)
                J = len(dummy)
                for j in range(J):
                    nv = dummy.decompose_j(j)
                    temp = [None] * len(nv)
                    for i,n in enumerate(nv):
                        temp[i] = indices[i][n]
                    self.__matrix[ self.compose_j(temp) ] = value
            
        elif type(index) == int:
            self.__matrix[index] = value
        elif type(index) == slice:
            step = index.step
            start = index.start
            stop = index.stop
            if step == None: step = 1
            if start == None: start = 0
            if stop == None: stop = self.__J
            
            try:
                blah = iter(value)
                iterable = True
            except:
                iterable = False
            
            if iterable:
                for j, val in zip(range(start,stop,step), value):
                    self.__matrix[j] = val
            else:
                for j in range(start,stop,step):
                    self.__matrix[j] = value
    
    def __add__(self, x):
        z = zList(*self.__Nvec)
        if type(x) == zList:
            if x.shape != self.__Nvec: raise ValueError('Shapes of zList addition don\'t match with: {} and {}'.format(self.__Nvec, x.shape))
            for i in range(self.__J):
                z[i] = self.__matrix[i] + x[i]
        elif type(x) == list:
            for i in range(self.__J):
                z[i] = self.__matrix[i] + x[i]
        else:
            for i in range(self.__J):
                z[i] = self.__matrix[i] + x
        return z
    
    def __radd__(self, x):
        return self + x
    
    def __sub__(self, x):
        z = zList(*self.__Nvec)
        if type(x) == zList:
            if x.shape != self.__Nvec: raise ValueError('Shapes of zList subtraction don\'t match with: {} and {}'.format(self.__Nvec, x.shape))
            for i in range(self.__J):
                z[i] = self.__matrix[i] - x[i]
        elif type(x) == list:
            for i in range(self.__J):
                z[i] = self.__matrix[i] - x[i]
        else:
            for i in range(self.__J):
                z[i] = self.__matrix[i] - x
        return z
    
    def __rsub__(self, x):
        z = zList(*self.__Nvec)
        if type(x) == zList:
            if x.shape != self.__Nvec: raise ValueError('Shapes of zList subtraction don\'t match with: {} and {}'.format(self.__Nvec, x.shape))
            for i in range(self.__J):
                z[i] = x[i] - self.__matrix[i]
        else:
            for i in range(self.__J):
                z[i] = x - self.__matrix[i]
        return z
    
    def __mul__(self, x):
        z = zList(*self.__Nvec)
        if type(x) == zList:
            if x.shape != self.__Nvec: raise ValueError('Shapes of zList multiplication don\'t match with: {} and {}'.format(self.__Nvec, x.shape))
            for i in range(self.__J):
                z[i] = self.__matrix[i] * x[i]
        elif type(x) == list:
            for i in range(self.__J):
                z[i] = self.__matrix[i] * x[i]
        else:
            for i in range(self.__J):
                z[i] = self.__matrix[i] * x
        return z
    
    def __pow__(self, x):
        z = zList(*self.__Nvec)
        if isIterable(x) and len(x) == len(self):
            for i in range(self.__J):
                z[i] = self.__matrix[i] ** x[i]
        elif isIterable(x):
            raise ValueError('For zList power, exponent doesn\'t have the same length as zList')
        else:
            for i in range(self.__J):
                z[i] = self.__matrix[i] ** x
        return z
    
    def __rmul__(self, x):
        return self * x
    
    def __div__(self, x):
        z = zList(*self.__Nvec)
        if type(x) == zList:
            if x.shape != self.__Nvec: raise ValueError('Shapes of zList division don\'t match with: {} and {}'.format(self.__Nvec, x.shape))
            for i in range(self.__J):
                z[i] = self.__matrix[i] / x[i]
        elif type(x) == list:
            for i in range(self.__J):
                z[i] = self.__matrix[i] / x[i]
        else:
            for i in range(self.__J):
                z[i] = self.__matrix[i] / x
        return z
    
    def __truediv__(self, x):
        return self.__div__(x)
    
    def __rdiv__(self, x):
        z = zList(*self.__Nvec)
        if type(x) == zList:
            if x.shape != self.__Nvec: raise ValueError('Shapes of zList division don\'t match with: {} and {}'.format(self.__Nvec, x.shape))
            for i in range(self.__J):
                z[i] = x[i] / self.__matrix[i]
        elif type(x) == list:
            for i in range(self.__J):
                z[i] = x[i] / self.__matrix[i]
        else:
            for i in range(self.__J):
                z[i] = x / self.__matrix[i]
        return z
    
    def __rtruediv__(self, x):
        return self.__rdiv__(x)
    
    def __eq__(self, x):
        if self.shape != x.shape: return False
        for j in range(self.__J):
            if self[j] != x[j]: return False
        return True
    
    def transpose(self, axis=(0,1)):
        # if self.__V != 2: raise ValueError('transpose requires that the zList be 2D instead of {}D'.format(self.__V))
        
        Nvec = list(self.__Nvec)
        temp = Nvec[axis[0]]
        Nvec[axis[0]] = Nvec[axis[1]]
        Nvec[axis[1]] = temp
        
        z = zList(*Nvec)
        
        for j in range(self.__J):
            nv_old = self.decompose_j(j)
            nv_new = nv_old[:]
            
            temp = nv_new[axis[0]]
            nv_new[axis[0]] = nv_new[axis[1]]
            nv_new[axis[1]] = temp
            
            i = z.compose_j(nv_new)
            
            z[i] = self[j]
        
        return z
    
    def dot(self, x):
        if self.__V != 1: raise ValueError('zList.dot(), dot product requires that the zList be 1D instead of {}D'.format(self.__V))
        if len(x.shape) != 1: raise ValueError('zList.dot(), dot product requires that the input zList be 1D instead of {}D'.format(len(x.shape)))
        if self.__J != len(x): raise ValueError('zList.dot(), dot product requires that both arrays be the same length')
        return sum([i*j for i, j in zip(self, x)])
    
    def cross(self, x):
        if (self.__V, len(x.shape), self.__J, len(x)) != (1, 1, 3, 3): raise ValueError('zList.cross(), cross product requires that the zLists be 1D and 3 elements long')
        z = zList(3)
        z[0] = self[1]*x[2] - self[2]*x[1]
        z[1] = self[2]*x[0] - self[0]*x[2]
        z[2] = self[0]*x[1] - self[1]*x[0]
        return z
    
    def mag(self):
        if self.__V != 1: raise ValueError('zList.mag() requires that the zList be 1D instead of {}D'.format(self.__V))
        return ( sum([i**2. for i in self]) )**0.5
    
    def normalize(self):
        if self.__V != 1: raise ValueError('zList.normalize() requires that the zList be 1D instead of {}D'.format(self.__V))
        m = self.mag()
        z = zList(self.__J)
        for j in range(self.__J):
            z[j] = self.__matrix[j] / m
        return z
    
    def matMul(self, x):
        if (self.__V, len(x.shape)) != (2, 2): raise ValueError('zList.matMul requires that both matrices are 2D')
        m, n = self.shape
        M, N = x.shape
        if n != M: raise ValueError('zList.matMul requires that the inner dimensions of the matrix multiplication are the same length.')
        z = zList(m, N)
        for row in range(m):
            for col in range(N):
                z[row, col] = self[row, :].dot( x[:, col] )
        return z
    
    def invert(self):
        #check for issues
        if self.__V != 2: raise ValueError('zList.invert() requires that the matrix be 2D')
        if self.__Nvec[0] != self.__Nvec[1]: raise ValueError('zList.invert() requires that the matrix be square')
        
        #get rows and cols
        rows, cols = self.__Nvec
        
        def rearrangeRows(a):
            rows = a.shape[0]
            cols = rows
            
            checking = True
            
            while checking:
                flag = False
                for i in range(cols):
                    if isClose(a[i,i], 0.):
                        flag = False
                        for j in range(cols):
                            if isClose(a[i,j], 0.): continue
                            
                            temp = a[j,:]
                            a[j,:] = a[i,:]
                            a[i,:] = temp
                            flag = True
                            break
                            
                        if not flag: raise ValueError('zList.invert(), matrix not invertible')
                if not flag: checking = False
            
            return a
        
        #create the augmented matrix
        am = zList(rows, cols*2)
        for row in range(rows):
            for col in range(cols*2):
                if col < cols:
                    am[row,col] = self[row,col]
                elif row + cols == col:
                    am[row,col] = 1
                else:
                    am[row,col] = 0
        
        #zero out values by performing row operations
        finished = False
        flag = False
        while not finished:
            for col in range(cols):
                for row in range(rows):
                    if row != col:
                        if not isClose(am[col,col], 0.):
                            k = am[row,col] / am[col,col]
                            am[row,:] -= k * am[col,:]
                        else:
                            flag = True
                            break
                    elif isClose(am[row,col], 0.):
                        flag = True
                        break
                if flag: break
            
            if flag:
                am = rearrangeRows(am)
                flag = False
            else:
                finished = True
        
        #normalize left side so it is identity
        for i in range(rows):
            am[i,:] /= am[i,i]
        
        return am[:, self.__Nvec[1]:]
    
    def Axb(self, b):
        #get rows and cols
        n = self.__Nvec[0]
        
        def rearrangeRows(a):
            rows = a.shape[0]
            cols = rows
            
            checking = True
            
            while checking:
                flag = False
                for i in range(cols):
                    if isClose(a[i,i], 0.):
                        flag = False
                        for j in range(cols):
                            if isClose(a[i,j], 0.): continue
                            
                            temp = a[j,:]
                            a[j,:] = a[i,:]
                            a[i,:] = temp
                            flag = True
                            break
                            
                        if not flag: raise ValueError('zList.invert(), matrix not invertible')
                if not flag: checking = False
            
            return a
        
        #create the augmented matrix
        am = zList(n, n+1)
        for row in range(n):
            for col in range(n+1):
                if col < n:
                    am[row,col] = self[row,col]
                else:
                    am[row,col] = b[row]
        
        #zero out values by performing row operations
        finished = False
        flag = False
        while not finished:
            for col in range(n):
                for row in range(n):
                    if row != col:
                        if not isClose(am[col,col], 0.):
                            k = am[row,col] / am[col,col]
                            am[row,:] -= k * am[col,:]
                        else:
                            flag = True
                            break
                    elif isClose(am[row,col], 0.):
                        flag = True
                        break
                if flag: break
            
            if flag:
                am = rearrangeRows(am)
                flag = False
            else:
                finished = True
        
        #normalize left side so it is identity
        for i in range(n):
            am[i,:] /= am[i,i]
        
        return am[:, n]
    
    def append(self, *vals, axis=0):
        # if self.__V != 1: raise ValueError('Can only append onto zList with one dimension, not {}'.format(self.__V))
        
        # z = zList(self.__J + len(vals))
        
        # for i in range(len(z)):
            # if i < self.__J:
                # z[i] = self[i]
            # else:
                # z[i] = vals[i-self.__J]
        
        # self.__Nvec = z.shape
        # self.__J = len(z)
        # self.__matrix = [i for i in z]
        
        nvec = list(self.shape[:])
        nvec[axis] += len(vals)
        z = zList(*nvec)
        
        for j in range(len(self)):
            n = self.decompose_j(j)
            z[tuple(n)] = self[j]
        
        nvecNew = [nvec[i] for i in range(self.__V) if i != axis]
        nn = [i-1 for i in nvecNew]
        
        for i,val in enumerate(vals):
            n = [j-1 for j in self.shape]
            n[axis] += i+1
            
            if len(nvecNew) != 0:
                if val.shape != tuple(nvecNew):
                    raise ValueError('Appending item isn\'t the right shape')
                for j in range(len(val)):
                    m = val.decompose_j(j)
                    m.insert(axis, n[axis])
                    z[tuple(m)] = val[j]
            else:
                # j = z.compose_j(n)
                z[tuple(n)] = val
        
        self.__Nvec = z.shape[:]
        self.shape = z.shape[:]
        self.__J = len(z)
        self.__matrix = [i for i in z]
    
    def array(self):
        return np.array(self).reshape(self.shape)
    
    def write(self, fn):
        f = open(fn+'.zL', 'w')
        f.write( csvLineWrite(*self.__Nvec) )
        f.write( csvLineWrite(*self.__matrix) )
        f.close()
    
    def read(self, fn):
        f = open(fn+'.zL', 'r')
        self.__Nvec = tuple(csvLineRead( f.readline(), obj_type=int))
        self.__matrix = csvLineRead( f.readline(), obj_type=float)
        f.close()
        self.shape = self.__Nvec[:]
        self.__V = len(self.__Nvec)
        self.ndim = self.__V
        self.__calcJ()
        return self


def jacobian(f, x, df=centralDifference, h=0.5e-2, return_np=True, args=(), kwargs={}):
    '''
    Computes the jacobian of a system.
    
    inputs
    ======
        f : sequence type or callable
            sequence type iterable object where each element is callable of
            the form f[0](x, *args, **kwargs). Object returned by callable
            elements must be able to add and subtract similar types, divide
            floats type(h[0]). Object returned is typically float
        
        x : sequence type
            sequence type iterable object where the elements are the
            independent variables of the system. Element types must be able
            to add and subtract type(h[0]). Element types are typically
            floats.
        
        df : callable, optional
            callable object of the form, df(f, x, h=0.5e-2, *args, **kwargs)
            that returns the derivative of f with respect to x, with a step
            size h. Defaults to centralDifference. See centralDifference for
            more information.
        
        h : sequence type or user defined, optional
            step size to be used when numerically computing the derivative.
            When given as a sequence type, the length should match the that
            of x. 
    '''
    ## get number of equations and number of independent variables
    n = len(x)
    if isIterable(f):
        m = len(f)
        nvec = (m,n)
    else:
        m = 0
        nvec = (n,)
    ## ensure that h is iterable with length equal to x
    if isIterable(h):
        if len(h) != n: raise ValueError('jacobian step size h must either be the same length as number of variables or a constant value')
    else:
        h = [h]*n
    ## initialize jacobian
    jaco = zList(*nvec)
    ## check for multiple equations
    if m > 0:
        ## loop thru equations
        for i in range(m):
            ## loop thru variables
            for j in range(n):
                ## compute the ij component of the jacobian with df
                jaco[i,j] = df( f[i],
                                zList(n,val=x),
                                h=zList(n, val=[0. if k != j else h[j] for k in range(n)]),
                                args=args,
                                kwargs=kwargs)
    else:
        ## loop thru variables
        for j in range(n):
            ## compute the j component of the jacobian with df
            jaco[j] = df(   f,
                            zList(n,val=x),
                            h=zList(n, val=[0. if k != j else h[j] for k in range(n)]),
                            args=args,
                            kwargs=kwargs)
    if return_np: return jaco.array()
    return jaco

def newtonsMethodSystem(f, xo, tol=1.0e-12, h=0.5e-2, maxIter=200, args=(), kwargs={}, jacobian=jacobian, display=False, bounds=(None,None), la=1.):
    n = len(xo)
    if len(f) != n: raise ValueError('jacobian requires the same number of variables as equations')
    if isIterable(h):
        if len(h) != n: raise ValueError('jacobian step size h must either be the same length as number of equations or a constant value')
    else:
        h = [h]*n
    
    ea = 1.
    count = 0
    if display: print('Iteration   Error')
    
    while ea > tol:
        count += 1
        grad = jacobian(f, xo, h=h, args=args, kwargs=kwargs)
        nF = [-f[i](xo, *args, **kwargs) for i in range(n)]
        ea = max([abs(i) for i in nF])
        if display: print('{:9d}   {:19.12e}'.format(count, ea))
        dx = grad.Axb(nF)
        xn = xo + la * dx
        if count >= maxIter:
            if display: print('Too many interations in newtonsMethodSystem with an approximate error of {:.12e}'.format(ea))
            return None
    if display: print('newtonsMethodSystem converged with {:.0f} iterations and an approximate error of {:.12e}'.format(count,ea))
    return xn

def isClose(x, y, tol=1.e-12):
    return y-tol <= x and x <= y+tol



def quadratic(a,b,c):
    d = b**2-4*a*c
    x1 = (-b+d**0.5)/2/a
    x2 = (-b-d**0.5)/2/a
    return x1, x2


def zStDev(x, returnMean=True):
    N = len(x)
    xbar = zMean(x)
    
    c = 1/(N-1)
    summ = 0
    for i in x:
        summ += c * (i-xbar)**2
    if returnMean: return summ ** 0.5, xbar
    return summ ** 0.5

def zMean(x):
    summ = 0
    for i in x:
        summ += i
    return summ / len(x)


def odeEULER(dfunc, times, xo, h=0.5e-2):
    '''
    function odeEULER implements the euler method to integrate the ode
    forward in time
    
    inputs
        dfunc = function that containts the system of first order
            differential equations of the form xdot = F(t,x) where x is the
            state vector of the problem and t is the current time
        times = list containing the starting time and ending time for the
            integration
        xo = list containing the inital state vector
        h = step size for how far forward to step in time
    
    outputs
        t = list of times at all the steps in the integration
        x = zlist of the state vectors at each time step
    '''
    
    tstart, tend = times
    duration = tend - tstart
    Nsteps = int(duration / h)
    if duration % h > 0: Nsteps += 1
    Npts = Nsteps + 1
    
    t = [tstart+i*h for i in range(Npts)]
    
    V = len(xo)
    x = zList(Npts, V)
    
    x[0,:] = xo[:]
    
    for i in range(Nsteps):
        
        dx = dfunc(t[i], x[i,:])
        
        x[i+1,:] = x[i,:] + dx*h
    
    return t, x

def odeTRAP(dfunc, times, xo, h=0.5e-2):
    '''
    function odeTRAP implements the trapezoidal rule to integrate the ode
    forward in time
    
    inputs
        dfunc = function that containts the system of first order
            differential equations of the form xdot = F(t,x) where x is the
            state vector of the problem and t is the current time
        times = list containing the starting time and ending time for the
            integration
        xo = list containing the inital state vector
        h = step size for how far forward to step in time
    
    outputs
        t = list of times at all the steps in the integration
        x = zlist of the state vectors at each time step
    '''
    
    tstart, tend = times
    duration = tend - tstart
    Nsteps = int(duration / h)
    if duration % h > 0: Nsteps += 1
    Npts = Nsteps + 1
    
    t = [tstart+i*h for i in range(Npts)]
    
    V = len(xo)
    x = zList(Npts, V)
    
    x[0,:] = xo[:]
    
    for i in range(Nsteps):
        
        xdot1 = dfunc(t[i], x[i,:])
        xtemp = x[i,:] + xdot1*h
        xdot2 = dfunc(t[i+1], xtemp)
        
        x[i+1,:] = x[i,:] + h/2*(xdot1+xdot2)
    
    return t, x

def odeRK4Old(dfunc, times, xo, h=0.5e-2, n=300, tol=1e-5, verbose=True):
    '''
    function odeRK4 implements the fourth order Runge-Kutta to integrate the
    ode forward in time
    
    inputs
        dfunc = function that containts the system of first order
            differential equations of the form xdot = F(t,x) where x is the
            state vector of the problem and t is the current time
        times = list containing the starting time and ending time for the
            integration
        xo = list containing the inital state vector
        h = step size for how far forward to step in time
    
    outputs
        t = list of times at all the steps in the integration
        x = zlist of the state vectors at each time step
    '''
    
    tstart, tend = times
    duration = tend - tstart
    
    t = [tstart]
    
    V = len(xo)
    # x = [xo[:]]
    x = zList(1,V)
    x[:] = xo[:]
    H = [None]
    
    #initialize variables
    dxOld = zList(V, val=0.)
    i = 0
    prog = Progress(100, msg=['ODE solver RK4','Time Steps used: 1'])
    cOld = 1
    
    # loop thru until arriving at tend
    while t[i] < tend:
        
        
        if verbose:
            prog.Set((t[i] - tstart)/duration*100.)
            prog.msg[1] = 'Time Steps Used: {}'.format(i)
            prog.display()
        
        # initialize variables for the variable step finder
        badStep = True
        count = -1
        # reverseStep = False
        
        # loop until a suitable step size is found
        while badStep:
            count += 1
            
            # print('time loop iteration {}, and variable step size generator loop iteration {}'.format(i,count))
            
            # check if time step is nonpositive, and fix accordingly
            if h <= 0.:
                h = 1e-10
                input('h was nonpositive value')
            # check if the time step will take the integration past the stopping point
            if t[i] + h > tend:
                # force the time step to end at the stopping point
                h = tend - t[i]
                # force the variable step generator algorithm to accept this time step
                badStep = False
            
            
            # perform the RK4 integration
            k1 = dfunc(t[i], x[i,:])
            k2 = dfunc(t[i]+h/2, x[i,:]+h*k1/2)
            k3 = dfunc(t[i]+h/2, x[i,:]+h*k2/2)
            k4 = dfunc(t[i]+h, x[i,:]+h*k3)
            
            # print('\n'*5)
            # print(x[i,:].shape(), k1.shape())
            # print(k1)
            # print(x[i,:].shape(), k2.shape())
            # print(k2)
            # print(x[i,:].shape(), k3.shape())
            # print(k3)
            # print(x[i,:].shape(), k4.shape())
            # print(k4)
            # print(t[i])
            # print(t[i]+h/2)
            # print(t[i]+h)
            
            
            dxNew = 1/2*(k1+2*k2+2*k3+k4)
            
            
            if count == 100:
                h = duration/n/10**4
                badStep = False
                continue
            elif count > 100:
                break
            
            
            
            # approximate the local truncation error
            LTE = h/2 * (dxNew-dxOld).mag()
            c = LTE / h**4
            
            print('LTE {}'.format(LTE))
            print('c   {}'.format(c))
            
            # print(dxOld.shape())
            # print(dxNew.shape())
            # print(LTE)
            # print(c)
            # print(h)
            # input()
            
            # #encountering a new stiff change
            # if cOld <= 0 and c > 0 and not reverseStep:
                # #backup one time step
                # i -= 1
                # reverseStep = True
                # badStep = True
                # continue
            # elif reverseStep:
                # h = duration/n/10**4
                # break
            
            # cOld = c
            
            # check if c is positive
            if c > 0.:
                # calculate new time step
                hn = (tol / c) ** 0.25
                # limit the new time step to the max available
                if hn > duration/n: hn = duration/n
            # if c is 0 and not the final time step
            elif badStep:
                hn = duration/n
            
            
            if isClose(h, hn, tol=.05*h):
                badStep = False
            elif badStep:
                # h += 0.5*(hn-h)
                h = hn
        
        print('found step')
        print(x.shape())
        input()
        temp = zList(i+15,V)
        for I in range(i+1):
            for v in range(V):
                temp[I,v] = x[I,v]
        temp[i+1,:] = x[i,:] + dxNew*h
        x = temp[:,:]
        del temp
        # x.append( x[i] + dxNew*h )
        t.append( t[i] + h )
        H.append(h)
        dxOld = dxNew[:]
        i += 1
    if verbose:
        prog.Set(100.)
        prog.display()
    
    
    return t, x, H

def odeRK4(dfunc, times, xo, ufunc=None, h='auto', n=300, tol=1e-5, verbose=True, **kw):
    '''
    function odeRK4 implements the fourth order Runge-Kutta to integrate the
    ode forward in time
    
    inputs
        dfunc = function that containts the system of first order
            differential equations of the form xdot = F(t,x) where x is the
            state vector of the problem and t is the current time
        times = list containing the starting time and ending time for the
            integration
        xo = list containing the inital state vector
        h = step size for how far forward to step in time
    
    outputs
        t = list of times at all the steps in the integration
        x = zlist of the state vectors at each time step
    '''
    
    tstart, tend = times
    duration = tend - tstart
    
    # t = [tstart]
    # t = zList(1, val=tstart)
    if h == 'auto':
        hh = 'auto'
        h = 0.5e-2
    else:
        hh = 'fixed'
    V = len(xo)
    # x = [xo[:]]
    # x = zList(1,V, val=xo[:])
    # x[:] = xo[:]
    # H = zList(0)
    if ufunc != None:
        u = ufunc(tstart, xo)
    else:
        u=0.
    # U = zList(1,val=u)
    
    t = tstart
    x = zList(2, val=xo[:])
    # h = None
    
    data = zemptyFile()
    data.zwrite(t, *x, u, None)
    
    #initialize variables
    dxOld = zList(V, val=0.)
    i = 0
    if hh == 'auto':
        prog = Progress(100, msg=['ODE solver RK4','Time Steps used: 1'], **kw)
    else:
        prog = Progress(duration//h, msg='ODE solver RK4', **kw)
    cOld = 1
    
    # loop thru until arriving at tend
    # while t[i] < tend:
    while t < tend:
        
        if ufunc != None:
            # u = ufunc(t[i], x[i,:])
            u = ufunc(t, x)
        else:
            u=0.
        
        
        if hh == 'auto':
            # initialize variables for the variable step finder
            badStep = True
            count = -1
            # reverseStep = False
            
            # loop until a suitable step size is found
            while badStep:
                count += 1
                
                # check if time step is nonpositive, and fix accordingly
                if h <= 0.:
                    h = 1e-10
                    input('h was nonpositive value')
                # check if the time step will take the integration past the stopping point
                # if t[i] + h > tend:
                if t + h > tend:
                    # force the time step to end at the stopping point
                    # h = tend - t[i]
                    h = tend - t
                    # force the variable step generator algorithm to accept this time step
                    badStep = False
                
                
                # perform the RK4 integration
                # k1 = dfunc(t[i], x[i,:], u=u)
                # k2 = dfunc(t[i]+h/2, x[i,:]+h*k1/2, u=u)
                # k3 = dfunc(t[i]+h/2, x[i,:]+h*k2/2, u=u)
                # k4 = dfunc(t[i]+h, x[i,:]+h*k3, u=u)
                k1 = dfunc(t, x, u=u)
                k2 = dfunc(t+h/2, x+h*k1/2, u=u)
                k3 = dfunc(t+h/2, x+h*k2/2, u=u)
                k4 = dfunc(t+h, x+h*k3, u=u)
                
                
                
                dxNew = 1/2*(k1+2*k2+2*k3+k4)
                
                
                if count == 100:
                    h = duration/n/10**4
                    badStep = False
                    continue
                elif count > 100:
                    break
                
                
                
                # approximate the local truncation error
                LTE = h/2 * (dxNew-dxOld).mag()
                c = LTE / h**4
                
                
                # #encountering a new stiff change
                # if cOld <= 0 and c > 0 and not reverseStep:
                    # #backup one time step
                    # i -= 1
                    # reverseStep = True
                    # badStep = True
                    # continue
                # elif reverseStep:
                    # h = duration/n/10**4
                    # break
                
                # cOld = c
                
                # check if c is positive
                if c > 0.:
                    # calculate new time step
                    hn = (tol / c) ** 0.25
                    # limit the new time step to the max available
                    if hn > duration/n: hn = duration/n
                # if c is 0 and not the final time step
                elif badStep:
                    hn = duration/n
                
                
                if isClose(h, hn, tol=.05*h):
                    badStep = False
                elif badStep:
                    # h += 0.5*(hn-h)
                    h = hn
                
                
                if verbose:
                    # prog.Set((t[i] - tstart)/duration*100.)
                    prog.Set((t - tstart)/duration*100.)
                    prog.msg[1] = 'Time Steps Used: {}'.format(i)
                    prog.display()
        else:
            
            # if t[i] + h > tend:
            if t + h > tend:
                # force the time step to end at the stopping point
                # h = tend - t[i]
                h = tend - t
            
            
            # perform the RK4 integration
            # k1 = dfunc(t[i], x[i,:], u=u)
            # k2 = dfunc(t[i]+h/2, x[i,:]+h*k1/2, u=u)
            # k3 = dfunc(t[i]+h/2, x[i,:]+h*k2/2, u=u)
            # k4 = dfunc(t[i]+h, x[i,:]+h*k3, u=u)
            k1 = dfunc(t, x, u=u)
            k2 = dfunc(t+h/2, x+h*k1/2, u=u)
            k3 = dfunc(t+h/2, x+h*k2/2, u=u)
            k4 = dfunc(t+h, x+h*k3, u=u)
            
            dxNew = 1/2*(k1+2*k2+2*k3+k4)
            
            prog.display()
        
        # x.append( x[i,:] + dxNew*h )
        # t.append( t[i] + h )
        # H.append(h)
        # U.append(u)
        x = x + dxNew*h
        t += h
        data.zwrite(t, *x, u, h)
        dxOld = dxNew[:]
        i += 1
    if verbose and hh == 'auto':
        prog.Set(100.)
        prog.display()
    
    vals = data.getValues(obj_type=float)
    t = vals[:,0]
    x = vals[:,1:3]
    U = vals[:,3]
    H = vals[:,4]
    
    if ufunc == None:
        return t, x, H
    else:
        return t, x, H, U

def zSort(v, *W, ascend=True, verbose=True, msg='Sorting the arrays', c=0):
    k = len(v)
    for w in W:
        if len(w) != k: raise ValueError('All arrays need to be the same length in zSort')
    c = []
    if verbose: prog = oneLineProgress(sum([i for i in range(k)])+len(W), msg=msg, c=c)
    for m in range(k):
        for j in range(k-1,m,-1):
            i = j-1
            
            if (ascend and v[j] < v[i]) or (not ascend and v[j] > v[i]): # or (v[i] != v[i] and v[j] == v[j]):
                c.append(j)
                temp = v[j]
                v[j] = v[i]
                v[i] = temp
            if verbose: prog.display()
    
    for w in W:
        for j in c:
            i = j-1
            temp = w[j]
            w[j] = w[i]
            w[i] = temp
        if verbose: prog.display()


def runCases(func, it, fn, nBatch=None, progKW={}, chunkSize=1, cpus=cpu_count()):
    '''
    func: function handle that runs a single case that takes in a single
        argument (the arg can be a tuple of multiple objects) and returns a
        tuple of results to write to a line of the file
    it: an iterable contianing the input arguments for all the cases to be
        run (if multiple input args are needed for a single case, they need
        to be packaged together into a tuple).
    fn: str of the filename to write the data to. Writes the data into a csv
        format, with one line per case
    nBatch: number of cases to be run in parallel before writing the results
        to the file, optional
    chunkSize: number of cases to be sent to a single cpu during the
        parallel processing, defaults to 1
    cpus: number of cpus to use for parallel processing, defaults to all the
        cpus on your machine
    progKW: dictionary of keyword arguments to pass to the Progress bar,
        optional
    '''
    ## determine total number of cases
    J = len(it)
    ## determine batch size if not given
    if nBatch == None:
        if J > 10:
            nBatch = J // 10
        else:
            nBatch = J
    ## determine the number of batch runs
    nRuns = J // nBatch
    if J % nBatch != 0: nRuns += 1
    ## setup progress bar
    prog = Progress(nRuns, **progKW)
    ## loop thru batch runs
    for i in range(0,J,nBatch):
        if i+nBatch>J:          ## check to see if batch won't be full size
            n = J - i
            x = [None] * n
            with Pool(cpus) as pool:
                for j,ans in enumerate(pool.imap_unordered(func, it[i:], chunkSize)):
                    x[j] = ans
        else:
            x = [None] * nBatch
            with Pool(cpus) as pool:
                for j,ans in enumerate(pool.imap_unordered(func, it[i:i+nBatch], chunkSize)):
                    x[j] = ans
        
        appendToFile(fn, *x, multiLine=True)
        
        prog.display()
