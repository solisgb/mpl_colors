# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 13:56:17 2023

@author: solis
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 11:55:25 2023

@author: solis

fork of WQChartPy https://github.com/jyangfsu/WQChartPy
"""

try:
    # import numpy as np
    from time import time
    import traceback
    
    from mpl_colors import MplColors as mc
    import littleLogging as myLogging

except ImportError as e:
    print( getattr(e, 'message', repr(e)))
    raise SystemExit(0)
    

if __name__ == "__main__":

    startTime = time()

    try:

        mc.display_colormaps(['tab10'])
    
    except ValueError:
        msg = traceback.format_exc()
        myLogging.append(msg)
    except Exception:
        msg = traceback.format_exc()
        myLogging.append(msg)
    finally:
        myLogging.dump()
        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')

