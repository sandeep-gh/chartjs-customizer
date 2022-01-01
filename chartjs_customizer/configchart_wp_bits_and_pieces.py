import traceback
import sys
import jsbeautifier
import re
from aenum import extend_enum, auto
from addict import Dict
from . import session_data
import justpy as jp
from .cfgpanel_sbs import cfggroup_panel_
#from .chart_ui_cfg import CPT, get_baseCfgAttrMeta, update_chartCfg, update_cfgattrmeta, add_dataset, build_plt_cfg
from dpath.util import get as dget, set as dset,  new as dnew, search as dsearch
import pickle
#from .chart_ui_cfg import CPT, addict_walker, get_baseCfgAttrMeta, update_chartCfg, FalseDict, update_cfgattrmeta
from justpy_chartjs import chartjscomponents as cj
import webapp_framework as wf
import json
from . import snowsty as sty

from . import attrmeta
from .chartcfg import update_chartCfg, update_cfgattrmeta, add_dataset, build_pltcfg

extend_enum(wf.FrontendReactActionTag, 'UpdateChart', auto())


def page_ready(self, msg):
    '''
    update dl login status after the page is ready
    '''
    styreport = wf.styreport()
    opts = jsbeautifier.default_options()
    res = jsbeautifier.beautify(json.dumps(styreport), opts)
    # print(res)
    #print("on page ready ", styreport)
    return


def all_things_page(wp):
    cfgAttrMeta = attrmeta.get_basecfg()
    cjs_cfg = Dict(track_changes=True)
    update_chartCfg(cfgAttrMeta, cjs_cfg)
    cfgAttrMeta.clear_changed_history()
    #session_id = request.session_id

    #[cjs_cfg, ui_cfg, cfgAttrMeta] = session_data.get(session_id)
    # with open("session_data.pickle", "rb") as fh:
    #     [cjs_cfg, ui_cfg, cfgAttrMeta] = pickle.load(fh)
    add_dataset(cjs_cfg)
    dnew(cjs_cfg, "/data/labels", "[1,2,4,5]")
    dset(cjs_cfg, "/type", "line")
    update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
    update_chartCfg(cfgAttrMeta, cjs_cfg)
    cfgAttrMeta.clear_changed_history()
    cjs_cfg.clear_changed_history()
    # opts = jsbeautifier.default_options()
    # res = jsbeautifier.beautify(json.dumps(cjs_cfg), opts)
    # print(res)
    # cjs_cfg.clear_changed_history()
    # ============================= done =============================
    # ============================= done =============================
    refBoard_ = Dict(track_changes=True)  # tracker for ui changes
    # build all cfg control panels
    cfgpanel_all_ = cfggroup_panel_(
        attrmeta.CPT.all, cjs_cfg, cfgAttrMeta, refBoard_)
    #tlc_ = cfgpanel_all_
    # wf.dc.StackG_("analysisPanel", 4, 6,  cgens=[cfgpanel_all_],
    # pcp=sty.analysisPanel)  # arrange the panels in grid layout

    cjs_plt_cfg = build_pltcfg(cjs_cfg)  # build chartjs compatible cfg
    pltcanvas_ = cj.ChartJS_(
        "pltcanvas", pcp=[], options=cjs_plt_cfg)  # build the chart
    noticeboard_ = wf.dbr.Noticebord_("noticeboard")
    dockbar_ = wf.Dockbar.build_dockbar_('dockbar')
    rootde_ = wf.hc.StackV_(
        "rootde",  cgens=[cfgpanel_all_, pltcanvas_], pcp=sty.rootde)
    dbref_rootde = rootde_(wp, "")
    dbref_dockbar = dbref_rootde.getItem('dockbar')
    dbref_noticeboard = dbref_rootde.getItem('noticeboard')
    dbref_chartcbox = dbref_rootde.getItem("pltcanvas")

    def update_ui():
        """update ui on update to cjs_cfg
        1. update cfgattrmeta based on context
        2. update ui 'hidden' attribute based newly active cfgattrmeta
        """
        update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
        for kpath in cfgAttrMeta.get_changed_history():
            print(f"update_ui_component:cfgattrmeta: {kpath}")
            kpath = kpath.lstrip()
            attrmeta = dget(cfgAttrMeta, kpath)
            dbref = dget(refBoard_, kpath)._go.target

            if attrmeta.active and 'hidden' in dbref.classes:
                dbref.remove_class("hidden")
                #print(kpath, " ", dbref.classes)
            elif not attrmeta.active and not 'hidden' in dbref.classes:
                dbref.set_class("hidden")
            # if new attrmeta elements have active;add them to cjs_cfg
        update_chartCfg(cfgAttrMeta, cjs_cfg)
        cfgAttrMeta.clear_changed_history()
        cjs_cfg.clear_changed_history()
        print("done update ui")

    def refresh_chart():
        cjs_plt_cfg = build_pltcfg(cjs_cfg)
        print("update chart with : ", cjs_plt_cfg)
        dbref_chartcbox.chartjs.new_chart(cjs_plt_cfg)

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
                # refresh rebBoard, cjs_cfg, cfgAttrMeta, ui, cjs
                print("calling UpdateChart")
                refBoard_.clear_changed_history()
                wf.refresh(refBoard_)
                for kpath in refBoard_.get_changed_history():
                    kpath = kpath.lstrip()
                    cjs_cfg_path = re.sub("/val$", "", kpath)
                    print(f"refBoard path:{kpath}:{cjs_cfg_path}:")
                    wf.dupdate(cjs_cfg, cjs_cfg_path, dget(refBoard_, kpath))
                    print("UpdateChart: ", dget(cjs_cfg, cjs_cfg_path))
                update_ui()
                refresh_chart()
                pass

        pass

    wp.run_frontendReactAction = run_frontendReactAction

    def update_ui_component(dbref, msg):
        """
        react  to changes on the ui panel
        """
        try:
            print(f"{dbref.key}, {dbref.apk} updated with {msg.value}")
            old_val = dget(cjs_cfg, dbref.key)
            wf.dupdate(cjs_cfg, dbref.key, msg.value)
            cfgAttrMeta.clear_changed_history()
            update_ui()
            refresh_chart()
            # fold in the changes into refBoard
            wf.refresh(refBoard_, [dbref.key])

        except Exception as e:
            print("exception : ", e)
            traceback. print_exc()
            raise e

    wp.update_ui_component = update_ui_component
    wp.on('page_ready', page_ready)


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
    try:
        all_things_page(wp)
    except Exception as e:
        print("error occured ", e)
        traceback. print_exc()
        raise e
    return wp


# launcher(None)
