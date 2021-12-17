import importlib
import sys
import traceback
from .cfgpanel_sbs import cfggroup_panel_
from .chart_ui_cfg import CPT, get_baseCfgAttrMeta, update_chartCfg, update_cfgattrmeta, add_dataset, build_plt_cfg
from aenum import extend_enum, auto
import json
import jsbeautifier
from justpy_chartjs import chartjscomponents as cj
import copy
import re
import logging
import justpy as jp
from addict import Dict
from dpath.util import get as dget, set as dset,  new as dnew
import webapp_framework as wf  # dc, dbr, Dockbar, FrontendReactActionTag
from . import fancysty as sty

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
    wp = jp.QuasarPage()
    wp.tailwind = True
    wp.head_html = """<script src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js" > </script >\n    <link href = "https://unpkg.com/tailwindcss/dist/tailwind.min.css" rel = "stylesheet" >"""

    wp.model = Dict(track_changes=True)

    # ================ initialize chart and ui configs ===============
    cjs_cfg = Dict(track_changes=True)
    ui_cfg = Dict(track_changes=True)

    cfgAttrMeta = get_baseCfgAttrMeta()
    update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
    add_dataset(cjs_cfg)
    print("post data addition = ", cjs_cfg)
    cjs_cfg.clear_changed_history()
    dset(cjs_cfg, "/type", "line")
    print("initial chartcfg ", cjs_cfg)
    update_cfgattrmeta(cjs_cfg, cfgAttrMeta)

    # ============================= done =============================

    refBoard_ = Dict(track_changes=True)
    cfgpanel_all_ = cfggroup_panel_(CPT.all, cjs_cfg, cfgAttrMeta, refBoard_)

    dockbar_ = wf.Dockbar.build_dockbar_('dockbar')
    tlc_ = wf.dc.StackG_("analysisPanel", 4, 6,  cgens=[cfgpanel_all_],
                         pcp=sty.analysisPanel)

    cjs_plt_cfg = build_plt_cfg(cjs_cfg)
    pltcanvas_ = cj.ChartJS_("pltcanvas", pcp=[], options=cjs_plt_cfg)
    noticeboard_ = wf.dbr.Noticebord_("noticeboard")
    rootde_ = wf.dc.StackV_(
        "rootde",  cgens=[dockbar_, pltcanvas_, tlc_, noticeboard_], pcp=sty.rootde)

    dbref_rootde = rootde_(wp, "")
    dbref_dockbar = dbref_rootde.getItem('dockbar')
    dbref_noticeboard = dbref_rootde.getItem('noticeboard')
    dbref_chartcbox = dbref_rootde.getItem("pltcanvas")
    wf.refresh(refBoard_)
    refBoard_.clear_changed_history()
    extend_enum(wf.FrontendReactActionTag, 'UpdateChart', auto())

    def locate_de(detag):
        '''
        find dbref at path encoded in detag
        '''
        croot = dbref_rootde
        cprefix = "rootde_"
        depath = detag.split("_")[1:]
        for c in depath:
            print("in locate_de = ", croot.apkdbmap)
            cdbref = croot.apkdbmap[cprefix + c]
            cprefix = cdbref.apk + "_"
            croot = cdbref
        return cdbref

    def run_frontendReactAction(tag, arg):
        # logger.info(f"in run_frontendReactAction : {tag} {arg}")
        match tag:
            case wf.FrontendReactActionTag.NoticeboardPost:
                dbref_noticeboard.post(wp.model.noticeboard_message)

            case wf.FrontendReactActionTag.DockInfocard:
                dbref_dockbar.dockde(arg.tdbref)
            case wf.FrontendReactActionTag.UndockInfocard:
                tdbref = locate_de(arg.tapk)
                dbref_dockbar.undockde(tdbref)
            case wf.FrontendReactActionTag.UpdateChart:
                cjs_plt_cfg = build_plt_cfg(cjs_cfg)
                print("update chart with : ", cjs_plt_cfg)
                dbref_chartcbox.chartjs.new_chart(cjs_plt_cfg)
                pass

        pass

    wp.run_frontendReactAction = run_frontendReactAction

    # ==================== frontend react actions ====================
    def update_ui_component():
        """
        update ui on ui state change;
        eventually this should be called update_ui only
        """
        print("ui state changed: update cjs_cfg; cfgattrmeta; ui components")
        try:
            refBoard_.clear_changed_history()
            wf.refresh(refBoard_)
            for kpath in refBoard_.get_changed_history():
                kpath = kpath.lstrip()
                # .replace("/val$", "").strip()
                cjs_cfg_path = re.sub("/val$", "", kpath)
                print(f"refBoard path:{kpath}:{cjs_cfg_path}:")
                wf.dupdate(cjs_cfg, cjs_cfg_path, dget(refBoard_, kpath))

            print("post cfg  update = ", cjs_cfg)
            update_cfgattrmeta(cjs_cfg, cfgAttrMeta)

            for kpath in cfgAttrMeta.get_changed_history():
                kpath = kpath.lstrip()
                print(f"changed cfgAttrMeta:{kpath}:")
                attrmeta = dget(cfgAttrMeta, kpath)
                dbref = dget(refBoard_, kpath)._go.target

                if attrmeta.active and 'hidden' in dbref.classes:
                    dbref.remove_class("hidden")
                    #print(kpath, " ", dbref.classes)
                elif not attrmeta.active and not 'hidden' in dbref.classes:
                    dbref.set_class("hidden")
            cfgAttrMeta.clear_changed_history()
        except Exception as e:
            print("exception : ", e)
            traceback. print_exc()
            raise e
        run_frontendReactAction(wf.FrontendReactActionTag.UpdateChart, None)
    wp.update_ui_component = update_ui_component

    # ============================== end =============================

    wp.on('page_ready', page_ready)
    return wp
