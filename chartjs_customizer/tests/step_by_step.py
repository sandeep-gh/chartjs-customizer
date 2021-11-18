import sys
import importlib
from addict import Dict
from chartjs_customizer import chart_ui_cfg as ccfg

from chartjs_customizer.dashboard_step_by_step import launcher
from chartjs_customizer import dashboard_step_by_step as dashboard
from dpath.util import get as dget, set as dset,  new as dnew

from chartjs_customizer import getChartdata_sbs_wp as getChartdata_wp
importlib.reload(ccfg)
importlib.reload(getChartdata_wp)
importlib.reload(wf)
cfgAttrMeta = ccfg.get_baseCfgAttrMeta()
cjs_cfg = Dict(track_changes=True)
ui_cfg = Dict(track_changes=True)
ccfg.update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
dset(cjs_cfg, "/type", "line")
ccfg.add_dataset(cjs_cfg)


plt_cfg = ccfg.build_plt_cfg(cjs_cfg)
wp = getChartdata_wp.launcher(None)

importlib.reload(dashboard)
dashboard.launcher(None)


cfgAttrMeta = get_baseCfgAttrMeta()
attrupdate(cfgAttrMeta, "/type",  True)
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
