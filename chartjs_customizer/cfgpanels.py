#from framework_looprunner import MRVWLR
#from taskstack import TaskStack
#from frontendreactactiontag import FrontendReactActionTag
import logging
import json
from dpath.util import get as dget
from addict import Dict
from webapp_framework import dur, dc, dbr, heading__gen
from justpy_chartjs.tags import cfg_template as ct
from chartcfg_builder import cfg, chartcfg
import ui_styles
from tailwind_tags import bg, pink, jc


def no_action(dbref, msg):
    pass


top_level_group = ["options", "data"]
tier1_level_group = {"options": ["elements", "scales/xAxis", "scales/yAxis"],
                     "data": []}


def build_cfgpanel_(cfgtype):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def cfgattr_iter(cfgtype):
        for kpath, cfgattr in ct.walker(cfg):
            #print ("cfgattr_iter : ", kpath, " ", cfgattr)

            if "/data/datasets" not in kpath:

                if cfgattr.decor_type.value == cfgtype:
                    yield (kpath, cfgattr)

    def get_input_ui(kpath, key,  cfgattr):
        if cfgattr.vtype == int:
            if cfgattr.vrange == int:
                return dc.TextInput_(kpath, key, cfgattr.default, no_action)
                # need int input

            if isinstance(cfgattr.vrange, list):
                # need select input
                return None

        if cfgattr.vtype == str:
            if cfgattr.vrange == str:
                # need int input
                return dc.TextInput_(kpath, key, cfgattr.default, no_action, pcp=[])
                pass
            if isinstance(cfgattr.vrange, list):
                # need select input
                return None
                pass
            print("unkown type ", kpath, cfgattr)

        if cfgattr.vtype == float:
            if cfgattr.vrange == float:
                # need int input
                return dc.TextInput_(kpath, key, cfgattr.default, no_action)
                pass
            if isinstance(cfgattr.vrange, list):
                # need select input
                return None

        if cfgattr.vtype == ct.Color:
            def getValue(dbref_stackv, kpath=kpath):
                dbref_cs = dbref_stackv.getItem(kpath)
                return dbref_cs.getValue()
            return dbr.ColorSelectorWBanner_(kpath, pcp=[jc.center])

        if cfgattr.vtype == bool:
            return dur.wrapdiv_(kpath+"Wrap", dc.ToggleBtn_(kpath, key))
            pass
        return None

    def cfg_category_iter(tlkey, tier1key=None):
        if tier1key is None:
            tier1keys = tier1_level_group[tlkey]
        else:
            tier1keys = [tier1key]

        def filter_by_category(kpath):
            """
            check if kpath belongs to tlkey/tier1key
            """
            if tlkey in kpath:
                res = len([True for _ in tier1keys if _ in kpath])
                if tier1key is not None:
                    if res > 0:
                        return True
                else:
                    if res == 0:
                        return True
            return False
        yield from filter(lambda _: filter_by_category(_[0]), cfgattr_iter(cfgtype))

    def ui_iter_for_cfgcategory(tlkey, tier1key=None):
        headingkey = tlkey
        if tier1key is not None:
            headingkey = tlkey + "/" + tier1key
        yield dur.wrapdiv_(headingkey+"Wrap", dc.Span_(headingkey, headingkey, pcp=[bg/pink/1]))

        def build_ui_cfgattr(kpath, cfgattr):
            _ = kpath.split("/")
            return get_input_ui(kpath, _[-2]+"/"+_[-1], cfgattr)
        yield from filter(lambda _: _ is not None,
                          map(lambda _: build_ui_cfgattr(_[0], _[1]),
                              cfg_category_iter(tlkey, tier1key))
                          )

    top_level_ui = {"options": dc.StackV_("options", ui_iter_for_cfgcategory(
        "options", None), pcp=ui_styles.cfgpanels.options), "data": dc.StackV_("data")}
    tier1_level_ui = {"options":
                      {  # "elements": dc.StackV_("options/elements", ui_iter_for_cfgcategory("options", "elements"), pcp=ui_styles.cfgpanels.options_child),
                          "scales/xAxis": dc.StackV_("options/scales/xAxis", ui_iter_for_cfgcategory("options", "scales/xAxis"), pcp=ui_styles.cfgpanels.options_child),
                          "scales/yAxis": dc.StackV_("options/scales/yAxis", ui_iter_for_cfgcategory("options", "scales/yAxis"), pcp=ui_styles.cfgpanels.options_child)
                      },
                      "data": {}
                      }

    def cfgblks_iter():
        for k, v in top_level_ui.items():

            yield v
            for kk, vv in tier1_level_ui[k].items():

                yield vv

    def cfgtype_iter(dbref_cfgpanel):
        """
        builds iterator over keys in cfgtype
        """
        for catkey in top_level_ui.keys():
            dbref_tlc = dbref_cfgpanel.getItem(catkey)
            for _ in cfg_category_iter(catkey, None):
                dbref_ce = dbref_tlc.getItem(_[0])
                yield (_[0], dbref_ce)
            for subcatkey in tier1_level_ui[catkey].keys():
                dbref_t1c = dbref_cfgpanel.getItem(catkey + "/" + subcatkey)
                for _ in cfg_category_iter(catkey, subcatkey):
                    dbref_ce = dbref_t1c.getItem(_[0])
                    yield (_[0], dbref_ce)

    def on_submit_click(dbref, msg):
        print("on submit click")
        dbref_ic = dbref.ediv
        dbref_cfgpanel = dbref_ic.getItem("cfgpanel")
        print("cfgpanel = ", dbref_cfgpanel)
        for _ in cfgtype_iter(dbref_cfgpanel):
            print(_[1])
            print(_[1].getValue())

    heading_ = heading__gen("Required configs")
    cfgblks_ = dc.StackG_("cfgpanel", cgens=cfgblks_iter(),
                          pcp=ui_styles.cfgpanels.cfgpanel)
    submit_ = dur.divbutton_(
        f"{cfgtype}Submit",  f"{cfgtype}_submit", "submit", on_submit_click)

    ic_ = dc.Infocard_(f'ic{cfgtype}',  cgens=[
                       heading_, cfgblks_, submit_], pcp=ui_styles.cfgpanels.infocard)
    return ic_
