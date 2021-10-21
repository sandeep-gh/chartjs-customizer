import importlib
import sys
import traceback
from .cfgpanel_sbs import cfggroup_panel_
from .chart_ui_cfg import CPT, get_baseCfgAttrMeta, update_chartCfg, update_cfgattrmeta, add_dataset, build_plt_cfg
from aenum import extend_enum, auto
import json
from justpy_chartjs import chartjscomponents as cj
import copy
import re
import logging
import justpy as jp
from addict import Dict
from dpath.util import get as dget, set as dset,  new as dnew
import webapp_framework as wf  # dc, dbr, Dockbar, FrontendReactActionTag
from . import fancysty as sty

# importlib.reload(sys.modules['chartjs_customizer.chart_ui_cfg'])
# importlib.reload(sys.modules['chartjs_customizer.cfgpanel_sbs'])


def page_ready(self, msg):
    '''
    update dl login status after the page is ready
    '''

    return


def launcher(request):
    logger = logging.getLogger('webapp')
    logger.setLevel(logging.INFO)
    wp = jp.QuasarPage()
    wp.tailwind = False
    wp.head_html = """
<script src="https://cdn.tailwindcss.com/"></script>
    <link
     rel="stylesheet"
     href="https://unpkg.com/@tailwindcss/typography@0.4.x/dist/typography.min.css"
    />
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js" >
    """

    wp.model = Dict(track_changes=True)

    # ================ initialize chart and ui configs ===============
    cjs_cfg = Dict(track_changes=True)  # the chart configuration
    ui_cfg = Dict(track_changes=True)  # the cfg for ui of chart controls

    cfgAttrMeta = get_baseCfgAttrMeta()  # description for each of the chart controls
    update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
    add_dataset(cjs_cfg)
    print("post data addition = ", cjs_cfg)
    cjs_cfg.clear_changed_history()
    dset(cjs_cfg, "/type", "line")
    print("initial chartcfg ", cjs_cfg)
    update_cfgattrmeta(cjs_cfg, cfgAttrMeta)

    # ============================= done =============================
    refBoard_ = Dict(track_changes=True)  # tracker for ui changes
    # build all cfg control panels
    cfgpanel_all_ = cfggroup_panel_(CPT.all, cjs_cfg, cfgAttrMeta, refBoard_)
    tlc_ = cfgpanel_all_
    # wf.dc.StackG_("analysisPanel", 4, 6,  cgens=[cfgpanel_all_],
    # pcp=sty.analysisPanel)  # arrange the panels in grid layout

    cjs_plt_cfg = build_plt_cfg(cjs_cfg)  # build chartjs compatible cfg
    pltcanvas_ = cj.ChartJS_(
        "pltcanvas", pcp=[], options=cjs_plt_cfg)  # build the chart
    noticeboard_ = wf.dbr.Noticebord_("noticeboard")
    dockbar_ = wf.Dockbar.build_dockbar_('dockbar')
    rootde_ = wf.dc.StackV_(
        "rootde",  cgens=[pltcanvas_, tlc_], pcp=sty.rootde)
    dbref_rootde = rootde_(wp, "")
    dbref_dockbar = dbref_rootde.getItem('dockbar')
    dbref_noticeboard = dbref_rootde.getItem('noticeboard')
    dbref_chartcbox = dbref_rootde.getItem("pltcanvas")
    wp.on('page_ready', page_ready)
    return wp
