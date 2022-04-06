#from chartjs_customizer.getChartdata_sbs_wp import launcher
#from chartjs_customizer.getChartdata_wp_bits_and_pieces import launcher
#from chartjs_customizer.dashboard_v2 import launcher
#from chartjs_customizer.just_chartjs_plt import launcher
#from chartjs_customizer.configchart_wp_bits_and_pieces import launcher, page_ready
#from chartjs_customizer.chartjs_customizer import launcher
from tailwind_tags import twcc2hex
import logging
import os
if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)


from chartjs_customizer.wp_initialSetup import wp_initialSetup
from chartjs_customizer.wp_chartjs_customizer import wp_chartjs_customizer

from chartjs_customizer.wp_tryoutScales import wp_tryoutScales
if os:
    from tracker import _hcs, refBoard

import justpy as jp
from addict import Dict


#wp = launcher(None)
# wp = wp_initialSetup(None)


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


# _hcs['/type'].target.selector.value = 'line'  # mimic key press

# dbref = _hcs['/options/scales/x/grid/display'].target
# # print(dbref)
# dbref.value = True
# msg = Dict()
# # msg.value = True
# # logging.debug("-------------- now we begin ----")
# wp.update_ui_component(dbref, msg)


# debuggin gold
#wp = wp_chartjs_customizer(None)
# logging.debug("start tinkering")
# # Turn on x1/display
# x1_display = _hcs['/options/scales/x1/display'].target
# x1_display.value = True
# msg = Dict()
# msg.value = True

# wp.update_ui_component(x1_display, msg)
# x1_bg_color_selector = _hcs['/options/scales/x1/backgroundColor'].target


# print("color options = ", twcc2hex.keys())

# color_selector = x1_bg_color_selector.cs_.target

# mainColorSelector = color_selector.mainColorSelector_.target
# mainColorSelector.setValue("pink")  # pick from palette-v2x.json

# shades = color_selector.shades_.target
# shades.setValue(8)
# print("post setValue ", shades.getValue())
# msg.value = shades.getValue()
# mainColorSelector.on_click(msg)


# x1_grid_display = _hcs['/options/scales/x1/grid/display'].target
# wp.update_ui_component(x1_grid_display, msg)


# logging.debug("-------------------- Turn it off ---------------------")
# msg.value = False
# wp.update_ui_component(x1_display, msg)

# logging.debug("-------------------- back on again ---------------------")
# msg.value = True
# wp.update_ui_component(x1_display, msg)


# # ============================= ends here ============================

# cs = cswb.cs_.target
# shades = cs.shades_.target
# maincolorselector = cs.mainColorSelector_.target
# mv = maincolorselector.value
# sv = shades.values


# # logging.debug("-------------- done ----")


# #wp = wp_tryoutScales(None)
# #jp.justpy(wp_tryoutScales, host="192.168.0.183", start_server=False)
# # _hcs['/type'].target.selector.value = 'line'  # mimic key press
# # wp.update_ui_component()
# #wp.update_scale_configurator(_hcs['/type'].target, None)
