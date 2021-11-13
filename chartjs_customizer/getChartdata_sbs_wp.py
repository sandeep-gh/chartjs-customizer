from chart_ui_cfg import CPT, addict_walker, get_baseCfgAttrMeta, update_chartCfg
from addict import Dict
from dpath.util import get as dget, set as dset, delete as dpop, new as dnew

import justpy as jp
import webapp_framework as wf
import ui_styles as sty
import tailwind_tags as tw
import pprint
import importlib
import sys
# importlib.reload(sys.modules['chartjs_customizer.chart_ui_cfg'])

#from .session_data import session_data


sample_label = ["l1", "l2", "l3", "l4", "l5"]
sample_data = [[{'x': 1, 'y': 3}, {'x': 5, 'y': 5}],
               [{'x': 1, 'y': 7}, {'x': 5, 'y': 2}],
               [{'x': 1, 'y': 0}, {'x': 5, 'y': 8}],
               [{'x': 1, 'y': 13}, {'x': 5, 'y': 2}],
               [{'x': 1, 'y': 2}, {'x': 5, 'y': 6}],
               [{'x': 1, 'y': 9}, {'x': 5, 'y': 7}],
               ]


def no_action(dbref, msg):
    pass


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

    refBoard_ = refBoard.initialcfg = Dict()
    # plottype_ = wf.fc.wrapdiv_(
    #     wf.register(refBoard_,
    #                 wf.fc.SelectorWBanner_("/type", "type",
    #                                        options=[
    #                                            "line", "bar"],
    #                                        values=[
    #                                            "line", "bar"], on_select=no_action
    #                                        )
    #                 )
    # )
    cjs_cfg = Dict(track_changes=True)
    ui_cfg = Dict(track_changes=True)
    cfgAttrMeta = get_baseCfgAttrMeta()
    update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
    cjs_cfg.clear_changed_history()  # don't care much for the change right now

    def cfggroup_iter():
        """
            iterator over attrmeta belonging to cfggroup
        """
        def is_in_group(kpath, attrmeta):
            if attrmeta.group == CPT.initial:  # TODO: should we filter based on is_active
                return True
            return False
        yield from filter(lambda _: is_in_group(_[0], _[1]), addict_walker(cfgAttrMeta))
    uic_iter = wf.uic_iter("Initial config", cfggroup_iter(),
                           refBoard_)
    cfgpanel_ = wf.dc.StackG_("cfgpanel", cgens=uic_iter,
                              pcp=sty.cfgpanels.cfgpanel)
    heading_ = wf.heading__gen("Configure Chart: Initial Config")

    def on_submit_click(dbref, msg):
        print(refBoard_)
        wf.refresh(refBoard_)
        print(refBoard_)
        #session_data[request.session_id] = chartcfg
        print(cjs_cfg)
        print(dget(cjs_cfg, "/type"))
        #dpop(cjs_cfg, "/options/parsing")
        #print("post delte ", cjs_cfg)
        for kpath, attrmeta in cfggroup_iter():
            print(kpath, attrmeta)
            print("val = ", refBoard_[kpath].val)
            #print("set val ", kpath, " ", dget(refBoard_, kpath))
            try:
                print(dget(cjs_cfg, "/type"))
                print(dget(cjs_cfg, kpath))
                if kpath == "/type":
                    cjs_cfg.pop('type', None)
                else:
                    optdict = dget(cjs_cfg, "/options")
                    print("optdict = ", optdict)
                    optdict.pop("parsing", None)
                print("a")
                dnew(cjs_cfg, kpath, refBoard_[kpath].val)
                print("b", cjs_cfg)
            except Exception as e:
                print(e)
                raise ValueError

        print("changed history ", cjs_cfg)
        for _ in cjs_cfg.get_changed_history():
            print(_)
        pass
    submit_ = wf.dur.divbutton_(
        "Submit",  "Submit", "Build Chart", on_submit_click)

    ic_ = wf.dc.Infocard_(f'icInitialcfg',  cgens=[
        heading_, cfgpanel_, submit_], pcp=sty.infocard)
    ic = ic_(tlc, "")
    # ================================================================
    return wp


app = jp.app
jp.justpy(launcher, start_server=False)
