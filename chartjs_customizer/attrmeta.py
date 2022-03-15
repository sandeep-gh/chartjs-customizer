"""
attrmeta is a graball module for all metadata about chartjs attributes 
"""
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

from typing import NamedTuple, Any
from addict import Dict, walker as dictWalker
from aenum import Enum, auto
from dpath.util import get as dget, set as dset, new as dnew, delete as dpop
from justpy_chartjs.tags.style_values import Align, Position
from justpy_chartjs.tags.style_values import Axis
import webapp_framework as wf
import tailwind_tags as twt
from tailwind_tags import color2hex as hexify


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    vtype: Any
    vrange: Any
    group: Any
    active: Any
    context: Any  # describes all scenarios when attribute is active


class uiorgCat(Enum):
    """attrmeta belongs to one of the categories
    """
    simple = "simple"
    simplemore = "simplemore"
    nitpick = "nitpick"
    ocd = "ocd"
    perf = "perf"
    config = "config"
    advanced = "advanced"
    required = "required"
    TBD = "tbd"
    ninja = "ninja"
    initial = "initial"
    all = "all"


class PlotType(Enum):
    Line = "line"
    Bar = "bar"
    Scatter = "scatter"
    Bubble = "bubble"
    Undef = None


class Color(Enum):
    pass


class FalseDict(Enum):
    """
    value is either False or a dict
    """
    pass


def get_basecfg():
    """generate canonical attrmeta
    """
    all_context = [('*', '*')]
    _base = cfgAttrMeta_base = Dict(track_changes=True)
    _base.type = AttrMeta(PlotType.Undef, PlotType,
                          PlotType, uiorgCat.initial, True, all_context)
    _base.options.responsive = AttrMeta(
        True, bool, bool, uiorgCat.perf, True, all_context)
    _base.options.aspectRatio = AttrMeta(
        2, int, [1, 4], uiorgCat.advanced, True, all_context)
    _base.options.resizeDelay = AttrMeta(
        4, int, [1, 9], uiorgCat.perf, True, all_context)
    _base.options.devicePixelRatio = AttrMeta(
        1, int, [1, 5], uiorgCat.advanced, True, all_context)

    _base.options.parsing.value = AttrMeta(False, FalseDict,
                                           Dict({'x': AttrMeta('x', str, str, uiorgCat.initial,
                                                               False, [('/options/parsing/', True)]),
                                                 'y': AttrMeta('y', str, str,  uiorgCat.initial, False, [('/options/parsing/', True)]),
                                                 'id': AttrMeta('id', str, str, uiorgCat.initial, False, [('/options/parsing/', True)])
                                                 }), uiorgCat.initial, True, all_context)

    _base.options.parsing.x = AttrMeta(
        'x', str, str, uiorgCat.initial, False, [('options/parsing', True)])  # active only if /options/parsing is True
    _base.options.parsing.y = AttrMeta(
        'y', str, str, uiorgCat.initial, False, [('options/parsing', True)])
    _base.options.parsing.id = AttrMeta('id', str, str, uiorgCat.initial, False, [
        ('options/parsing', 'True')])

    # _base.options.plugins = Dict()
    # _base.options.plugins.legend = Dict()
    _base.options.plugins.legend.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simplemore, True, all_context)

    # _base.options.plugins.title = Dict()
    _base.options.plugins.title.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, all_context)
    _base.options.plugins.title.text = AttrMeta(
        "plot_title", str, str, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])

    # ========================= elements/line ========================

    #TODO: bug in addict
    #_base.options.elements = Dict(track_changes=True)
    #_ = _base.options.elements.line = Dict(track_changes=True)
    # _.tension = AttrMeta(0, float, [0, 1], uiorgCat.advanced, True, [
    # ('/type', 'line')])
    _base.options.elements.line.tension = AttrMeta(0, float, [0, 1], uiorgCat.advanced, True, [
        ('/type', 'line')])
    _ = _base.options.elements.line
    _.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, True, [('/type', 'line')])
    _.borderWidth = AttrMeta(
        2, int, [0, 5], uiorgCat.simple, True, [('/type', 'line')])
    _.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simple,  True, [('/type', 'line')])
    _.borderCapStyle = AttrMeta(
        "butt", None, None, uiorgCat.TBD, False, [('/type', 'line')])
    _.borderDash = AttrMeta([], None, None, uiorgCat.TBD,
                            False, [('/type', 'line')])
    _.borderDashOffset = AttrMeta(
        0.0, None, None, uiorgCat.TBD, False, [('/type', 'line')])
    _.borderJoinStyle = AttrMeta(
        "miter", None, None, uiorgCat.TBD, False, [('/type', 'line')])
    _.capBezierPoints = AttrMeta(
        True, bool, bool, uiorgCat.advanced, False, [('/type', 'line')])
    _.cubicInterpolationMode = AttrMeta(
        "default", None, None, uiorgCat.TBD, False, [('/type', 'line')])
    _.fill = AttrMeta(None, None, None, uiorgCat.TBD,
                      False, [('/type', 'line')])
    _.stepped = AttrMeta(None, None, None, uiorgCat.TBD,
                         False, [('/type', 'line')])
    # ============================ end elements/line===========================

    _xAxis = _base.options.scales.xAxis
    # _xAxis.grid = Dict()  # TBD
    _xAxis.grid.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/type', 'line')])
    _xAxis.grid.color = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simplemore, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.tickColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simplemore, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.circular = AttrMeta(
        None, None, None, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])  # from for radar chart

    return _base

