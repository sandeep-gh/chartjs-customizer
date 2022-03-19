"""main entry point to chartjs customizer
"""
import traceback
import logging
import os
import dill as pickle
import re
if logging:  # pin code here so that ide doesn't move around the import statements
    # try:
    #     os.remove("chartjs_customizer.log")
    # except:
    #     pass
    #logging.basicConfig(filename="chartjs_customizer.log", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict, refBoard

import justpy as jp

import webapp_framework as wf
#from .attrmeta import get_basecfg, uiorgCat
from .attrmeta_basecfg_helper import uiorgCat
from .attrmeta_basecfg_orig import get_basecfg
from .chartcfg import (add_dataset, build_pltcfg, update_cfgattrmeta,
                       update_chartCfg)
from dpath.util import get as dget, set as dset,  new as dnew, search as dsearch

from addict import Dict
from aenum import extend_enum, auto
import jsbeautifier
from .chartjs_customizer_components import cfggroup_panel_
import json
from webapp_framework_tracking.dbrefBoard import refresh as dbrefBoard_refresh


def page_ready(self, msg):
    refBoard.clear_changed_history()
    dbrefBoard_refresh(refBoard)


# ========================== init cjs_cfg =========================
# chartjs configuration as nested-addict-AttrMeta
cfgAttrMeta = get_basecfg()

# cjs_cfg: Json version of cfgAttrMeta -- will come from session_dict
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

# ================================ end ===============================
extend_enum(wf.ReactTag_UI, 'UpdateChart', 'UpdateChart')


def gen_wp_components():
    """
    build stubs for all the components of the webpage
    """
    cfggroup_panel_(uiorgCat.all, cjs_cfg, cfgAttrMeta)
    # opts = jsbeautifier.default_options()
    # print(jsbeautifier.beautify(json.dumps(stubStore), opts))
    # print(jsbeautifier.beautify(json.dumps(cjs_cfg), opts))
    # print(cjs_cfg)
    return wf.Container_(cgens=[stubStore.uiorg_all.topPanel])


def make_wp_react(wp):
    """
    make the webpage responsive by code that modify 
    ui attributes and states
    """

    def update_ui():
        """update ui on update to cjs_cfg
        1. update cfgattrmeta based on context
        2. update ui 'hidden' attribute based newly active cfgattrmeta
        """
        logger.debug("in update_ui")
        logger.debug("bt_update_cfgattrmeta")
        update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
        logger.debug("end_update_cfgattrmeta")

        for kpath in cfgAttrMeta.get_changed_history():
            logger.debug(f"handle changed {kpath}")
            kpath = kpath.lstrip()
            attrmeta = dget(cfgAttrMeta, kpath)

            # dget(refBoard_, kpath)._go.target
            dbref = dget(refBoard, kpath)._go.target

            if attrmeta.active and 'hidden' in dbref.classes:
                logger.debug(f"unhide {kpath}")
                dbref.remove_class("hidden")

                # print(kpath, " ", dbref.classes)
            elif not attrmeta.active and not 'hidden' in dbref.classes:
                logger.debug(f"hide {kpath}")
                dbref.set_class("hidden")
            # if new attrmeta elements have active;add them to cjs_cfg
        # we should loop over updates until fix point is reached

        logger.debug("bt_update_chartcfg")
        update_chartCfg(cfgAttrMeta, cjs_cfg)
        logger.debug("end_update_chartcfg")
        cfgAttrMeta.clear_changed_history()
        cjs_cfg.clear_changed_history()
        logger.debug("done update_ui")

    def refresh_chart():
        cjs_plt_cfg = build_pltcfg(cjs_cfg)
        logger.debug("gt-update chart with new {cjs_plt_cfg}")
        # logger.debug(
        # f"this is pltcanvas dbref: {stubStore.pltctx.pltcanvas.target.chartjs}")
        stubStore.pltctx.pltcanvas.target.chartjs.new_chart(cjs_plt_cfg)

    def update_ui_component(dbref, msg):
        """
        all uic generated component ship there events directly here -- 
        instead of invoking MVULR
        """

        old_val = dget(cjs_cfg, dbref.key)
        wf.dupdate(cjs_cfg, dbref.key, msg.value)
        cfgAttrMeta.clear_changed_history()  # we should loop until done
        logger.debug(
            f"react: updated cjs_cfg: key={dbref.key} with value {msg.value}")
        update_ui()
        refresh_chart()

    def react_ui(tag, arg):
        match tag:
            case wf.ReactTag_UI.UpdateChart:
                refBoard.clear_changed_history()
                dbrefBoard_refresh(refBoard)
                for kpath in refBoard.get_changed_history():
                    kpath = kpath.lstrip()
                    logger.debug(
                        f"react_ui:TBD: path:{kpath} {dget(refBoard, kpath)} ")
                    # horrible approach
                    cjs_cfg_path = re.sub("/val$", "", kpath)
                    wf.dupdate(cjs_cfg, cjs_cfg_path, dget(refBoard, kpath))

                refresh_chart()

    wp.update_ui_component = update_ui_component
    wp.react_ui = react_ui


@ jp.SetRoute('/customize_chartjs')
def wp_chartjs_customizer(request):
    wp_components = gen_wp_components()
    # with open("components.pickle", "wb") as fh:
    #     pickle.dump(wp_components, fh)

    wp = wf.WebPage_("wp_index", page_type='quasar', head_html_stmts=[
        """<script src = "https://cdn.jsdelivr.net/npm/chart.js"></script >"""], cgens=[wp_components])()
    make_wp_react(wp)
    # logging.info("this is info")
    # logging.debug("this is debug")
    # wp = jp.QuasarPage()
    # wp.tailwind = False
    # wp.head_html = """
    # \n
    # <script src="https://cdn.tailwindcss.com/"></script>
    # <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css">
    # """

    # ================ initialize chart and ui configs ===============
    wp.on('page_ready', page_ready)
    return wp
