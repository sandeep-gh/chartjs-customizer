import logging
import justpy as jp
from addict import Dict
from webapp_framework import dur, dc, dbr, Dockbar, FrontendReactActionTag
from justpy_chartjs import chartjscomponents as cj
from chartcfg_builder import chartcfg
from cfgpanels import build_cfgpanel_
import ui_styles
import jsbeautifier
import json
from aenum import extend_enum, auto

my_chart_def2 = """{
              type: 'bar',
              data: {
                  labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                  datasets: [{
data: [5,6,7,8,9,10, 11]

}
]
              },
              options: {
                  scales: {
                      y: {
                          beginAtZero: true
                      }
                  },

                  title: {
                      display: true,
                      text: 'Custom Chart Title',
position: 'bottom'
                  }
              }
          }"""


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
    #wp.head_html = """<script src = "https://cdn.jsdelivr.net/npm/chart.js" > </script >\n    <link href = "https://unpkg.com/tailwindcss/dist/tailwind.min.css" rel = "stylesheet" >"""
    wp.head_html = """<script src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js" > </script >\n    <link href = "https://unpkg.com/tailwindcss/dist/tailwind.min.css" rel = "stylesheet" >"""
    wp.tailwind = True
    wp.model = Dict(track_changes=True)
    dockbar_ = Dockbar.build_dockbar_('dockbar')
    cfgpanel_simple_ = build_cfgpanel_("simple", chartcfg)
    cfgpanel_simplemore_ = build_cfgpanel_("simplemore", chartcfg)
    cfgpanel_nitpick_ = build_cfgpanel_("nitpick", chartcfg)
    cfgpanel_advanced_ = build_cfgpanel_("advanced", chartcfg)
    cfgpanel_ocd_ = build_cfgpanel_("ocd", chartcfg)
    #cfgpanel_advanced_ = build_cfgpanel_("ocd", chartcfg)

    tlc_ = dc.StackG_("analysisPanel", 4, 6,  cgens=[cfgpanel_simple_, cfgpanel_simplemore_, cfgpanel_nitpick_, cfgpanel_advanced_, cfgpanel_ocd_],
                      pcp=ui_styles.analysisPanel)

    # opts = jsbeautifier.default_options()
    # res = jsbeautifier.beautify(json.dumps(chartcfg), opts)
    # print(res)
    pltcanvas_ = cj.ChartJS_("pltcanvas", pcp=[], options=chartcfg)
    rootde_ = dc.StackV_(
        "rootde",  cgens=[dockbar_, pltcanvas_, tlc_], pcp=ui_styles.rootde)
    dbref_rootde = rootde_(wp, "")
    dbref_dockbar = dbref_rootde.getItem('dockbar')
    dbref_chartcbox = dbref_rootde.getItem("pltcanvas")
    dbref_noticeboard = dbr.Noticebord_("noticeboard")(wp, "")

    logger.info("end profiling")
    print(" data\-", chartcfg)

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

    # add tags

    extend_enum(FrontendReactActionTag, 'UpdateChart', auto())

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
                print("need to update chart")
                # print("charcbox = ", dbref_chartcbox)
                # print("chartjs = ", dbref_chartcbox.chartjs)
                dbref_chartcbox.chartjs.new_chart(arg.chartcfg)

                # dbref_chartcbox.chartjs.new_chart(my_chart_def2)

        pass

    wp.run_frontendReactAction = run_frontendReactAction
    wp.on('page_ready', page_ready)
    return wp


app = jp.app
jp.justpy(launcher, start_server=False)
