import os
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import pprint
from itertools import chain

import webapp_framework as wf
import webapp_framework_extn as wfx
# from .attrmeta import get_basecfg, uiorgCat, FalseDict
from .attrmeta_basecfg_helper import uiorgCat, FalseDict
from .attrmeta_basecfg import get_basecfg
from .cfgattr_uic import build_uic_iter
from addict import Dict, walker as dictWalker
if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict, refBoard

cfgAttrMeta = get_basecfg()


def cfgattr_groupInitial():
    """
        iterator over attrmeta belonging to uiorgCat.initial
    """
    def is_in_group(kpath, attrmeta):
        # if 'parsing' in kpath:
        #     logger.debug(f"typecheck {type(attrmeta.vrange)} ")
        # # if isinstance(attrmeta.vtype,  FalseDict):
        # if kpath in '/options/parsing/value':
        #     filter(lambda _: is_in_group(
        #         _[0], _[1]), dictWalker(attrmeta.vrange))
        # if 'parsing' in kpath:
        #    logger.debug(f"evaluation {kpath} {attrmeta} ")

        if attrmeta.group == uiorgCat.initial:  # TODO: should we filter based on is_active
            print("groupInitial ", kpath)
            return True

        return False
    yield from filter(lambda _: is_in_group(_[0], _[1]), dictWalker(cfgAttrMeta))


def on_submit_click(dbref, msg):
    print("go  on ...build the chart")


submit_ = wf.Wrapdiv_(wf.Button_(
    "Submit",  "Submit", "Build Chart", on_submit_click))


def no_action(dbref, msg):
    pass


uic_iter = build_uic_iter(cfgattr_groupInitial()
                          )

wf.Subsection_("cfghcs", "Initial Configuration",
               wf.StackW_("attrhc",
                          build_uic_iter(
                              cfgattr_groupInitial()
                          )
                          )
               )
wf.StackV_("topPanel", cgens=[
           stubStore.cfghcs, submit_])


with wf.uictx("scalesCtx") as _ctx:

    # context for line plot
    with wf.uictx("lineCtx") as _lctx:
        with wf.uictx("xyaxes") as _xyaxes:
            with wf.uictx("xcfgCtx")as _xctx:
                def no_action(dbref, msg):
                    print("btn clicked", msg.value, " ", dbref.key)
                    _xctx.deck.target.bring_to_front(msg.value)

                    pass
                with wf.uictx("xxctx") as _xxctx:
                    _tc = _xxctx
                    wf.StackH_(
                        "card", [wf.Span_("ph", "use the default x-axis")])
                    wf.Button_(
                        "btn", _tc.card, "X", no_action)
                with wf.uictx("xaxesctx") as _xaxesctx:
                    _tc = _xaxesctx
                    wf.StackH_(
                        "card", [wf.Span_("ph", "create multiple x-axes(TBD)")])
                    wf.Button_(
                        "btn", _tc.card, "XAxes", no_action)
                with wf.uictx("xcustomctx") as _xcustomctx:
                    _tc = _xcustomctx
                    wf.StackH_(
                        "card", [wf.Span_("ph", "create multiple custom x-axes(TBD)")])
                    wf.Button_(
                        "btn", _tc.card, "Design Custom Axes", no_action)

                wf.Decked_("deck", [_xxctx.card,
                                    _xaxesctx.card, _xcustomctx.card])

                wf.StackV_("panel", [wf.StackH_("btns", [_xxctx.btn, _xaxesctx.btn, _xcustomctx.btn]),
                                     _xctx.deck])
                wf.Subsection_("section", "Configure X scales", _xctx.panel)

            with wf.uictx("ycfgCtx")as _yctx:
                def no_action(dbref, msg):
                    print("btn clicked", msg.value, " ", dbref.key)
                    _yctx.deck.target.bring_to_front(msg.value)

                    pass
                with wf.uictx("yyctx") as _yyctx:
                    wf.StackH_(
                        "card", [wf.Span_("ph", "use the default y-axis")])
                    wf.Button_(
                        "btn", _yyctx.card, "Y", no_action)
                with wf.uictx("yaxesctx") as _yaxesctx:
                    _tc = _yaxesctx
                    wf.StackH_(
                        "card", [wf.Span_("ph", "create multiple y-axes(TBD)")])
                    wf.Button_(
                        "btn", _tc.card, "YAxes", no_action)
                with wf.uictx("ycustomctx") as _ycustomctx:
                    _tc = _ycustomctx
                    wf.StackH_(
                        "card", [wf.Span_("ph", "create multiple custom y-axes(TBD)")])
                    wf.Button_(
                        "btn", _tc.card, "Design Custom Axes", no_action)

                wf.Decked_("deck", [_yyctx.card,
                                    _yaxesctx.card, _ycustomctx.card])

                wf.StackV_("panel", [wf.StackH_("btns", [_yyctx.btn, _yaxesctx.btn, _ycustomctx.btn]),
                                     _yctx.deck])
                wf.Subsection_("section", "Configure Y scales", _yctx.panel)
            wf.StackH_("xy", [_xctx.section, _yctx.section])

    plottypes = [wf.Span_("noselection", "Select plot type to enable scale configuration"),
                 wf.Span_("line", "Show config option for line plot"),
                 wf.Span_("bar", "Show config option for bar plot"),
                 wf.Span_("radial", "Show config option for radial plot"),
                 wf.Span_("polar", "Show config option for polar plot")
                 ]
    wf.Decked_("deck", plottypes)
    # wf.Subsection_("panel", "Configure Scale", stubStore.deck)
