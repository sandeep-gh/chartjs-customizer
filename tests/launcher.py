#from chartjs_customizer.getChartdata_sbs_wp import launcher
#from chartjs_customizer.getChartdata_wp_bits_and_pieces import launcher
#from chartjs_customizer.dashboard_v2 import launcher
#from chartjs_customizer.just_chartjs_plt import launcher
#from chartjs_customizer.configchart_wp_bits_and_pieces import launcher, page_ready
#from chartjs_customizer.chartjs_customizer import launcher
import logging
import os
if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    logging.basicConfig(filename="launcher.log", level=logging.INFO)


from chartjs_customizer.wp_initialSetup import wp_initialSetup
from chartjs_customizer.wp_chartjs_customizer import wp_chartjs_customizer
if os:
    from tracker import _hcs, refBoard

import justpy as jp
from addict import Dict

#wp = launcher(None)
# wp = wp_initialSetup(None)
# _hcs['/type'].target.selector.value = 'line'  # mimic key press

# _hcs['/options/parsing/value'].target.value = True

# #print("_hcs == ", _hcs['/type'].target.selector.value)
# logging.debug("respond to uic change in value")
# wp.update_ui_component(_hcs['/type'].target, None)
#print("refBoard = ", refBoard)

# wp.update_ui_component()
# page_ready(wp, None)
app = jp.app
#jp.justpy(wp_initialSetup, start_server=False)
jp.justpy(wp_chartjs_customizer, host="192.168.0.183", start_server=False)

#wp = wp_chartjs_customizer(None)
# _hcs['/type'].target.selector.value = 'line'  # mimic key press

# dbref = _hcs.optionsCtx['/options/scales/xAxis/grid/display'].target
# dbref.value = True
# msg = Dict()
# msg.value = True

# wp.update_ui_component(dbref, msg)
