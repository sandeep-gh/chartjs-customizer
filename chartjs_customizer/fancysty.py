from tailwind_tags import *
from addict import Dict

analysisPanel = [bg/gray/2]
tlc = [container, mr/x/auto, bg/gray/3, space/y/1]

rootde = [container, mr/x/auto, bg/gray/2, space/y/1]
grid = [col/span/6, row/span/1, bg/gray/2, fc/gray/6, shdw.md]
infocard = [bg/gray/2, fc/gray/6]
border_style = [bt.bd, bdr.md,  bd/gray/4]
panel = [*border_style]

_ = cfgpanels = Dict()

_.cfgpanel = [col/span/6, row/span/1, bg/gray/2, fc/gray/6, shdw.md]
_.options = [row/span/2, col/span/2, bg/gray/2, fc/gray/6, mr/1, *border_style]
_.options_child = [row/span/1, col/span/2, mr/1,
                   bg/gray/2, fc/gray/6, shdw.md, *border_style]