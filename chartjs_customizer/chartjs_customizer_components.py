import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

from addict import Dict
from .dpathutils import walker as dictWalker
import webapp_framework as wf
import webapp_framework_extn as wfx
# from . import attrmeta
from .cfgattr_uic import build_uic_iter
from itertools import chain
from .chartcfg import build_pltcfg
from justpy_chartjs import chartjscomponents as cj
from .attrmeta_basecfg_helper import is_visible
top_level_group = ["options/elements", "options/plugins", "options/scales"]
tier1_level_group = {"options/elements": ["line", "point"],
                     'options/plugins': ['legend'],
                     'options/scales': ['xaxes'],
                     "data": []}


def pltcanvas_(chartcfg: Dict):
    with wf.uictx("pltctx") as _ctx:
        cjs_plt_cfg = build_pltcfg(chartcfg)  # build chartjs compatible cfg
        pltcanvas_ = cj.ChartJS_(
            "pltcanvas", pcp=[], options=cjs_plt_cfg)  # build the chart
        _ctx.pltcanvas = pltcanvas_  # TODO: auto track canvas
    return pltcanvas_


def build_uigroup_blocks_(grouptag: str,   cfgattrmeta: Dict):
    """Builds a panel containing ui elements for cfg items  belonging
    to grouptag.
    ui_elemts are stacked in grid/auto-flow.  
    """

    # if user has specified multiple axes make groups for each one
    # tier1_level_group['options/scales'].append("xaxes/x1")

    def cfggroup_iter():
        """    iterator over attrmeta belonging to cfggroup
        """
        def is_in_group(kpath, attrmeta):
            if "/data/datasets" not in kpath:
                logger.debug(f"{kpath} is in group {grouptag}")
                return True  # for testing-- using all attributes
            # if attrmeta.group == grouptag:              #     return True
            # return False
        yield from filter(lambda _: is_in_group(_[0], _[1]),
                          filter(lambda _: is_visible(_[1]),
                                 dictWalker(cfgattrmeta)
                                 )
                          )

    def subgroup_iter(tlkey, tier1key=None):
        """
                tlkey/tier1key: defines a subgroup
                all cfg items in the subgroup
        """
        logger.debug("in subgroup iter")
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
                        logger.debug(f"{kpath} belongs to {tlkey}/{tier1key}")
                        return True
                    else:
                        return False  # kpath belongs to subcategory
                else:
                    if res > 0:
                        logger.debug(f"{kpath} belongs to {tlkey}/{tier1key}")
                        return True
                    else:
                        return False

        yield from filter(lambda _: is_in_subgroup(_[0]), cfggroup_iter())

    def build_ui_panel(tlkey, subkey=None):
        return wf.StackW_(tlkey, num_cols=2,
                          cgens=build_uic_iter(subgroup_iter(
                              tlkey, subkey),  # all cfgattr that come under options but not under elements or scales
                          )
                          )

    top_level_ui = Dict([(_, build_ui_panel(_)) for _ in top_level_group])
    tier1_level_ui = Dict()
    for tlkey in top_level_group:
        for subkey in tier1_level_group[tlkey]:
            subpanel_ = wf.Subsection_(
                f"{tlkey}_{subkey}",  f"{tlkey}/{subkey}", build_ui_panel(tlkey, subkey))
            tier1_level_ui[tlkey][subkey] = subpanel_

    def cfgblks_iter():
        for tlkey, tlui in top_level_ui.items():
            content_ = wf.StackV_(f"{tlkey}content", cgens=[tlui, wf.StackV_("subgroup", cgens=tier1_level_ui[tlkey].values())]
                                  )  # all the attr-uic for top level group k
            yield wf.Section_(f"{tlkey}panel", wf.HeadingBanner_(tlkey, tlkey),  content_)

    return cfgblks_iter()


def build_uigroup_panel_(grouptag: str,  chartcfg: Dict,  cfgattrmeta: Dict):

    @ wf.MRVWLR
    def on_submit_click(dbref, msg):
        rts = wf.TaskStack()
        rts.addTask(wf.ReactTag_UI.UpdateChart, None)
        return msg.page, rts
    submit_ = wf.Wrapdiv_(wf.Button_("Submit",  "Submit",
                          "Config Chart", on_submit_click))
    return wf.StackV_('topPanel',
                      cgens=chain.from_iterable(
                          [[pltcanvas_(chartcfg)], build_uigroup_blocks_(grouptag, cfgattrmeta), [submit_]])
                      )
