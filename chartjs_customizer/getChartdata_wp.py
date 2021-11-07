from addict import Dict
from dpath.util import get as dget
from dpath.util import set as dset

import justpy as jp
import webapp_framework as wf
import ui_styles as sty
import tailwind_tags as tw
import pprint
from .session_data import session_data


def no_action(dbref, msg):
    pass


sample_label = ["l1", "l2", "l3", "l4", "l5"]
sample_data = [[{'x': 1, 'y': 3}, {'x': 5, 'y': 5}],
               [{'x': 1, 'y': 7}, {'x': 5, 'y': 2}],
               [{'x': 1, 'y': 0}, {'x': 5, 'y': 8}],
               [{'x': 1, 'y': 13}, {'x': 5, 'y': 2}],
               [{'x': 1, 'y': 2}, {'x': 5, 'y': 6}],
               [{'x': 1, 'y': 9}, {'x': 5, 'y': 7}],
               ]


def launcher(request):
    wp = jp.QuasarPage()
    wp.tailwind = True
    wp.head_html = """<script src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js" > </script >\n    <link href = "https://unpkg.com/tailwindcss/dist/tailwind.min.css" rel = "stylesheet" >"""

    tlc = jp.Div(a=wp, classes=tw.tstr(*sty.tlc))
    refBoard = Dict()
    # =================== db for chart label input ===================
    labelsarea_ = wf.register(refBoard, wf.fc.textarea_("label", placeholder=pprint.pformat(sample_label),
                                                        readonly=False))
    span_ = wf.dur.span_("label", "Enter chart labels")
    labelpanel_ = wf.dc.StackV_(
        "labelpanel", cgens=[span_, labelsarea_], pcp=sty.panel)

    # ======================= db for chart data ======================
    textarea_ = wf.register(refBoard, wf.fc.textarea_("data", placeholder=pprint.pformat(sample_data),
                                                      readonly=False))
    span_ = wf.dur.span_("label", "Enter chart data")
    datapanel_ = wf.dc.StackV_(
        "datapanel", cgens=[span_, textarea_], pcp=sty.panel)
    heading_ = wf.heading__gen(f"Chart Data")
    ic_ = wf.dc.Infocard_(f'icChartData',  cgens=[
        heading_, labelpanel_, datapanel_])
    ic = ic_(tlc, "")
    # ========================= chart config =========================
    refBoard_ = refBoard.initialcfg = Dict()
    plottype_ = wf.fc.wrapdiv_(
        wf.register(refBoard_,
                    wf.fc.SelectorWBanner_("/type", "type",
                                           options=[
                                               "line", "bar"],
                                           values=[
                                               "line", "bar"], on_select=no_action
                                           )
                    )
    )

    # xAxisKey_ = wf.register(refBoard_,
    #                         wf.fc.TextInput_(
    #                             "/options/parsing/xAxisKey", "parsing/xAxisKey", "x", no_action)
    #                         )
    # yAxisKey_ = wf.register(refBoard_,
    #                         wf.fc.TextInput_(
    #                             "/options/parsing/yAxisKey", "parsing/yAxisKey", "y", no_action)
    #                         )

    heading_ = wf.heading__gen("Configure Chart: Initial Config")
    panel_ = wf.dc.StackG_("panel", cgens=[plottype_, xAxisKey_, yAxisKey_],
                           pcp=sty.grid)

    def on_submit_click(dbref, msg):
        wf.refresh(refBoard)
        print("data labels = ", refBoard.label.val)
        print("data  = ", refBoard.data.val)
        print("data  = ", refBoard.initialcfg["/type"].val)
        # print("data  = ", refBoard.initialcfg["/options/parsing/xAxisKey"].val)
        # print("data  = ", refBoard.initialcfg["/options/parsing/yAxisKey"].val)

        cfgctx = Dict()
        cfgctx.plttype = ct.PlotType.Line
        cfgctx.xaxis_type = ct.ScaleType.Linear
        cfgctx.xaxis_title = "xaxis"
        cfgctx.yaxis_title = "yaxis"
        cfgctx.plot_title = "plot title"
        cfg = ct.build_pltcfg(cfgctx)
        chartcfg = ct.build_cfg(cfg, refBoard.label.val, refBoard.data.val)
        dset(chartcfg, "/type", refBoard.initialcfg["/type"].val)
        # dset(chartcfg, "/options/parsing/xAxisKey",
        #      refBoard.initialcfg["/options/parsing/xAxisKey"].val)
        # dset(chartcfg, "/options/parsing/yAxisKey",
        #      refBoard.initialcfg["/options/parsing/yAxisKey"].val)

        session_data[request.session_id] = chartcfg
        pass
    submit_ = wf.dur.divbutton_(
        "Submit",  "Submit", "Build Chart", on_submit_click)

    ic_ = wf.dc.Infocard_(f'icInitialcfg',  cgens=[
        heading_, panel_, submit_], pcp=sty.infocard)
    ic = ic_(tlc, "")
    # ================================================================
    return wp


app = jp.app
jp.justpy(launcher, start_server=False)
