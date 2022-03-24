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
from webapp_framework_tracking.dbrefBoard import refresh as dbrefBoard_refresh
from .chartcfg import (add_dataset, build_pltcfg, update_cfgattrmeta,
                       update_chartCfg)
from .attrmeta import uiorgCat

from . import components_scales


def on_page_ready(self, msg):
    logger.debug("calling refresh on page_ready")
    dbrefBoard_refresh(refBoard)


@jp.SetRoute('/initialSetup')
def wp_tryoutScales(request):
    wp = wf.WebPage_("wp_index",
                     page_type='quasar', cgens=[stubStore.topPanel,
                                                stubStore._scales._plottype.deck,
                                                stubStore._scales._lineplot.panel,
                                                stubStore._scales.scalesNoticeboard]
                     )()

    cjs_cfg = Dict(track_changes=True)
    update_chartCfg(cfgAttrMeta, cjs_cfg)
    # ignore cjs_cfg changes coming from previous statement
    cjs_cfg.clear_changed_history()
    cfgAttrMeta.clear_changed_history()
    for kpath in cfgAttrMeta.get_changed_history():
        print("post clean ", kpath)
    dbrefBoard_refresh(refBoard)

    def react_ui(tag, arg):
        pass
    wp.react_ui = react_ui

    def update_ui_component(dbref, msg):
        dbrefBoard_refresh(refBoard)

        pass
    wp.update_ui_component = update_ui_component

    def update_scale_configurator(dbref, msg):
        dbrefBoard_refresh(refBoard)
        # for now scale configuration is only dependent on plottype
        print(refBoard)
        print("deck ", stubStore.scalesCtx.deck)
        print("plot type select",  dget(refBoard, "/type"))
        choosen_plottype = dget(refBoard, "/type").val
        match choosen_plottype:
            case 'None':
                print("plottype selected None")
                stubStore.scalesCtx.deck.target.bring_to_front(
                    stubStore.scalesCtx.noselection.spath)
            case 'line':
                line = 'line'
                print("spath = ", stubStore.scalesCtx.line.spath)
                stubStore.scalesCtx.deck.target.bring_to_front(
                    stubStore.scalesCtx.line.spath)
            case 'bar':
                # bar stuff
                stubStore.scalesCtx.deck.target.bring_to_front(
                    stubStore.scalesCtx.bar.spath)
                pass
            case 'scatter':
                # scatter stuff
                pass
            case 'polararea':
                # polaar stuff
                pass

        pass

    wp.update_scale_configurator = update_scale_configurator
    wp.on("page_ready", on_page_ready)
    return wp
