import logging
import justpy as jp
from addict import Dict
from webapp_framework import dur, dc, dbr, Dockbar, FrontendReactActionTag
from justpy_chartjs import chartjscomponents as cj
from chartcfg_builder import chartcfg
from cfgpanels import build_cfgpanel_
import ui_styles


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
    wp.head_html = """<script src = "https://cdn.jsdelivr.net/npm/chart.js" > </script >\n    <link href = "https://unpkg.com/tailwindcss/dist/tailwind.min.css" rel = "stylesheet" >"""
    wp.tailwind = True
    wp.model = Dict(track_changes=True)
    dockbar_ = Dockbar.build_dockbar_('dockbar')
    cfgpanel_simple_ = build_cfgpanel_("simple")
    tlc_ = dc.StackG_("analysisPanel", 4, 6,  cgens=[cfgpanel_simple_],
                      pcp=ui_styles.analysisPanel)

    pltcanvas_ = cj.ChartJS_("pltcanvas", pcp=[], options=chartcfg)
    rootde_ = dc.StackV_(
        "rootde",  cgens=[dockbar_, tlc_], pcp=ui_styles.rootde)
    dbref_rootde = rootde_(wp, "")
    dbref_dockbar = dbref_rootde.getItem('dockbar')
    dbref_noticeboard =  dbr.Noticebord_("noticeboard")(wp, "")
    logger.info("end profiling")
    def locate_de(detag):
        '''
        find dbref at path encoded in detag
        '''
        croot = dbref_rootde
        cprefix = "rootde_"
        depath = detag.split("_")[1:]
        for c in depath:
            print ("in locate_de = ", croot.apkdbmap)
            cdbref = croot.apkdbmap[cprefix + c]
            cprefix = cdbref.apk + "_"
            croot = cdbref
        return cdbref    
    def run_frontendReactAction(tag, arg):
        logger.info(f"in run_frontendReactAction : {tag} {arg}")
        match tag:  
            case FrontendReactActionTag.NoticeboardPost:
                dbref_noticeboard.post(wp.model.noticeboard_message)
                
            case FrontendReactActionTag.DockInfocard:
                dbref_dockbar.dockde(arg.tdbref)
            case FrontendReactActionTag.UndockInfocard:
                tdbref = locate_de(arg.tapk)
                dbref_dockbar.undockde(tdbref)

        pass

    wp.run_frontendReactAction = run_frontendReactAction
    wp.on('page_ready', page_ready)
    return wp

app = jp.app
jp.justpy(launcher, start_server=False)
    
