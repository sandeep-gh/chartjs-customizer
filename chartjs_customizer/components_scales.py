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
from .attrmeta_basecfg_helper import uiorgCat, FalseDict, CartesianAxesType
from .attrmeta_basecfg import get_basecfg
from .cfgattr_uic import build_uic_iter
from addict import Dict
from .dpathutils import walker as dictWalker
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


with wf.uictx("_scales") as _ctx:

    # context for line plot
    with wf.uictx("_lineplot") as _lctx:
        def lineplot_deck_action(dbref, msg):
            print("btn clicked", msg.value, " ", dbref.key)
            _lctx.deck.target.bring_to_front(msg.value)
            pass
        with wf.uictx("_xyaxes") as _xyaxesctx:
            _ctx = _xyaxesctx
            with wf.uictx("_xaxes")as _xctx:
                def no_action(dbref, msg):
                    print("btn clicked", msg.value, " ", dbref.key)
                    _xctx.deck.target.bring_to_front(msg.value)

                    pass
                with wf.uictx("_x") as _xxctx:
                    _ctx = _xxctx

                    def set_x(dbref, msg):
                        print("set choices to use default x")
                        pass
                    wf.StackH_(
                        "card", [wf.Button_("set", "x", "use the default x-axis", set_x)])

                with wf.uictx("_xaxes") as _xaxesctx:
                    _ctx = _xaxesctx

                    wf.TextInput_("id", "axes id", "new id")
                    wfx.EnumSelector_(
                        "axestype", CartesianAxesType, "Choose Axes Type")

                    def on_addaxesbtn_click(dbref, msg):
                        _lctx.scalesNoticeboard.showText("added new axes")
                    wf.Button_("addaxesbtn", "newid", "add axes")
                    wf.StackH_(
                        "card", [wf.StackV_("new axes", [_ctx.id, _ctx.axestype]), _ctx.addaxesbtn])

                # with wf.uictx("xcustomctx") as _xcustomctx:
                #     _tc = _xcustomctx
                #     wf.StackH_(
                #         "card", [wf.Span_("ph", "create multiple custom x-axes(TBD)")])
                #     wf.Button_(
                #         "btn", _tc.card, "Design Custom Axes", no_action)

                wf.Decked_("deck", [_xxctx.card,
                                    _xaxesctx.card])
                wf.Button_(
                    "xbtn", _xxctx.card, "X", no_action)
                wf.Button_(
                    "xaxesbtn", _xaxesctx.card, "XAxes", no_action)

                wf.StackV_("panel", [wf.StackH_("btns", [_xctx.xbtn, _xctx.xaxesbtn]),
                                     _xctx.deck])
                # exports
                wf.Subsection_("section", "Configure X scales", _xctx.panel)

            with wf.uictx("_yaxes")as _yctx:
                def no_action(dbref, msg):
                    print("btn clicked", msg.value, " ", dbref.key)
                    _yctx.deck.target.bring_to_front(msg.value)

                    pass
                with wf.uictx("_y") as _yyctx:
                    def set_y(dbref, msg):
                        print("sect choices to use default x")
                        pass
                    wf.StackH_(
                        "card", [wf.Button_("set", "y", "use the default x-axis", set_y)])

                with wf.uictx("_new") as _yaxesctx:
                    _ctx = _yaxesctx
                    # ========== ui to create several y-axes =========
                    wf.TextInput_("id", "axes id", "new id")
                    wfx.EnumSelector_(
                        "axestype", CartesianAxesType, "Choose Axes Type")
                    wf.Button_("addaxesbtn", "newid", "add axes")
                    wf.StackH_(
                        "card", [wf.StackV_("new axes", [_ctx.id, _ctx.axestype]), _ctx.addaxesbtn])

                    # ===================== done =====================

                wf.Decked_("deck", [_yyctx.card,
                                    _yaxesctx.card])
                wf.Button_(
                    "ybtn", _yyctx.card, "Y", no_action)
                wf.Button_(
                    "yaxesbtn", _yaxesctx.card, "YAxes", no_action)
                wf.StackV_("panel", [wf.StackH_("btns", [_yctx.ybtn, _yctx.yaxesbtn]),
                                     _yctx.deck])
                wf.Subsection_("section", "Configure Y scales", _yctx.panel)
            wf.StackH_("card", [_xctx.section, _yctx.section])
            wf.Button_(
                "btn", _xyaxesctx.card, "Use XY Axes", lineplot_deck_action)

        with wf.uictx("_custom") as _customctx:
            _ctx = _customctx
            wf.StackH_(
                "card", [wf.Span_("ph", "create multiple custom axes(TBD)")])
            wf.Button_(
                "btn", _ctx.card, "Design Custom Axes", lineplot_deck_action)
        wf.Decked_("deck", [_xyaxesctx.card,
                            _customctx.card])
        wf.StackV_("panel", [wf.StackH_("btns", [_xyaxesctx.btn, _customctx.btn]),
                             _lctx.deck])

    with wf.uictx("_plottype") as _ctx:
        plottypes = [wf.Span_("noselection", "Select plot type to enable scale configuration"),
                     wf.Span_("line", "Show config option for line plot"),
                     wf.Span_("bar", "Show config option for bar plot"),
                     wf.Span_("radial", "Show config option for radial plot"),
                     wf.Span_("polar", "Show config option for polar plot")
                     ]
        wf.Decked_("deck", plottypes)
    # wf.Subsection_("panel", "Configure Scale", stubStore.deck)

    wfx.Noticebord_("scalesNoticeBoard")
