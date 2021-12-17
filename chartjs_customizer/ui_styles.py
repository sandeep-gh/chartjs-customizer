import os
from . import snowsty as snow
from . import fancysty as fancy
styles = {'snow': snow, 'fancy': fancy
          }


sty = styles['snow']

if 'WFSTY' in os.environ:
    sty = styles[os.environ['WFSTY']]
