"""Ask user for chart data and initial chart configuration
"""
import os
import logging
if logging:  # pin code here so that ide doesn't move around the import statements
    try:
        os.remove("chartjs_customizer.log")
    except:
        pass
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(filename="chartjs_customizer.log", level=logging.DEBUG)
import traceback
from addict import Dict
from dpath.util import get as dget, set as dset,  new as dnew
import justpy as jp
#from .components_initialSetup import cfgAttrMeta, cfgattr_groupInitial
from .components_scales import cfgAttrMeta, cfgattr_groupInitial

if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict, refBoard

import webapp_framework as wf
import webapp_framework_extn as wfx
from .chartcfg import (add_dataset, build_pltcfg, update_cfgattrmeta,
                       update_chartCfg)
from .attrmeta import uiorgCat


def on_page_ready(self, msg):
    logger.debug("calling refresh on page_ready")
    wfx.refresh(refBoard)


@jp.SetRoute('/initialSetup')
def wp_tryoutScales(request):
    wp = wf.WebPage_("wp_index",
                     page_type='quasar'
                     )()
    stubStore.topPanel(wp, "")  # render all of the ui components

    cjs_cfg = Dict(track_changes=True)
    update_chartCfg(cfgAttrMeta, cjs_cfg)
    # ignore cjs_cfg changes coming from previous statement
    cjs_cfg.clear_changed_history()
    cfgAttrMeta.clear_changed_history()
    for kpath in cfgAttrMeta.get_changed_history():
        print("post clean ", kpath)
    wfx.refresh(refBoard)

    def update_ui_component(dbref, msg):
        pass
    wp.update_ui_component = update_ui_component
    wp.on("page_ready", on_page_ready)
    return wp
