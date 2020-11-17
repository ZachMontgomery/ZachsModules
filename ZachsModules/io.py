# from ..aerodynamics import np
from .misc import isIterable
from numpy import float64

def csvLineWrite(*obj, sep=',', end='\n'):
    line = ''
    k = len(obj)
    if k == 0: return end
    for i,o in enumerate(obj):
        Sep = sep
        if i == k-1: Sep = ''
        if type(o) == float or type(o) == int or type(o) == float64:
            line += '{:23.16e}'.format(o) + Sep
        elif o == None:
            line += Sep
        else:
            line += str(o) + Sep
    return line+end

def csvLineRead(line, sep=',', end='\n', columns=None, obj_type=None):
    strings = line[:-len(end)].split(sep)
    if columns == None:
        if obj_type == None: return strings
        if not isIterable(obj_type): obj_type = [obj_type]*len(strings)
        data = [None] * len(strings)
        for i,s in enumerate(strings):
            if s == '': continue
            if obj_type[i] == float:
                data[i] = float(s)
            elif obj_type[i] == int:
                temp = float(s)
                data[i] = int(temp)
            else:
                data[i] = s
        return data
    else:
        if obj_type == None:
            while len(strings) < columns:
                strings.append(None)
            return strings[:columns]
        if not isIterable(obj_type): obj_type = [obj_type]*columns
        data = [None] * columns
        for i in range(columns):
            if i < len(strings):
                s = strings[i]
                if s == '': continue
                if obj_type[i] == float:
                    data[i] = float(s)
                elif obj_type[i] == int:
                    temp = float(s)
                    data[i] = int(temp)
                else:
                    data[i] = s
        return data

def text(*word, c=77, border=True, title=None, p2s=True):
    if len(word) == 1: word = word[0]
    s = '\n'
    if type(word) == list or type(word) == tuple:
        k = 0
        for w in word:
            if len(w) > c: c = len(w)
        if title != None: s += oneLineText(title, c=c, p=0, border=False, p2s=False) + '\n'
        if border: s += '='*c+'\n'
        for w in word:
            l = int((c-len(w))/2)
            s += '{}{}'.format(l*' ',w) + '\n'
        if border: s += '='*c+'\n'
    else:
        if len(word) > c: c = len(word)
        if title != None: s += oneLineText(title, c=c, p=0, border=False, p2s=False) + '\n'
        if border: s += '='*c+'\n'
        l = int((c - len(word)) / 2)
        s += '{}{}'.format(l*' ',word) + '\n'
        if border: s += '='*c+'\n'
    s += '\n'
    if p2s: print(s, end='')
    return s

def oneLineText(word, c=77, p=4, b='=', border=True, p2s=True):
    s = ''
    if len(word) > c: c = len(word)
    l = int((c-len(word)) / 2) - p
    if border:
        if l > 0:
            s += b*l + ' '*p
        else: s += ' '*(l+p)
    else: s += ' '*(l+p)
    s += word
    if border:
        if l > 0:
            s += ' '*p + b*l
        else: s += ' '*(l+p)
    if p2s: print(s)
    return s

def pause():
    text(['Paused','Press Enter to Continue'])
    input()

from sys import stdout
def deleteLastLines(n=1):
    for _ in range(n):
        stdout.write('\x1b[1A')
        stdout.write('\x1b[2K')

