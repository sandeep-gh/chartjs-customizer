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
from . import ui_styles
from tailwind_tags import bg, pink, jc, db, jc, mr
from .chart_ui_cfg import addict_walker
top_level_group = ["options"]
tier1_level_group = {"options": ["elements"],
                     "data": []}


# def uic_iter(label, attrmetaIter, refBoard):
#     """
#     label: group or subgroup label
#     """
#     for attrmeta in attrmetaIter:
#         print(attrmeta)
#     return []  # don't draw anything yet


def cfggroup_panel_(grouptag,  chartcfg, uicfg, refBoard_):
    # =========================== begin ==========================
    dbrefBoard = Dict()

    def cfggroup_iter():
        """
        iterator over attrmeta belonging to cfggroup
        """
        def is_in_group(kpath, attrmeta):
            if "/data/datasets" not in kpath:
                return True  # testing for all
                if attrmeta.group == grouptag:  # TODO: should we filter based on is_active
                    return True
            return False
        #
        yield from filter(lambda _: is_in_group(_[0], _[1]), addict_walker(uicfg))
    # =========================== end ===========================

    def subgroup_iter(tlkey, tier1key=None):
        """
                tlkey/tier1key: defines a subgroup
        """
        if tier1key is None:
            tier1keys = tier1_level_group[tlkey]
        else:
            tier1keys = [tier1key]

        def is_in_subgroup(kpath):
            """
            check if kpath belongs to group defined by tlkey/tier1key
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

        yield from filter(lambda _: is_in_subgroup(_[0]), cfggroup_iter())
    # ============================ end ===========================
    top_level_ui = {"options":
                    wf.register(dbrefBoard,
                                wf.fc.StackV_("options",
                                              wf.uic_iter("options",
                                                          subgroup_iter(
                                                              "options", None),
                                                          refBoard_
                                                          ),
                                              pcp=ui_styles.cfgpanels.options
                                              )
                                )
                    }
    tier1_level_ui = {"options":
                      {"elements": wf.register(dbrefBoard,
                                               wf.fc.StackV_("options/elements",
                                                             wf.uic_iter("options/elements",
                                                                         subgroup_iter(
                                                                             "options", "elements"),
                                                                         refBoard_),
                                                             pcp=ui_styles.cfgpanels.options_child
                                                             )
                                               )
                       }
                      }

    def cfgblks_iter():
        for k, v in top_level_ui.items():

            yield v
            for kk, vv in tier1_level_ui[k].items():

                yield vv

    def on_submit_click(dbref, msg):
        rts = TaskStack()
        rts.addTask(FrontendReactActionTag.UpdateChart, None)
        pass
    heading_ = heading__gen(
        f"Configure Chart: {grouptag.value} chart config options")
    cfgblks_ = dc.StackG_("cfgpanel", cgens=cfgblks_iter(),
                          pcp=ui_styles.cfgpanels.cfgpanel)
    submit_ = dur.divbutton_(
        f"{grouptag.value}Submit",  f"{grouptag.value}submit", "submit", on_submit_click)
    ic_ = dc.Infocard_(f'ic{grouptag.value}',  cgens=[
        heading_, cfgblks_, submit_], pcp=ui_styles.cfgpanels.infocard)
    return ic_
