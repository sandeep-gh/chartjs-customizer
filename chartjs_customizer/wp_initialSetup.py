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
#from dpath.util import get as dget, set as dset,  new as dnew
from .dpathutils import dget, dnew, dpop
import justpy as jp
from .components_initialSetup import cfgAttrMeta, cfgattr_groupInitial

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
def wp_initialSetup(request):
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
        """
        update ui on ui state change;
        eventually this should be called update_ui only
        """

        #print("update_ui: refBoard = ", refBoard)
        logger.debug("update_ui..begin")
        wfx.refresh(refBoard)

        # update cjs_cfg with all the updates at the ui
        # will be needed to refresh the chart plot
        for kpath, attrmeta in cfgattr_groupInitial():
            if attrmeta.active:
                logger.debug(
                    f"looking for change: evaluating {kpath} {dget(cjs_cfg, kpath)} {dget(refBoard, kpath).val}")
                if dget(cjs_cfg, kpath) != dget(refBoard, kpath).val:
                    #print(f"update chartcfg {kpath}")

                    wf.dupdate(cjs_cfg, kpath, dget(refBoard, kpath).val)

        # the cjs_cfg changes will open up new ui components
        # just to make sure old stuff are not messing things up
        cfgAttrMeta.clear_changed_history()
        for _ in cfgAttrMeta.get_changed_history():
            print("Should not happen ", _)
        update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
        cjs_cfg.clear_changed_history()
        for kpath in cfgAttrMeta.get_changed_history():
            attrmeta = dget(cfgAttrMeta, kpath)
            if attrmeta.group != uiorgCat.initial:
                continue  # skip cfgattr not in initial group
            dbref = dget(refBoard, kpath)._go.target
            if attrmeta.active and 'hidden' in dbref.classes:
                logger.debug(f"making {dbref.key} visible")
                dbref.remove_class("hidden")

            elif not attrmeta.active and not 'hidden' in dbref.classes:
                logger.debug(f"making {dbref.key} hidden")
                dbref.set_class("hidden")
        cfgAttrMeta.clear_changed_history()
        logger.debug("update_ui..end")
        pass
    wp.update_ui_component = update_ui_component
    wp.on("page_ready", on_page_ready)
    return wp
