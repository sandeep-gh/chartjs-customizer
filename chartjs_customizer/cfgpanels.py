#from framework_looprunner import MRVWLR
#from taskstack import TaskStack
#from frontendreactactiontag import FrontendReactActionTag
import logging
import json
from dpath.util import get as dget
from dpath.util import set as dset
import jsbeautifier
from addict import Dict
from webapp_framework import dur, dc, dbr, heading__gen
from webapp_framework import MRVWLR, TaskStack, FrontendReactActionTag
from justpy_chartjs.tags import cfg_template as ct
from chartcfg_builder import cfg
import ui_styles
from tailwind_tags import bg, pink, jc, db, jc, mr


def no_action(dbref, msg):
    pass


top_level_group = ["options", "data"]
tier1_level_group = {"options": ["elements", "scales/xAxis", "scales/yAxis"],
                     "data": []}


def build_cfgpanel_(cfgtype, chartcfg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def cfgattr_iter(cfgtype):
        """
        iter over cfgattr in cfg restricted to cfgtype
        """
        for kpath, cfgattr in ct.walker(cfg):

            if "/data/datasets" not in kpath:

                if cfgattr.decor_type.value == cfgtype:
                    yield (kpath, cfgattr)

    def get_input_ui(kpath, key,  cfgattr):
        default_val = dget(chartcfg, kpath)
        match str(cfgattr.vtype):
            case "<class 'int'>":

                match cfgattr.vrange:
                    case type():
                        return dc.TextInput_(kpath, key, cfgattr.default, no_action)
                    case[x, y]:
                        return dur.wrapdiv_(kpath+"Wrap",
                                            dbr.WithBanner_(
                                                kpath, dc.Slider_(kpath, range(
                                                    x, y), cfgattr.default), key,
                                            ), [db.f, jc.center, mr/2]
                                            )

                    case _:
                        print("skipping ", kpath)
                        return None  # not handling multi-attribute ranges

            case "<class 'str'>":
                match cfgattr.vrange:
                    case type():
                        return dc.TextInput_(kpath, key, default_val, no_action, pcp=[])
                    case[x, y]:
                        print("skipping str", kpath)
                        return None
                    case _:
                        print("skipping str", kpath)
                        return None
            case "<class 'float'>":
                match cfgattr.vrange:
                    case type():
                        return dc.TextInput_(kpath, key, default_val, no_action, pcp=[])
                    case[x, y]:
                        print("skipping float", kpath)
                        return None
                    case _:
                        print("skipping float", kpath)
                        return None

            case "<aenum 'Color'>":
                return dbr.ColorSelectorWBanner_(kpath, key, pcp=[jc.center])

            case "<class 'bool'>":
                return dur.wrapdiv_(kpath+"Wrap", dc.ToggleBtn_(kpath, key, value=default_val))
            case "<aenum 'Position'>":
                return dur.wrapdiv_(kpath+"Wrap", dbr.SelectorWBanner_(kpath, key,
                                                                       options=[
                                                                           _.value for _ in cfgattr.vtype],
                                                                       values=[_.value for _ in cfgattr.vtype], on_select=no_action)
                                    )
        print("skipping ", kpath)
        return None

    def cfg_category_iter(tlkey, tier1key=None):
        if tier1key is None:
            tier1keys = tier1_level_group[tlkey]
        else:
            tier1keys = [tier1key]

        def is_in_category(kpath):
            """
            check if kpath belongs to tlkey/tier1key
            """
            if tlkey in kpath:
                res = len([True for _ in tier1keys if _ in kpath])
                if tier1key is None:
                    if res == 0:
                        return True
                    else:
                        return False  # kpath belongs to subcategory
                else:
                    if res > 0:
                        return True
                    else:
                        return False

        yield from filter(lambda _: is_in_category(_[0]), cfgattr_iter(cfgtype))

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
                      {"elements": dc.StackV_("options/elements", ui_iter_for_cfgcategory("options", "elements"), pcp=ui_styles.cfgpanels.options_child),
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
                dbref_ce = dbref_tlc.getItemUnwrapped(_[0])
                yield (_[0], dbref_ce)
            for subcatkey in tier1_level_ui[catkey].keys():
                dbref_t1c = dbref_cfgpanel.getItem(catkey + "/" + subcatkey)
                for _ in cfg_category_iter(catkey, subcatkey):
                    dbref_ce = dbref_t1c.getItemUnwrapped(_[0])
                    yield (_[0], dbref_ce)

    @MRVWLR
    def on_submit_click(dbref, msg):
        print("on submit click")
        dbref_ic = dbref.get_tlw().ediv
        print("dbref_ic = ", dbref_ic)
        dbref_cfgpanel = dbref_ic.getItem("cfgpanel")
        print("cfgpanel = ", dbref_cfgpanel)
        for _ in cfgtype_iter(dbref_cfgpanel):
            kpath, kdbref = _  # kdbref: the dbref corresponding to kpath
            # edit chartcfg
            print(_)
            kval = kdbref.getValue()
            print(kpath, kdbref, kval)
            if kval != "" or kval is not None:
                dset(chartcfg, kpath, kval)

        opts = jsbeautifier.default_options()
        res = jsbeautifier.beautify(json.dumps(chartcfg), opts)
        # print(res)
        rts = TaskStack()
        rts.addTask(FrontendReactActionTag.UpdateChart, Dict({'chartcfg':
                                                              chartcfg}))
        return msg.page, rts

    heading_ = heading__gen(f"Configure Chart: {cfgtype} config")
    cfgblks_ = dc.StackG_("cfgpanel", cgens=cfgblks_iter(),
                          pcp=ui_styles.cfgpanels.cfgpanel)
    submit_ = dur.divbutton_(
        f"{cfgtype}Submit",  f"{cfgtype}_submit", "submit", on_submit_click)

    ic_ = dc.Infocard_(f'ic{cfgtype}',  cgens=[
                       heading_, cfgblks_, submit_], pcp=ui_styles.cfgpanels.infocard)

    return ic_
