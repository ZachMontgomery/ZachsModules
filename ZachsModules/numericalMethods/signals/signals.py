from ...misc import isIterable
from ...io import text
from numpy import pi

class runningAverage():
    
    def __init__(self, *args):
        
        self.__i = 0
        
        if len(args) == 2:
            self.__length = args[0]
            
            # try:
                # iter(args[1])
                # iterable = True
            # except:
                # iterable = False
            iterable = isIterable(args[1])
            
            if iterable and len(args[1]) == self.__length:
                self.__array = args[1][:]
            elif iterable:
                avg = sum(args[1]) / len(args[1])
                self.__array = [avg] * self.__length
            else:
                self.__array = [args[1]] * self.__length
            
        elif len(args) == 1:
            args = args[0]
            
            self.__length = args
            self.__array = [0.] * args
            
        else:
            raise ValueError('Unknown number of inputs')
    
    def average(self):
        return sum(self.__array) / self.__length
    
    def update(self, val):
        # del self.__array[0]
        # self.__array.append(val)
        # return self.average()
        
        self.__array[self.__i] = val
        self.__i += 1
        if self.__i >= self.__length: self.__i = 0
        return self.average()


class lowPassFilter():
    
    def __init__(self, freqHZ=None, timeConstant=None):
        
        if freqHZ == None and timeConstant == None:
            raise ValueError('Either the cut-off frequency or time constant needs to be specified.')
        elif timeConstant == None:
            self.__freq__ = freqHZ
            self.__tc__ = 1 / 2 / pi / freqHZ
        elif freqHZ == None:
            self.__tc__ = timeConstant
            self.__freq__ = 1 / 2 / pi / timeConstant
        else:
            if freqHZ != 1 / 2 / pi / timeConstant: raise ValueError('Given cut-off frequency, {} Hz, does not agree with given time constant, {} sec.'.format(freqHZ, timeConstant))
            self.__freq__ = freqHZ
            self.__tc__ = timeConstant
        
        self.time  = []
        self.value = []
    
    def update(self, t, v):
        if isIterable(t):
            if not isIterable(v) or len(v) != len(t): raise ValueError()
            t = list(t)
            v = list(v)
            
            if len(self.time) == 0:
                self.time.append(t.pop(0))
                self.value.append(v.pop(0))
            
            k = len(t)
            
            dt = [t[i] - t[i-1] if i > 0 else t[i] -  self.time[-1] for i in range(k)]
            a  = [i / (self.__tc__ + i) for i in dt]
            
            prev = self.value[-1]
            x = [None]*k
            for i in range(k):
                new = a[i] * v[i] + (1-a[i])*prev
                x[i] = new
                prev = new
            
            self.time  += t
            self.value += x
            return prev
        else:
            if isIterable(v): raise ValueError()
            
            prev = self.value[-1]
            
            dt = t - self.time[-1]
            dv = v - prev
            
            a = dt / (self.__tc__ + dt)
            
            new = prev + a * dv
            
            self.time.append(t)
            self.value.append(new)
            return new


class highPassFilter():
    
    def __init__(self, *args):
        
        if len(args) == 2:
            tc, h = args
            a = tc / (tc + h)
            self.set_a(a)
        elif len(args) == 1:
            self.set_a(args[0])
        elif len(args) > 2:
            raise ValueError(text('Unexpected number of arguments to create highpassFilter object',title='highpassFileter __init__ error!',p2s=False))
        else:
            self.__a__ = None
        
        self.__pastVal__, self.__pastInput__ = None, None
    
    def set_a(self, a):
        if isClose(a, 0.5, tol = 0.5):
            self.__a__ = a
        else:
            raise ValueError(text(['WARNING','exponential factor for high pass filter is not 0 <= a <= 1'],title='highpassFilter set_a error!',p2s=False))
    
    def get_a(self):
        return self.__a__
    
    def initialize(self, val):
        self.__pastVal__ = val
        self.__pastInput__ = val
    
    def update(self, inp):
        if None in (self.__pastVal__, self.__pastInput__):
            self.__pastVal__ = inp
            self.__pastInput__ = inp
            return inp
        else:
            self.__pastVal__ = self.__a__ * self.__pastVal__ + self.__a__ * (inp - self.__pastInput__)
            self.__pastInput__ = inp
            return self.__pastVal__


