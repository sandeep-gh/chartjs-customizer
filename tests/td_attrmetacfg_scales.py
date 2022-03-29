import logging
import os
if os:
    try:
        os.remove("launcher.log")
    except:
        pass
    logging.basicConfig(filename="launcher.log", level=logging.INFO)
    logger = logging.getLogger(__name__)

import traceback
import logging
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


import justpy as jp

import webapp_framework as wf
#from .attrmeta import get_basecfg, uiorgCat
#from .attrmeta_basecfg_helper import uiorgCat, PlotType
from chartjs_customizer.attrmeta_basecfg_orig import get_basecfg
import jsbeautifier
choices = Dict()
choices.plottype = PlotType.Line

# default for line
choices.scales.xaxes = 'x'
choices.scales.yaxes = 'y'

# multiple xaxes
choices.line.scales.xaxes = [
    {'id': x, 'type': 'time', 'title': {'text': 'Data'}}]
cfgAttrMeta = get_basecfg(choices)

cjs_cfg = Dict(track_changes=True)
update_chartCfg(cfgAttrMeta, cjs_cfg)
cfgAttrMeta.clear_changed_history()
add_dataset(cjs_cfg)
dnew(cjs_cfg, "/data/labels", "[1,2,4,5]")
dset(cjs_cfg, "/type", "line")
update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
update_chartCfg(cfgAttrMeta, cjs_cfg)
cfgAttrMeta.clear_changed_history()
cjs_cfg.clear_changed_history()

print(cjs_cfg)