class xProgress():
    
    def __init__(self, Total, title=None, border=True, msg=[]):
        self.__total = Total
        self.__count = 0
        # self.__perc = 0.
        self.__rollTimer = dt.now()
        self.__rollDelta = 0.2
        self.__rollCount = -1
        self.__timer = dt.now()
        
        self.__kw = {'title':title, 'border':border}
        if type(msg) != list: msg = [msg]
        self.msg = msg
        text(*self.msg, ' ', ' ', **self.__kw)
        self.display()
    
    def __str__(self):
        # self.__perc = self.__count/self.__total*100
        # s = '{:7.3f}% finished'.format(self.__perc)
        # self.increment()
        # return s
        pass
    
    def increment(self):
        self.__count += 1
    
    def decrement(self):
        self.__count -= 1
    
    def __len__(self):
        l = len(str(self))
        self.decrement()
        return l
    
    def reset(self, Total):
        self.__total = Total
        self.__count = 0
    
    def Set(self, count):
        self.__count = count
    
    def display(self):
        rolling = '-\\|/'
        rollDelta = (dt.now() - self.__rollTimer).total_seconds()
        
        p2s = False
        if rollDelta >= self.__rollDelta or self.__rollCount == -1:
            p2s = True
            self.__rollTimer = dt.now()
            self.__rollCount += 1
            if self.__rollCount >= len(rolling):
                self.__rollCount = 0
        
        perc = self.__count / self.__total * 100.
        self.increment()
        
        if not p2s and perc < 100.: return
        
        for i in range(10):
            if perc >= i*10:
                j = i
        
        if perc < 100.:
            bar = u'\u039e'*j + rolling[self.__rollCount] + '-'*(9-j)
            if perc <= 0.:
                etr = 'ETR -:--:--.------'
            else:
                time = (dt.now() - self.__timer).total_seconds()
                etr = 'ETR {}'.format(td(seconds=time / perc * 100. - time))
        else:
            bar = u'\u039e'*10
            etr = 'Run time {}'.format(dt.now()-self.__timer)
        bar += ' '*4 + '{:7.3f}%'.format(perc)
        
        if p2s or perc >= 100.:
            n = 4
            if self.__kw['title'] != None: n += 1
            if self.__kw['border']: n += 2
            deleteLastLines(n=n+len(self.msg))
            text(*self.msg, bar, etr, **self.__kw)
        
        
        
        
        
        
        
        
        
        # self.__t.length()
        # sec = self.__t.timeLength.getTotalSeconds()
        
        
        
        # p2s = False
        
        # if sec <= 0.2:
            # r = 0
            # if self.__delta == 0.:
                # p2s = True
                # self.__delta = 0.2
        # elif sec <= 0.4:
            # r = 1
            # if self.__delta == 0.2:
                # p2s = True
                # self.__delta = 0.4
        # elif sec <= 0.6:
            # r = 2
            # if self.__delta == 0.4:
                # p2s = True
                # self.__delta = 0.6
        # elif sec <= 0.8:
            # r = 3
            # if self.__delta == 0.6:
                # p2s = True
                # self.__delta = 0.8
        # else:
            # r = 0
            # p2s = True
            # self.__delta = 0.
            # self.__t = zt()
        
        # base = u'\u039e'*j + rolling[r] + '-'*(9-j) + ' '
        # if self.__perc >= 100.:
            # base = u'\u039e'*10 + ' '
            # #print('\b'*(10+11+17) + ' '*10 + base + s, **edits)
            # #print()
            # n = 4
            # if self.__kw['title'] != None: n += 1
            # if self.__kw['border']: n += 2
            # deleteLastLines(n=n+len(self.msg))
            # text(*self.msg, base+s, 'Ran for {}'.format(str(self.__timer)[12:]), **self.__kw)
        # elif p2s:
            
            # if self.__perc > 0.:
                # self.__timer.length()
                # SEC = self.__timer.timeLength.getTotalSeconds()
                # SEC = SEC / self.__perc * 100. - SEC
                # HRS = SEC // 3660.
                # SEC -= HRS * 3660.
                # MIN = SEC // 60.
                # SEC -= MIN * 60.
                # etr = 'Estimated Time Remaining is {:0>2.0f}:{:0>2.0f}:{:0>9.6f}'.format(HRS, MIN, SEC)
            # else:
                # etr = 'Estimated Time Remaining is --:--:--.------'
            
            # n = 4
            # if self.__kw['title'] != None: n += 1
            # if self.__kw['border']: n += 2
            # deleteLastLines(n=n+len(self.msg))
            # text(*self.msg, base+s, etr, **self.__kw)

from datetime import datetime as dt
from datetime import timedelta as td


