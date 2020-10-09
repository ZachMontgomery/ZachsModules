from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator
from matplotlib import rcParams
import matplotlib.pyplot as plt

defaultLW = 0.5
defaultColor = '0.75'
defaultDashedLS = (0, (3, 3))

def createBasePlot(**kw):
    ## extract input data
    fs = kw.get('figsize', None)
    sp = kw.get('subplot', 111)
    
    if fs != None:
        fig = plt.figure(figsize=fs)
    else:
        fig = plt.figure()
    ax = fig.add_subplot(sp)
    return fig, ax

def updateRCParams(paperPublication=False, useZachsDefaults=True, **kw):
    
    ## default settings
    if useZachsDefaults:
        ## set default font to Times New Roman
        rcParams['text.usetex'] = True
        rcParams['font.family'] = 'serif'
        rcParams['font.serif'] = ['Times New Roman', 'Times']
        ## set default save fig setting for transparent background
        rcParams['savefig.transparent'] = True
        ## set default math test. I pulled these from Jeff's contour code. This may or may not be needed.
        rcParams['mathtext.rm'] = 'serif'
        rcParams['mathtext.it'] = 'serif:italic'
        rcParams['mathtext.bf'] = 'serif:bold'
        # rcParams['mathtext.fontset'] = 'custom'
        ## set default line settings
        rcParams['lines.linewidth'] = 0.5
        # rcParams['lines.scale_dashes'] = False
        rcParams['lines.dashed_pattern'] = [3., 3.]
        ## set axes defaults
        rcParams['axes.grid'] = True
        rcParams['axes.linewidth'] = 0.75
        ## set grid defaults
        rcParams['grid.color'] = '0.75'
        rcParams['grid.linewidth'] = 0.5
        rcParams['grid.linestyle'] = '--'
        ## set marker defaults
        rcParams['markers.fillstyle'] = 'none'
        ## set tick defaults
        rcParams['xtick.direction'] = 'in'
        rcParams['xtick.major.pad'] = 7.25
        # rcParams['xtick.major.top'] = True
        rcParams['xtick.major.width'] = 0.75
        rcParams['xtick.major.size'] = 3.0
        rcParams['xtick.minor.pad'] = 7.25
        # rcParams['xtick.minor.top'] = True
        rcParams['xtick.minor.width'] = 0.25
        rcParams['xtick.minor.size'] = 1.75
        rcParams['xtick.minor.visible'] = True
        rcParams['xtick.top'] = True
        
        rcParams['ytick.direction'] = 'in'
        rcParams['ytick.major.pad'] = 7.25
        # rcParams['ytick.major.right'] = True
        rcParams['ytick.major.width'] = 0.75
        rcParams['ytick.major.size'] = 3.0
        rcParams['ytick.minor.pad'] = 7.25
        # rcParams['ytick.minor.right'] = True
        rcParams['ytick.minor.width'] = 0.25
        rcParams['ytick.minor.size'] = 1.75
        rcParams['ytick.minor.visible'] = True
        rcParams['ytick.right'] = True
    
    if paperPublication:
        rcParams['font.size'] = 7.1
        rcParams['figure.figsize'] = [3.25, 2.5]
        rcParams['xtick.labelsize'] = 7.1
        rcParams['ytick.labelsize'] = 7.1
        
    
    ## additional settings (these can override the default settings)
    for k,v in kw.items():
        rcParams[k] = v