# ==================== end get_baseCfgAttrMeta ===================


def get_defaultVal(attrmeta):  # TODO: ask SO if there is a better way to
    '''get default value of attrmeta
    '''
    cam = attrmeta
    match str(cam.vtype):
        case "<class 'int'>" | "<class 'bool'>" | "<class 'str'>" | "<class 'float'>":

            return cam.default

        case "<aenum 'FalseDict'>":
            return cam.default

        case "<aenum 'Position'>" | "<aenum 'PlotType'>":
            return cam.default.value

        case "<aenum 'Color'>":
            return hexify(cam.default)  # TODO: will deal with later

        case _:
            print("unkown vtype :", cam)
            raise ValueError


def attrupdate(cfgattrmeta, kpath, active):
    logger.debug(f"attrupdate {kpath} {active} {bool(active)}g")
    attrmeta = dget(cfgattrmeta, kpath)
    attrmeta = attrmeta._replace(active=bool(active))
    wf.dupdate(cfgattrmeta, kpath, attrmeta)


def attradd(cfgattrmeta, kpath, metaval):
    dnew(cfgattrmeta, kpath, metaval)


def is_visible(attrmeta):
    if attrmeta.vtype != None:
        if attrmeta.group != uiorgCat.TBD:
            return True
    return False


def attrmeta_in_context(ctx, cfgattrmeta):
    for kpath, attrmeta in filter(lambda _: is_visible(_[1]),
                                  dictWalker(cfgattrmeta)
                                  ):
        if 'title' in kpath:
            logger.debug(f"ctxmp {attrmeta.context} {ctx}")

        if ctx in attrmeta.context:
            yield kpath

    pass


def update_cfgattrmeta_kpath(kpath, val, cfgattrmeta, chartcfg):
    """the key function: update cfgattrmeta if context changes
    """

    ctx = (kpath, val)
    logger.info(f"update_cfgattrmeta_kpath: {kpath} {ctx}")
    for dpath in attrmeta_in_context(ctx, cfgattrmeta):
        attrupdate(cfgattrmeta, dpath, val)
        logger.debug(f"paths in ctx: {dpath}")

    match(kpath, val):
        case("/type", None):
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", False)
        case("/type", PlotType.Line | 'line'):  # value in justpy is never a python objet
            # TODO: also disable any
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", True)
            for dpath in attrmeta_in_context(('/type', 'line'), cfgattrmeta):
                # update all things in the ('/type', 'line') context
                attrupdate(cfgattrmeta, dpath, True)
            # activate point element
            # activate line element

        case("/options/scales/xAxis/grid/display", True):
            for _ in ['color', 'borderColor', 'tickColor']:  # deal with circular later
                attrupdate(
                    cfgattrmeta, f"/options/scales/xAxis/grid/{_}", True)
        case("/options/parsing/value", True):
            # TODO: make it more generic by using FalseDict type
            #parsing_metaval = cfgattrmeta.options.parsing.value
            # for k, v in parsing_metaval.vrange.items():
            #    logger.debug(f"adding /options/parsing/{k} to cfgattrmeta")
            #    attradd(cfgattrmeta, f"/options/parsing/{k}", v)
            match dget(chartcfg, "/type"):
                case PlotType.Line | 'line':
                    attrupdate(cfgattrmeta, "/options/parsing/x", True)
                    attrupdate(cfgattrmeta, "/options/parsing/y", True)
                case PlotType.Bubble:
                    attrupdate(cfgattrmeta, "/options/parsing/id", True)