class oneLineProgress():
    
    def __init__(self, Total, msg='', showETR=True):
        self.total = Total
        self.msg = msg
        self.count = 0
        self.showETR = showETR
        self.start = dt.now()
        self.rollTimer = dt.now()
        self.rollCount = -1
        self.rollDelta = 0.2
        self.display()
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1
    
    def __str__(self):
        pass
    
    def __len__(self):
        l = len(str(self))
        self.decrement()
        return l
    
    def Set(self, count):
        self.count = count
    
    def setMessage(self, msg):
        self.msg = msg
    
    def display(self):
        rolling = '-\\|/'
        rollDelta = (dt.now()-self.rollTimer).total_seconds()
        
        p2s = False
        if rollDelta >= self.rollDelta or self.rollCount == -1:
            p2s = True
            self.rollTimer = dt.now()
            self.rollCount += 1
            if self.rollCount >= len(rolling):
                self.rollCount = 0
        
        perc = self.count / self.total * 100.
        self.increment()
        
        if not p2s and perc < 100.: return
        
        
        s = '\r' + ' '*(len(self.msg)+50) + '\r'
        # s += colorText(self.msg, colorFG='blue') + ' '*4
        s += self.msg + ' '*4
        
        # j = 0
        for i in range(10):
            if perc >= i*10:
                j = i
        
        if perc < 100.:
            # s += colorText(u'\u039e'*j + rolling[self.rollCount] + '-'*(9-j), colorFG='green', bold=True)
            s += u'\u039e'*j + rolling[self.rollCount] + '-'*(9-j)
        else:
            # s += colorText(u'\u039e'*10, colorFG='green', bold=True)
            s += u'\u039e'*10
        
        # for i in range(1,11):
            # if i*10 <= perc:
                # s += u'\u039e'
            # else:
                # s += '-'
        s += ' '*4 + '{:7.3f}%'.format(perc)
        if not self.showETR:
            if perc >= 100.: s += '\n'
            print(s, end='')
            return
        
        if perc <= 0:
            etr = '-:--:--.------'
            s += ' '*4 + 'ETR = {}'.format(etr)
        elif perc >= 100.:
            s += ' '*4 + 'Run Time {}'.format(dt.now()-self.start) + '\n'
        else:
            time = (dt.now()-self.start).total_seconds()
            etr = td(seconds=time / perc * 100. - time)
            s += ' '*4 + 'ETR = {}'.format(etr)
        print(s, end='')
        return

class Progress():
    
    def __init__(self, Total, title=None, border=True, msg=[]):
        self.total = Total
        self.__kw = {'title':title, 'border':border}
        if type(msg) != list: msg = [msg]
        self.msg = msg
        self.count = 0
        self.start = dt.now()
        self.rollTimer = dt.now()
        self.rollCount = -1
        self.rollDelta = 0.2
        self.display()
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1
    
    def __str__(self):
        pass
    
    def __len__(self):
        l = len(str(self))
        self.decrement()
        return l
    
    def Set(self, count):
        self.count = count
    
    def display(self):
        rolling = '-\\|/'
        rollDelta = (dt.now()-self.rollTimer).total_seconds()
        
        p2s = False
        if rollDelta >= self.rollDelta or self.rollCount == -1:
            p2s = True
            self.rollTimer = dt.now()
            self.rollCount += 1
            if self.rollCount >= len(rolling):
                self.rollCount = 0
        
        perc = self.count / self.total * 100.
        self.increment()
        
        if not p2s and perc < 100.: return
        
        for i in range(10):
            if perc >= i*10:
                j = i
        
        if perc < 100.:
            s = u'\u039e'*j + rolling[self.rollCount] + '-'*(9-j)
        else:
            s = u'\u039e'*10
        s += ' '*4 + '{:7.3f}%'.format(perc)
        
        if perc <= 0:
            etr = 'ETR is -:--:--.------'
        elif perc >= 100.:
            etr = 'Run Time is {}'.format(dt.now()-self.start)
        else:
            time = (dt.now()-self.start).total_seconds()
            etr = 'ETR is {}'.format(td(seconds=time / perc * 100. - time))
        
        n = 4
        if self.__kw['title'] != None: n += 1
        if self.__kw['border']: n += 2
        deleteLastLines(n=n+len(self.msg))
        text(*self.msg, s, etr, **self.__kw)
        return



def mySplit(S,sep='- :.'):
    o = []
    c = ''
    for s in S:
        if s in sep:
            if c != '': o.append(c)
            c = ''
        else:
            c += s
    if c != '': o.append(c)
    return o


