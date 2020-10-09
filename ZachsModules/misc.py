
def isIterable(val):
    try:
        iter(val)
        return True
    except:
        return False


def mergeSort(u):
    n = len(u)
    if n <= 1: return u
    
    k = n//2
    l, r = u[:k], u[k:]
    
    l = mergeSort(l)
    r = mergeSort(r)
    
    return merge(l,r)

def merge(l, r):
    result = []
    
    while l != [] and r != []:
        if l[0] <= r[0]:
            result.append(l[0])
            l = l[1:]
        else:
            result.append(r[0])
            r = r[1:]
    
    if l != []: result += l
    if r != []: result += r
    return result



def nestedIF(d, *conds):
    s = ''
    for cond in conds:
        if cond(*args, **kwargs):
            s += '1'
        else:
            s += '0'
    return d.get(s, None)

def validBinary(x):
    l = list(str(x))
    if len(l) == l.count('1') + l.count('0'):
        return True
    else:
        return False

def int2bin(x):
    b = 0
    while x > 0:
        i = 0
        while x//2**i > 0:
            i += 1
        i -= 1
        b += 10**i
        x -= 2**i
    return b

class zBinary():
    
    def __init__(self, Int=None, Hexadecimal=None, Binary=None):
        self.b = 0
        if Binary != None:
            if validBinary(Binary): self.b = Binary
        elif Int != None:
            self.b = int2bin(Int)
        elif Hexadecimal != None:
            pass
    
    def __int__(self):
        b = self.b
        x = 0
        while b > 0:
            i = 0
            while b//10**i > 0:
                i += 1
            i -= 1
            x += 2**i
            b -= 10**i
        return x
    
    def __str__(self):
        return str(self.b)
    
    def __add__(self, x):
        return zBinary(Int= int(self) + int(x))
    
    def __radd__(self, x):
        return self + x
    
    def __sub__(self, x):
        return zBinary(Int= int(self) - int(x))
    
    def __rsub__(self, x):
        return zBinary(Int= int(x) - int(self))
    
    def __mul__(self, x):
        return zBinary(Int= int(self) * int(x))
    
    def __rmul__(self, x):
        return self * x
    
    def __div__(self, x):
        return zBinary(Int= int(int(self) / int(x)))
    
    def __truediv__(self, x):
        return self.__div__(x)
    
    def __rdiv__(self, x):
        return zBinary(Int= int(int(x) / int(self)))
    
    def __rtruediv__(self, x):
        return self.__rdiv__(x)

