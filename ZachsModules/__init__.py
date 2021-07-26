# Set environment variables to tell numpy to not use multithreading
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

from . import numericalMethods as nm
from . import aerodynamics as aero
from . import io
from . import misc
from . import zPlotter as zp
from .zPlotter import plt

__all__ = ['nm', 'aero', 'io', 'misc', 'zp', 'plt']