def appendToFile(*vals):
    f = open(vals[0], 'a')
    f.write( csvLineWrite(*vals[1:]) )
    f.close()


from tempfile import TemporaryFile as tf

class zemptyFile():
    
    
    def __init__(self):
        self.__f = tf(mode='w+')
    
    def zwrite(self, *x):
        self.__f.write( csvLineWrite(*x) )
    
    # def readline(self, **kw):
        # s = self.__s.splitlines()
        # vals = csvLineRead(s[self.__i], **kw)
        # self.__i += 1
        # return vals
    
    # def seek(self, i):
        # self.__i = i
    
    # def getIndex(self):
        # return self.__i
    
    # def getValues(self, **kw):
        # s = self.__s.splitlines()
        # col = len(s[0].split(','))
        # data = zList(len(s), col)
        # for i in range(len(s)):
            # data[i,:] = csvLineRead(s[i], **kw)
        # return data
    
    def getValues(self, **kw):
        self.__f.seek(0)
        raw = self.__f.readlines()
        self.__f.close()
        col = len(raw[0].split(','))
        data = zList(len(raw), col)
        for i,line in enumerate(raw):
            data[i,:] = csvLineRead(line, **kw)
        return data


def colorText(s, colorFG=None, colorBG=None, brightFG=False, brightBG=False, underline=False, bold=False, faint=False, crossedOut=False, concealed=False, p2s=False):
    colors = [  'black',
                'red',
                'green',
                'yellow',
                'blue',
                'magenta',
                'cyan',
                'white']
    brightness = {'normal': 30, 'bright': 90}
    which = {'fore': 0, 'back': 10}
    
    end = '\033[0m'
    code = ''
    if colorFG != None:
        if colorFG.lower() not in colors: raise ValueError('FG color {} not accepted'.format(colorFG.lower))
        
        if len(code) != 0: code += ';'
        n  = colors.index(colorFG.lower())
        if brightFG:
            n += brightness['bright']
        else:
            n += brightness['normal']
        n += which['fore']
        code += str(n)
    
    if colorBG != None:
        if colorBG.lower() not in colors: raise ValueError('BG color {} not accepted'.format(colorBG.lower))
        
        if len(code) != 0: code += ';'
        n  = colors.index(colorBG.lower())
        if not brightBG:
            n += brightness['normal']
        else:
            n += brightness['bright']
        n += which['back']
        code += str(n)
    
    if underline:
        if len(code) != 0: code += ';'
        code += '4'
    
    if bold:
        if len(code) != 0: code += ';'
        code += '1'
    
    if faint:
        if len(code) != 0: code += ';'
        code += '2'
    
    if crossedOut:
        if len(code) != 0: code += ';'
        code += '9'
    
    if concealed:
        if len(code) != 0: code += ';'
        code += '8'
    
    if len(code) == 0:
        if p2s:
            print(s)
            return
        else:
            return s
    else:
        base = '\033[{}m'.format(code)
        if p2s:
            print(base+s+end)
            return
        else:
            return base+s+end


def textAlternate(*word, c=77, border=True, title=None, p2s=True, **kw):
    if len(word) == 1: word = word[0]
    s = '\n'
    if type(word) == list or type(word) == tuple:
        k = 0
        for w in word:
            if len(w) > c: c = len(w)
        if title != None: s += oneLineText(title, c=c, p=0, border=False, p2s=False) + '\n'
        if border: s += '='*c+'\n'
        for w in word:
            l = int((c-len(w))/2)
            s += '{}{}'.format(l*' ',w) + '\n'
        if border: s += '='*c+'\n'
    else:
        if len(word) > c: c = len(word)
        if title != None: s += oneLineText(title, c=c, p=0, border=False, p2s=False) + '\n'
        if border: s += '='*c+'\n'
        l = int((c - len(word)) / 2)
        s += '{}{}'.format(l*' ',word) + '\n'
        if border: s += '='*c+'\n'
    s += '\n'
    s = strFancyFormat(s, p2s=False, **kw)
    
    if p2s: print(s, end='')
    return s

