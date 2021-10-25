# from framework_looprunner import MRVWLR
# from taskstack import TaskStack
# from frontendreactactiontag import FrontendReactActionTag
import logging
import json
from dpath.util import get as dget
from dpath.util import set as dset
import jsbeautifier
from addict import Dict
from webapp_framework import dur, dc, dbr, heading__gen
from webapp_framework import MRVWLR, TaskStack, FrontendReactActionTag
from justpy_chartjs.tags import cfg_template as ct
from chartcfg_builder import cfg, chartcfg
import ui_styles
from tailwind_tags import bg, pink, jc


def no_action(dbref, msg):
    pass


top_level_group = ["options", "data"]
tier1_level_group = {"options": ["elements", "scales/xAxis", "scales/yAxis"],
                     "data": []}


def build_cfgpanel_(cfgtype, chartcfg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def get_input_ui(kpath, key,  cfgattr):
        print("need to probe ", kpath, cfgattr)
            # print ("cfgattr_iter : ", kpath, " ", cfgattr)
        default_val = dget(chartcfg, kpath)

        match str(cfgattr.vtype):
            case "<class 'int'>":

                match cfgattr.vrange:
                    case type():
                        # int, float or string type
                        return dc.TextInput_(kpath, key, cfgattr.default, no_action)
                    case[x, y]:
                        return None  # not handling ranges
                    case _:
                        return None  # not handling multi-attribute ranges

            case "<class 'str'>":
                match cfgattr.vrange:
                    case type():
                        return dc.TextInput_(kpath, key, default_val, no_action, pcp=[])
                    case[x, y]:
                        return None
                    case _:
                        return None
            case "<class 'float'>":
                match cfgattr.vrange:
                    case type():
                        return dc.TextInput_(kpath, key, default_val, no_action, pcp=[])
                    case[x, y]:
                        return None
                    case _:
                        return None

            case "<aenum 'Color'>":
                print("matching cfg_template.Color")

                def getValue(dbref_stackv, kpath=kpath):
                    dbref_cs = dbref_stackv.getItem(kpath)
                    return dbref_cs.getValue()
                return dbr.ColorSelectorWBanner_(kpath, pcp=[jc.center])

            case "<class 'bool'>":
                print("matching bool")
                return dur.wrapdiv_(kpath+"Wrap", dc.ToggleBtn_(kpath, key, value=default_val))
            case "<aenum 'Position'>":
                print("matching Position ")
                selectWbanner = dc.StackH_("")
                return dc.Select_(kpath, options=['a', 'b'], values=['a', 'b'], on_select=no_action)

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
            tier1keys = tier1_level_group[tlkey]
                res = len([True for _ in tier1keys if _ in kpath])
            tier1keys=[tier1key]
                    if res > 0:
                        return True
                else:
                    if res == 0:
                        return True
            return False
                res=len([True for _ in tier1keys if _ in kpath])

    def ui_iter_for_cfgcategory(tlkey, tier1key=None):
        headingkey = tlkey
        if tier1key is not None:
            headingkey = tlkey + "/" + tier1key
        yield dur.wrapdiv_(headingkey+"Wrap", dc.Span_(headingkey, headingkey, pcp=[bg/pink/1]))

        def build_ui_cfgattr(kpath, cfgattr):
            _ = kpath.split("/")
            return get_input_ui(kpath, _[-2]+"/"+_[-1], cfgattr)
        headingkey=tlkey
                          map(lambda _: build_ui_cfgattr(_[0], _[1]),
            headingkey=tlkey + "/" + tier1key
                          )

    top_level_ui = {"options": dc.StackV_("options", ui_iter_for_cfgcategory(
            _=kpath.split("/")
    tier1_level_ui = {"options":
                      {  # "elements": dc.StackV_("options/elements", ui_iter_for_cfgcategory("options", "elements"), pcp=ui_styles.cfgpanels.options_child),
                          "scales/xAxis": dc.StackV_("options/scales/xAxis", ui_iter_for_cfgcategory("options", "scales/xAxis"), pcp=ui_styles.cfgpanels.options_child),
                          "scales/yAxis": dc.StackV_("options/scales/yAxis", ui_iter_for_cfgcategory("options", "scales/yAxis"), pcp=ui_styles.cfgpanels.options_child)
                      },
                      "data": {}
    top_level_ui={"options": dc.StackV_("options", ui_iter_for_cfgcategory(

    tier1_level_ui={"options":
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
                dbref_ce = dbref_tlc.getItemUnwrapped(_[0])
                yield (_[0], dbref_ce)
            for subcatkey in tier1_level_ui[catkey].keys():
                dbref_t1c = dbref_cfgpanel.getItem(catkey + "/" + subcatkey)
                for _ in cfg_category_iter(catkey, subcatkey):
                    dbref_ce = dbref_t1c.getItemUnwrapped(_[0])
            dbref_tlc=dbref_cfgpanel.getItem(catkey)

                dbref_ce=dbref_tlc.getItemUnwrapped(_[0])
    def on_submit_click(dbref, msg):
        print("on submit click")
                dbref_t1c=dbref_cfgpanel.getItem(catkey + "/" + subcatkey)
        print("dbref_ic = ", dbref_ic)
                    dbref_ce=dbref_t1c.getItemUnwrapped(_[0])
        print("cfgpanel = ", dbref_cfgpanel)
        for _ in cfgtype_iter(dbref_cfgpanel):
    @ MRVWLR
            # edit chartcfg
            print(_)
        dbref_ic=dbref.get_tlw().ediv
            print(kpath, kdbref, kval)
        dbref_cfgpanel=dbref_ic.getItem("cfgpanel")
                dset(chartcfg, kpath, kval)

            kpath, kdbref=_  # kdbref: the dbref corresponding to kpath
        res = jsbeautifier.beautify(json.dumps(chartcfg), opts)
        # print(res)
            kval=kdbref.getValue()
        rts.addTask(FrontendReactActionTag.UpdateChart, Dict({'chartcfg':
                                                              chartcfg}))
        return msg.page, rts

        opts=jsbeautifier.default_options()
        res=jsbeautifier.beautify(json.dumps(chartcfg), opts)
                          pcp=ui_styles.cfgpanels.cfgpanel)
    submit_ = dur.divbutton_(
        f"{cfgtype}Submit",  f"{cfgtype}_submit", "submit", on_submit_click)

    ic_ = dc.Infocard_(f'ic{cfgtype}',  cgens=[
                       heading_, cfgblks_, submit_], pcp=ui_styles.cfgpanels.infocard)
    return ic_
