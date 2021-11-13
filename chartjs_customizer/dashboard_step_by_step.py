import logging
import justpy as jp
from addict import Dict
from webapp_framework import dur, dc, dbr, Dockbar, FrontendReactActionTag
from justpy_chartjs import chartjscomponents as cj
from . import ui_styles
import jsbeautifier
import json
from aenum import extend_enum, auto
from .chart_ui_cfg import CPT, get_baseCfgAttrMeta, update_chartCfg

from .cfgpanel_sbs import cfggroup_panel_

import sys
import importlib
importlib.reload(sys.modules['chartjs_customizer.chart_ui_cfg'])
importlib.reload(sys.modules['chartjs_customizer.cfgpanel_sbs'])


def page_ready(self, msg):
    '''
    update dl login status after the page is ready
    '''

    return


def launcher(request):
    logger = logging.getLogger('webapp')
    logger.setLevel(logging.INFO)
    logger.info("start profiling")
    wp = jp.QuasarPage()
    wp.head_html = """<script src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js" > </script >\n    <link href = "https://unpkg.com/tailwindcss/dist/tailwind.min.css" rel = "stylesheet" >"""

    wp.model = Dict(track_changes=True)

    # ================ initialize chart and ui configs ===============
    cjs_cfg = Dict(track_changes=True)
    ui_cfg = Dict(track_changes=True)
    cfgAttrMeta = get_baseCfgAttrMeta()
    update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
    # ============================= done =============================

    cfgpanel_all_ = cfggroup_panel_(CPT.all, cjs_cfg, cfgAttrMeta)

    dockbar_ = Dockbar.build_dockbar_('dockbar')
    tlc_ = dc.StackG_("analysisPanel", 4, 6,  cgens=[cfgpanel_all_],
                      pcp=ui_styles.analysisPanel)

    noticeboard_ = dbr.Noticebord_("noticeboard")
    rootde_ = dc.StackV_(
        "rootde",  cgens=[dockbar_, tlc_, noticeboard_], pcp=ui_styles.rootde)

    dbref_rootde = rootde_(wp, "")
    dbref_dockbar = dbref_rootde.getItem('dockbar')
    dbref_dockbar = dbref_rootde.getItem('noticeboard')
    #dbref_chartcbox = dbref_rootde.getItem("pltcanvas")

    def run_frontendReactAction(tag, arg):
        # logger.info(f"in run_frontendReactAction : {tag} {arg}")
        match tag:
            case FrontendReactActionTag.NoticeboardPost:
                dbref_noticeboard.post(wp.model.noticeboard_message)

            case FrontendReactActionTag.DockInfocard:
                dbref_dockbar.dockde(arg.tdbref)
            case FrontendReactActionTag.UndockInfocard:
                tdbref = locate_de(arg.tapk)
                dbref_dockbar.undockde(tdbref)
            case FrontendReactActionTag.UpdateChart:
                pass

        pass

    wp.run_frontendReactAction = run_frontendReactAction
    wp.on('page_ready', page_ready)
    return wp
