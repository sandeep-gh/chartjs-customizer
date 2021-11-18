import pprint
from aenum import extend_enum, auto
from addict import Dict
from dpath.util import get as dget, set as dset,  new as dnew
import justpy as jp
import webapp_framework as wf
from webapp_framework import dpop
import tailwind_tags as tw
from .chart_ui_cfg import CPT, addict_walker, get_baseCfgAttrMeta, update_chartCfg, FalseDict, update_cfgattrmeta
from . import ui_styles as sty
# import actions
import importlib
import sys
import traceback
# importlib.reload(sys.modules['chartjs_customizer.chart_ui_cfg'])

# from .session_data import session_data


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

    # def uicattrwalker(cfggroup_iter):
    #     for kpath, attrmeta in cfggroup_iter:
    #         yield kpath, attrmeta
    #         if attrmeta.vtype == FalseDict:
    #             yield from addict_walker(attrmeta.vrange)

    def cfggroup_iter():
        """
            iterator over attrmeta belonging to cfggroup
        """
        def is_in_group(kpath, attrmeta):
            if attrmeta.group == CPT.initial:  # TODO: should we filter based on is_active
                return True
            return False
        yield from filter(lambda _: is_in_group(_[0], _[1]), addict_walker(cfgAttrMeta))
    # uic_iter = wf.uic_iter("Initial config", cfggroup_iter(),
    # refBoard_)
    uic_iter = wf.uic_iter("Initial config", cfggroup_iter(),
                           refBoard_)
    cfgpanel_ = wf.dc.StackG_("cfgpanel", cgens=uic_iter,
                              pcp=sty.cfgpanels.cfgpanel)
    heading_ = wf.heading__gen("Configure Chart: Initial Config")

    # ========================= end ui stuff =========================

    def update_ui():
        print(refBoard_)
        for kpath in cfgAttrMeta.get_changed_history():
            attrmeta = dget(cfgAttrMeta, kpath)
            dbref = refBoard_[kpath]._go.target
            if attrmeta.active and 'hidden' in dbref.classes:
                dbref.remove_class("hidden")
                print(kpath, " ", dbref.classes)
            elif not attrmeta.active and not 'hidden' in dbref.classes:
                dbref.set_class("hidden")
        cfgAttrMeta.clear_changed_history()
        # ========================= action stuff =========================
        # extend_enum(wf.ModelUpdaterTag, 'UPDATE_CFGATTRMETA',
        #             actions.UPDATE_CFGATTRMETA)
        # extend_enum(wf.ModelUpdaterTag, 'UPDATE_CHARTCFG',
        #             actions.GEN_EDCFG_FILE)
        # extend_enum(wf.FrontendReactActionTag, 'UPDATE_UI',
        #             actions.GEN_EDCFG_FILE)

    def on_submit_click(dbref, msg):
        print("go  on ...build the chart")
    submit_ = wf.dur.divbutton_(
        "Submit",  "Submit", "Build Chart", on_submit_click)

    ic_ = wf.dc.Infocard_(f'icInitialcfg',  cgens=[
        heading_, cfgpanel_, submit_], pcp=sty.infocard)
    ic = ic_(tlc, "")
    # ================================================================

    # ==================== frontend react actions ====================
    def update_ui_component():
        """
        update ui on ui state change;
        eventually this should be called update_ui only
        """
        wf.refresh(refBoard_)
        for kpath, attrmeta in cfggroup_iter():
            if attrmeta.active:
                if dget(cjs_cfg, kpath) != refBoard_[kpath].val:
                    print(f"update chartcfg {kpath}")
                    wf.dupdate(cjs_cfg, kpath, refBoard_[kpath].val)

        update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
        for kpath in cfgAttrMeta.get_changed_history():
            attrmeta = dget(cfgAttrMeta, kpath)
            dbref = refBoard_[kpath]._go.target
            if attrmeta.active and 'hidden' in dbref.classes:
                dbref.remove_class("hidden")
                print(kpath, " ", dbref.classes)
            elif not attrmeta.active and not 'hidden' in dbref.classes:
                dbref.set_class("hidden")
        cfgAttrMeta.clear_changed_history()
    wp.update_ui_component = update_ui_component

    # ============================== end =============================
    return wp
