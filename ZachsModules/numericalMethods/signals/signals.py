
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


class lowpassFilter():
    
    def __init__(self, *args):
        
        if len(args) == 2:
            tc, h = args
            a = h / (tc + h)
            self.set_a(a)
            if h > tc/5: text(['WARNING','time step {:.6e} is not <= time constant {:.6e} / 5'.format(h, tc),'for a lowpass filter object'])
        elif len(args) == 1:
            self.set_a(args[0])
        elif len(args) > 2:
            raise ValueError(text('Unexpected number of arguments to create lowpassFilter object',title='lowpassFilter __init__ error!',p2s=False))
        else:
            self.__a__ = None
        
        
        self.__past__ = None
    
    def set_a(self, a):
        if a >= 0. and a <= 1.:
            self.__a__ = a
        else:
            raise ValueError(text(['exponential factor not between 0 and 1','0 <= a <= 1'],title='lowpassFilter set_a error!',p2s=False))
    
    def get_a(self):
        return self.__a__
    
    def initialize(self, val):
        self.__past__ = val
    
    def update(self, val):
        if self.__past__ == None:
            self.__past__ = val
            return val
        else:
            self.__past__ = (1.-self.__a__) * self.__past__ + self.__a__ * val
            return self.__past__

class highpassFilter():
    
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


