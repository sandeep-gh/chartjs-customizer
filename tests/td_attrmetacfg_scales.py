from chartjs_customizer.cfgattr_uic import build_uic_iter
from chartjs_customizer.attrmeta_basecfg_helper import uiorgCat
import chartjs_customizer.attrmeta
import logging
import os


if os:
    try:
        os.remove("launcher.log")
    except:
        pass
    logging.basicConfig(filename="launcher.log", level=logging.DEBUG)
    #logger = logging.getLogger(__name__)

import traceback

import os
import re

import dill as pickle
from addict import Dict
from chartjs_customizer.attrmeta_basecfg_helper import PlotType
from dpath.util import get as dget, set as dset,  new as dnew, search as dsearch
from chartjs_customizer.chartcfg import (add_dataset, update_cfgattrmeta,
                                         update_chartCfg)
if os:
    from tracker import _hcs, refBoard

from chartjs_customizer.chartcfg import (add_dataset, build_pltcfg, update_cfgattrmeta,
                                         update_chartCfg)


import justpy as jp

import webapp_framework as wf
from chartjs_customizer.cfgattrmeta_datasets import add_datacfg
#from .attrmeta import get_basecfg, uiorgCat
#from .attrmeta_basecfg_helper import uiorgCat, PlotType
from chartjs_customizer.attrmeta_basecfg_orig import get_basecfg
import jsbeautifier
from chartjs_customizer.dpathutils import walker
choices = Dict()
choices.plottype = PlotType.Line

# default for line
choices.scales.xaxes = 'x'
choices.scales.yaxes = 'y'

# multiple xaxes
choices.line.scales.xaxes = [
    {'id': 'x', 'type': 'time', 'title': {'text': 'Data'}}]
cfgAttrMeta = get_basecfg(choices)

cjs_cfg = Dict(track_changes=True)
update_chartCfg(cfgAttrMeta, cjs_cfg)
cfgAttrMeta.clear_changed_history()
dnew(cjs_cfg, "/data/labels", "[1,2,4,5]")
dset(cjs_cfg, "/type", "line")
update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
cfgAttrMeta.clear_changed_history()
# add data after update_cfgattrmeta for now
add_dataset(cjs_cfg)
add_datacfg(cfgAttrMeta, cjs_cfg.data.datasets)

print("post adding datasets")
# for _ in cfgAttrMeta.get_changed_history():
#     print("post data: get change history", _, dget(cfgAttrMeta, _))
#update_chartCfg(cfgAttrMeta, cjs_cfg)
cfgAttrMeta.clear_changed_history()
cjs_cfg.clear_changed_history()


print(cjs_cfg)
# print("post adding datasets")
# for _ in cfgAttrMeta.get_changed_history():
#     print("post data: get change history", _, dget(cfgAttrMeta, _))


#pltcfg = build_pltcfg(cjs_cfg)
# print(pltcfg)


def is_visible(attrmeta):
    if attrmeta.vtype != None:
        if attrmeta.group != uiorgCat.TBD:
            return True
    return False


# for _ in walker(cfgAttrMeta.data):
#     print(_)
cfgiter_for_ui = filter(lambda _: is_visible(_[1]), walker(cfgAttrMeta.data))

for _ in build_uic_iter(cfgiter_for_ui):
    print(_)
