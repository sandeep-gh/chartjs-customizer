import sys
import importlib
from addict import Dict
from chartjs_customizer.chart_ui_cfg import *

from chartjs_customizer.dashboard_step_by_step import launcher
from chartjs_customizer import dashboard_step_by_step as dashboard


from chartjs_customizer import getChartdata_sbs_wp as getChartdata_wp
importlib.reload(getChartdata_wp)
wp = getChartdata_wp.launcher(None)

importlib.reload(dashboard)
dashboard.launcher(None)

cjs_cfg = Dict(track_changes=True)
ui_cfg = Dict(track_changes=True)
cfgAttrMeta = get_baseCfgAttrMeta()
update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
# ui will change cjs_cfg here: hidden will become unhidden
cjs_cfg.clear_changed_history()
cjs_cfg.type = PlotType.Line

# update cfgattrmeta --> when value in cjs_cfg  changes
update_cfgattrmeta(cjs_cfg, cfgAttrMeta)

for kpath in cfgAttrMeta.get_changed_history():
    print(kpath, " ", dget(cfgAttrMeta, kpath))

update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)

# The update_cfgattrmeta and update_chartCfg should
# happen in loop until ad-infinitum
for kpath in cjs_cfg.get_changed_history():
    print(kpath, " ", dget(cjs_cfg, kpath))

cjs_cfg.clear_changed_history()

# now go back in revese <--> all grid references should go away
cjs_cfg.type = None
update_cfgattrmeta(cjs_cfg, cfgAttrMeta)

update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)


#from chartjs_customizer.responsive import Color, AttrMeta, CPT, update_cfg_attrMeta


#cfgMeta = Dict(track_changes=True)

# cfgMeta.options.scales.xAxis.grid.display = False
# _ = cfgMeta.options.scales.xAxis

# _.grid.color = AttrMeta("", Color, Color, CPT.simple, True)
# _.grid.borderColor = AttrMeta("", Color, Color, CPT.nitpick, True)
# _.grid.tickColor = AttrMeta("", Color, Color, CPT.simplemore, True)
# _.grid.circular = AttrMeta(
#     None, None, None, CPT.TBD, True)  # from for radar chart

# cfgMeta.clear_changed_history()


# def iter_cfgMeta(cfgMeta, prefix=""):
#     for attr, val in cfgMeta.items():
#         if isinstance(val, Dict):
#             yield from iter_CfgMeta(val, f"{prefix}/{attr}")
#         else:
#             yield (f"{prefix}/{attr}", val)


# def build_chart_ui_cfg(cfgMetaIter):
#     chartcfg = Dict()
#     uicfg = Dict()
#     for kpath, attrMeta in cfgMetaIter:
#         is_disabled, default_val = attrMeta_eval(cfgMetaIter)
#         dset(kpath, uicfg, [is_disabled, default_val])
#         if not is_disabled:
#             dset(kpath, chartcfg, default_val)

#     return [uicfg, chartcfg]


# update_cfg_attrMeta("/options/scales/xAxis/grid/display", True, cfgMeta)

# for kpath in cfgMeta.get_changed_history():
#     print(kpath)
