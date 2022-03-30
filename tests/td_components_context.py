"""
be clear about what components are being generated be under what context

"""

import logging
import os
if os:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)


from dpath.util import (get as dget, new as dnew, search as dsearch,
                        set as dset)
from chartjs_customizer.attrmeta_basecfg_orig import get_basecfg
from chartjs_customizer.attrmeta_basecfg_helper import PlotType, uiorgCat
from addict import Dict
from chartjs_customizer.chartjs_customizer_components import build_uigroup_panel_
from chartjs_customizer.chartcfg import (add_dataset, build_pltcfg, update_cfgattrmeta,
                                         update_chartCfg)
import jsbeautifier
import json

from chartjs_customizer.dpathutils import walker
choices = Dict()
choices.plottype = PlotType.Line
choices.line.xscale = 'x'
choices = Dict()
choices.plottype = PlotType.Line

# default for line
choices.scales.xaxes = 'x'
choices.scales.yaxes = 'y'
choices.scales.xaxes = [
    {'id': 'x1', 'type': 'time', 'title': {'text': 'Data'}}]

cfgAttrMeta = get_basecfg(choices)

print("walking --------------------")
for pp in walker(cfgAttrMeta):
    print(pp)
# cjs_cfg = Dict(track_changes=True)
# update_chartCfg(cfgAttrMeta, cjs_cfg)
# opts = jsbeautifier.default_options()
# print(jsbeautifier.beautify(json.dumps(cjs_cfg), opts))

# cfgAttrMeta.clear_changed_history()
# add_dataset(cjs_cfg)
# dnew(cjs_cfg, "/data/labels", "[1,2,4,5]")
# update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
# update_chartCfg(cfgAttrMeta, cjs_cfg)
# cfgAttrMeta.clear_changed_history()
# cjs_cfg.clear_changed_history()

# # cycle through
# panel_ = build_uigroup_panel_(uiorgCat.all, cjs_cfg, cfgAttrMeta)
# print(panel_)
