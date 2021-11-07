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
import webapp_framework as wf
from justpy_chartjs.tags import cfg_template as ct
from chartcfg_builder import cfg
import ui_styles
from tailwind_tags import bg, pink, jc, db, jc, mr


def no_action(dbref, msg):
    pass


top_level_group = ["options", "data"]
tier1_level_group = {"options": ["elements"],
                     "data": []}


def build_cfgpanel_(cfgtype, chartcfg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    refBoard = Dict()

    def cfgattr_iter(cfgtype):
        """
        iter over cfgattr in cfg restricted to cfgtype
        """
        for kpath, cfgattr in ct.walker(cfg):

            if "/data/datasets" not in kpath:

                if cfgattr.decor_type.value == cfgtype:
                    yield (kpath, cfgattr)

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

    top_level_ui = {"options":
                    wf.register(refBoard,
                                wf.fc.StackV_("options",
                                              wf.uic_iter("options",
                                                          cfg_category_iter(
                                                              "options", None),
                                                          refBoard
                                                          ),
                                              pcp=ui_styles.cfgpanels.options
                                              )
                                )
                    }
    tier1_level_ui = {"options":
                      {"elements": dc.StackV_("options/elements",
                                              wf.uic_iter("options/elements",
                                                          cfg_category_iter(
                                                              "options", "elements"),
                                                          refBoard),
                                              pcp=ui_styles.cfgpanels.options_child
                                              )
                       }
                      }

    def cfgblks_iter():
        for k, v in top_level_ui.items():

            yield v
            for kk, vv in tier1_level_ui[k].items():

                yield vv

    def on_submit_click(dbref, msg):
        pass

    heading_ = heading__gen(f"Configure Chart: {cfgtype} config")
    cfgblks_ = dc.StackG_("cfgpanel", cgens=cfgblks_iter(),
                          pcp=ui_styles.cfgpanels.cfgpanel)
    submit_ = dur.divbutton_(
        f"{cfgtype}Submit",  f"{cfgtype}_submit", "submit", on_submit_click)

    ic_ = dc.Infocard_(f'ic{cfgtype}',  cgens=[
        heading_, cfgblks_, submit_], pcp=ui_styles.cfgpanels.infocard)

    return ic_
