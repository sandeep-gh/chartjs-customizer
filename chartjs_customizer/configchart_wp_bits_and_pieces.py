from addict import Dict
from . import session_data
import justpy as jp
from .cfgpanel_sbs import cfggroup_panel_
from dpath.util import get as dget, set as dset,  new as dnew, search as dsearch
from .chart_ui_cfg import add_dataset
import pickle
from .chart_ui_cfg import CPT, addict_walker, get_baseCfgAttrMeta, update_chartCfg, FalseDict, update_cfgattrmeta

import json


@jp.SetRoute('/getchartdata')
def launcher(request):
    wp = jp.QuasarPage()
    wp.tailwind = False
    wp.head_html = """
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js"></script >\n    
    <script src="https://cdn.tailwindcss.com/"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css">
    """
    wp.css = 'body { font-family: Inter; }'

    # ================ initialize chart and ui configs ===============
    cfgAttrMeta = get_baseCfgAttrMeta()
    cjs_cfg = Dict(track_changes=True)
    ui_cfg = Dict(track_changes=True)
    update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
    #session_id = request.session_id

    #[cjs_cfg, ui_cfg, cfgAttrMeta] = session_data.get(session_id)
    # with open("session_data.pickle", "rb") as fh:
    #     [cjs_cfg, ui_cfg, cfgAttrMeta] = pickle.load(fh)
    add_dataset(cjs_cfg)
    #dnew(cjs_cfg, "/data/labels", "[1,2,4,5]")
    dset(cjs_cfg, "/type", "line")
    print(json.dumps(cjs_cfg))
    cjs_cfg.clear_changed_history()

    # ============================= done =============================
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

    return wp


# launcher(None)
