import pprint
from aenum import extend_enum, auto
from addict import Dict
from dpath.util import get as dget, set as dset,  new as dnew, search as dsearch
import justpy as jp
import webapp_framework as wf
from webapp_framework import dpop
import tailwind_tags as tw
from .chart_ui_cfg import CPT, addict_walker, get_baseCfgAttrMeta, update_chartCfg, FalseDict, update_cfgattrmeta
from .session_data import add_data

from .ui_styles import sty
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

    tlc = jp.Div(a=wp, classes=tw.tstr(*sty.tlc))
    session_id = request['session_id']
    refBoard = Dict()
    # =================== db for chart label input ===================
    labelsarea_ = wf.hc.Wrapdiv_(wf.register(refBoard, wf.hc.Textarea_("label", placeholder=pprint.pformat(sample_label),
                                                                       readonly=False)))
    labelpanel_ = wf.hc.Subsection_("enterChartLabel",
                                    "Enter horizontal (or x-) labels", labelsarea_)

    dbref_labelpanel = labelpanel_(tlc, "")

    # ============================== end =============================

    # ========================== chart data ==========================
    textarea_ = wf.hc.Wrapdiv_(wf.register(refBoard, wf.hc.Textarea_("data", placeholder=pprint.pformat(sample_data),
                                                                     readonly=False)))
    datapanel_ = wf.hc.Subsection_("enterChartData",
                                   "Enter chart/plot data", textarea_)

    dbref_datapanel = datapanel_(tlc, "")

    # ============================== end =============================

    # ========================= cfg entities =========================
    cfgAttrMeta = get_baseCfgAttrMeta()

    def cfggroup_iter():
        """
            iterator over attrmeta belonging to cfggroup CPT.initial
        """
        def is_in_group(kpath, attrmeta):
            if attrmeta.group == CPT.initial:  # TODO: should we filter based on is_active
                return True
            return False
        yield from filter(lambda _: is_in_group(_[0], _[1]), addict_walker(cfgAttrMeta))

    refBoard = Dict()
    refBoard_ = refBoard.initialcfg = Dict()
    uic_iter = wf.uic_iter("Initial config", cfggroup_iter(),
                           refBoard_)

    cfgpanel_ = wf.hc.StackW_("cfgpanel", cgens=uic_iter,
                              pcp=sty.cfgpanels.cfgpanel)

    def on_submit_click(dbref, msg):
        print("go  on ...build the chart")
        add_data(session_id, [cjs_cfg, ui_cfg, cfgAttrMeta])

        wp.redirect = "/configchart"

    submit_ = wf.hc.Wrapdiv_(wf.hc.Button_(
        "Submit",  "Submit", "Build Chart", on_submit_click))
    ic_ = wf.hc.StackV_(f'icInitialcfg',  cgens=[
        cfgpanel_, submit_], pcp=sty.infocard)
    controlpanel_ = wf.hc.Subsection_("chartInitialConfig",
                                      "Initial Config", ic_)
    dbref_controlpanel = controlpanel_(tlc, "")

    # ============================ configs ===========================
    cjs_cfg = Dict(track_changes=True)
    ui_cfg = Dict(track_changes=True)
    update_chartCfg(cfgAttrMeta, cjs_cfg, ui_cfg)
    cjs_cfg.clear_changed_history()  # don't care much for the change right now
    # ================= respond/react to user action =================
    wf.refresh(refBoard_)

    def update_ui_component():
        """
        update ui on ui state change;
        eventually this should be called update_ui only
        """
        wf.refresh(refBoard_)
        for kpath, attrmeta in cfggroup_iter():
            if attrmeta.active:
                if dget(cjs_cfg, kpath) != dget(refBoard_, kpath).val:
                    print(f"update chartcfg {kpath} ",
                          dget(refBoard_, kpath).val)
                    wf.dupdate(cjs_cfg, kpath, dget(refBoard_, kpath).val)
                    print([_ for _ in cjs_cfg.get_changed_history()])
        update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
        cjs_cfg.clear_changed_history()  # done with cjs changes

        for _ in cfgAttrMeta.get_changed_history():
            print("cfg attr changes = ", _)

        for kpath in cfgAttrMeta.get_changed_history():
            attrmeta = dget(cfgAttrMeta, kpath)
            refentry = dsearch(refBoard_, kpath)
            if not refentry:
                print(f"{kpath} is not rendered")
                continue
            dbref = dget(refBoard_, kpath)._go.target
            print("target dbref = ", dbref)
            if attrmeta.active and 'hidden' in dbref.classes:
                dbref.remove_class("hidden")
                print(kpath, " ", dbref.classes)
            elif not attrmeta.active and not 'hidden' in dbref.classes:
                dbref.set_class("hidden")
        cfgAttrMeta.clear_changed_history()
    wp.update_ui_component = update_ui_component
    return wp