def formatAxis(ax, **kw):
    '''
    Formats the inputted axis with the following optional keyword inputs:
        
        gridPresent: boolean, (False) Determine whether to add and format a grid for
            the axis
        gridWhich: 'major'
        gridColor
        gridLS
        gridLW
        gridAlpha
        
        xTickDensity
        yTickDensity
        xTickLabelDensity
        yTickLabelDensity
        xTickLabelFormat
        yTickLabelFormat
        
        minorTicks
        xMinorTickDensity
        yMinorTickDensity
        minorTickStep
        tickParams
        
        xTitle
        yTitle
        
        axis
        
        spines.linewidth
    '''
    
    ## set border
    ########################################################################
    if 'spines.linewidth' in kw:
        temp = kw['spines.linewidth']
        ax.spines['top'].set_linewidth(temp)
        ax.spines['bottom'].set_linewidth(temp)
        ax.spines['left'].set_linewidth(temp)
        ax.spines['right'].set_linewidth(temp)
    
    ## axis Range
    ########################################################################
    if 'axis' in kw:
        ax.axis( kw['axis'] )
    
    ## format grid
    ########################################################################
    if kw.get('gridPresent', False):
        ax.grid(which     = kw.get('gridWhich', 'major'),
                color     = kw.get('gridColor', defaultColor),
                linestyle = kw.get('gridLS'   , defaultDashedLS),
                linewidth = kw.get('gridLW'   , lw),
                alpha     = kw.get('gridAlpha', 1.0))
    
    ## format ticks
    ########################################################################
    ## set tick densities
    if 'xTickDensity' in kw:
        ax.set_xticks(kw['xTickDensity'])
    if 'yTickDensity' in kw:
        ax.set_yticks(kw['yTickDensity'])
    if 'xTickLabelDensity' in kw:
        ax.xaxis.set_ticklabels(kw['xTickLabelDensity'])
    if 'yTickLabelDensity' in kw:
        ax.yaxis.set_ticklabels(kw['yTickLabelDensity'])
    ## toggle minor ticks
    if kw.get('minorTicks', False):
        ax.minorticks_on()
    
    # if 'xTickDensity' in kw:
        # mt = [kw['xTickDensity'][0]]
        # xMinorTickDensity = kw.get('xMinorTickDensity', 4)
        # for i in range(len(kw['xTickDensity'])-1):
            # val1, val2 = kw['xTickDensity'][i], kw['xTickDensity'][i+1]
            # step = (val2-val1)/xMinorTickDensity
            # for j in range(1,1+xMinorTickDensity):
                # mt.append(val1+j*step)
        # ax.set_xticks(mt, minor=True)
    # if 'yTickDensity' in kw:
        # mt = [kw['yTickDensity'][0]]
        # yMinorTickDensity = kw.get('yMinorTickDensity', 4)
        # for i in range(len(kw['yTickDensity'])-1):
            # val1, val2 = kw['yTickDensity'][i], kw['yTickDensity'][i+1]
            # step = (val2-val1)/yMinorTickDensity
            # for j in range(1,1+yMinorTickDensity):
                # mt.append(val1+j*step)
        # ax.set_yticks(mt, minor=True)
    
    if 'minorTickStep' in kw:
        # X, Y = ax.get_xticks(), ax.get_yticks()
        # xStep, yStep = abs(X[0] - X[1])/kw['minorTickStep'], abs(Y[0]-Y[1])/kw['minorTickStep']
        # xLim, yLim = ax.get_xlim(), ax.get_ylim()
        # xN = int((max(X)-min(X)+2.*xStep*kw['minorTickStep'])/xStep)+1
        # yN = int((max(Y)-min(Y)+2.*yStep*kw['minorTickStep'])/yStep)+1
        
        # x = []
        # for i in range(xN):
            # val = min(X)-xStep + i*xStep
            # if val not in X and val >= min(xLim) and val <= max(xLim):
                # x.append(val)
        # y = []
        # for i in range(yN):
            # val = min(Y)-yStep + i*yStep
            # if val not in Y and val >= min(yLim) and val <= max(yLim):
                # y.append(val)
        
        # ax.set_xticks(x, minor=True)
        # ax.set_yticks(y, minor=True)
        minorTickStep(ax, kw['minorTickStep'])
    
    
    
    # if 'minorTickStep' in kw:
        # ax.xaxis.set_minor_locator(AutoMinorLocator(n=kw['minorTickStep']))
        # ax.yaxis.set_minor_locator(AutoMinorLocator(n=kw['minorTickStep']))
    
    
    
    
    ## set tick parameters (formatting)
    tickParams = kw.get('tickParams', {
        'major': {
            'which': 'major',
            'labelsize': 7.1,
            'direction': 'in',
            'width': 0.75,
            'length': 3.0,
            'top': True,
            'right': True,
            'pad': 7.25
        },
        'minor': {
            'which': 'minor',
            'labelsize': 7.1,
            'direction': 'in',
            'width': 0.25,
            'length': 1.75,
            'top': True,
            'right': True,
            'pad': 7.25
        }
    })
    ax.tick_params(**tickParams['major'])
    ax.tick_params(**tickParams['minor'])
    ## set tick label formats
    if 'xTickLabelFormat' in kw:
        ax.xaxis.set_major_formatter(FormatStrFormatter(kw['xTickLabelFormat']))
    if 'yTickLabelFormat' in kw:
        ax.yaxis.set_major_formatter(FormatStrFormatter(kw['yTickLabelFormat']))
    # ax.xaxis.set_major_formatter(FormatStrFormatter(kw.get('xTickLabelFormat', '%.1f')))
    # ax.yaxis.set_major_formatter(FormatStrFormatter(kw.get('yTickLabelFormat', '%.1f')))
    
    ## axis titles
    ########################################################################
    if 'xTitle' in kw:
        ax.set_xlabel(kw['xTitle'])
    if 'yTitle' in kw:
        ax.set_ylabel(kw['yTitle'])

def saveFigEMF(fig, filename, **kw):
    
    if filename[-4:] == '.svg':
        fig.savefig(filename, format='svg', **kw)
    else:
        fig.savefig(filename+'.svg', format='svg', **kw)
    
    import os
    
    os.system('inkscape {}.svg --export-emf={}.emf'.format(filename, filename))


def minorTickStep(ax, n):
    X, Y = ax.get_xticks(), ax.get_yticks()
    xStep, yStep = abs(X[0] - X[1])/n, abs(Y[0]-Y[1])/n
    xLim, yLim = ax.get_xlim(), ax.get_ylim()
    xN = int((max(X)-min(X)+2.*xStep*n)/xStep)+1
    yN = int((max(Y)-min(Y)+2.*yStep*n)/yStep)+1
    
    x = []
    for i in range(xN):
        val = min(X)-xStep + i*xStep
        if val not in X and val >= min(xLim) and val <= max(xLim):
            x.append(val)
    y = []
    for i in range(yN):
        val = min(Y)-yStep + i*yStep
        if val not in Y and val >= min(yLim) and val <= max(yLim):
            y.append(val)
    
    ax.set_xticks(x, minor=True)
    ax.set_yticks(y, minor=True)
