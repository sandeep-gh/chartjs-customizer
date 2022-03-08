import logging
from addict import Dict, walker as dictWalker
import webapp_framework as wf
import webapp_framework_extn as wfx
from . import attrmeta
from .cfgattr_uic import build_uic_iter
from itertools import chain

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
top_level_group = ["options"]
tier1_level_group = {"options": ["elements", "scales"],
                     "data": []}


def cfggroup_panel_(grouptag: str,  chartcfg: Dict, cfgattrmeta: Dict):
    """Builds a Section/Subsection containing ui elements for cfgattrmeta belonging
    to grouptag.
    ui_elemts are stacked in grid/auto-flow.  Within the grid, they are grouped by attrmetaclass(simple/simplemore/etc.)
    """
    logger.debug("In cfggroup_panel_")

    def cfggroup_iter():
        """    iterator over attrmeta belonging to cfggroup
        """
        logger.debug("in group iter")

        def is_in_group(kpath, attrmeta):
            if "/data/datasets" not in kpath:
                return True  # for testing-- using all attributes
            # if attrmeta.group == grouptag:              #     return True
            # return False

        yield from filter(lambda _: is_in_group(_[0], _[1]),
                          filter(lambda _: attrmeta.is_visible(_[1]),
                                 dictWalker(cfgattrmeta)
                                 )
                          )

    def subgroup_iter(tlkey, tier1key=None):
        """
                tlkey/tier1key: defines a subgroup
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
            logger.debug(f"check if {kpath} belongs to {tlkey}")
            if tlkey in kpath:
                res = len([True for _ in tier1keys if _ in kpath])
                logger.debug(f"check1: {res}")
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

    top_level_ui = {"options":
                    wf.StackW_("options", num_cols=2,
                               cgens=build_uic_iter(subgroup_iter(
                                   "options", None),  # all cfgattr that come under options but not under elements or scales
                               )
                               )

                    }
    tier1_level_ui = Dict()

    for key in top_level_group:
        for kk in tier1_level_group[key]:
            kk_panel = wf.Subsection_(f"{key}_{kk}", f"{key}/{kk}",
                                      wf.StackW_(f"{key}/{kk}",
                                                 cgens=build_uic_iter(
                                                     subgroup_iter(
                                                         f"{key}", f"{kk}")
                                                 )
                                                 )
                                      )
            tier1_level_ui[key][kk] = kk_panel

    def cfgblks_iter():
        logger.debug("in cfgblks iter")
        for k, v in top_level_ui.items():
            with wf.uictx(f"{k}Ctx") as _ctx:
                def subgroup_ui():
                    for k, v in tier1_level_ui[key].items():
                        yield v
                wf.StackV_("content", cgens=[v, wf.StackV_("subgroup", cgens=subgroup_ui())]
                           )
                yield wf.Section_("panel", wf.HeadingBanner_(k, k), _ctx.content)

            # yield v

    # ============================ end ===========================
    with wf.uictx(f"uiorg_{grouptag.value}") as _ctx:
        wfx.Noticebord_("noticeboard")
        # wf.StackV_("cfgpanel", cgens=cfgblks_iter())

        @wf.MRVWLR
        def on_submit_click(dbref, msg):
            rts = wf.TaskStack()
            rts.addTask(wf.ReactTag_UI.UpdateChart, None)
            return msg.page, rts
        submit_ = wf.Wrapdiv_(wf.Button_(
            "Submit",  "Submit", "Config Chart", on_submit_click))
        wf.StackV_('topPanel',  cgens=chain.from_iterable([cfgblks_iter(), [submit_]]),
                   )
