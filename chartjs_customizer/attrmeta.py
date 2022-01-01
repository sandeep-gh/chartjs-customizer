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


class CPT(Enum):
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
                          PlotType, CPT.initial, True, all_context)
    _base.options.responsive = AttrMeta(
        True, bool, bool, CPT.perf, True, all_context)
    _base.options.aspectRatio = AttrMeta(
        2, int, [1, 4], CPT.advanced, True, all_context)
    _base.options.resizeDelay = AttrMeta(
        4, int, [1, 9], CPT.perf, True, all_context)
    _base.options.devicePixelRatio = AttrMeta(
        1, int, [1, 5], CPT.advanced, True, all_context)
    _base.options.parsing.value = AttrMeta(False, FalseDict,
                                           {'xAxisKey': AttrMeta('x', str, str, CPT.initial, False, [('/options/parsing/', True)]),
                                            'yAxisKey': AttrMeta('y', str, str, CPT.initial, False, [('/options/parsing/', True)]),
                                            'key': AttrMeta('id', str, str, CPT.initial, False, [('/options/parsing/', True)])
                                            }, CPT.initial, True, [('*', '*')])

    # _base.options.parsing.xAxisKey = AttrMeta(
    #     'x', str, str, CPT.initial, False, [('options/parsing', 'True')])  # active only if /options/parsing is True
    # _base.options.parsing.yAxisKey = AttrMeta(
    #     'y', str, str, CPT.initial, False, [('options/parsing', 'True')])
    # _base.options.parsing.id = AttrMeta('id', str, str, CPT.initial, False, [
    #     ('options/parsing', 'True')])

    # _base.options.plugins = Dict()
    # _base.options.plugins.legend = Dict()
    _base.options.plugins.legend.position = AttrMeta(
        Position.top, Position, Position, CPT.simplemore, True, all_context)

    # _base.options.plugins.title = Dict()
    _base.options.plugins.title.display = AttrMeta(
        True, bool, bool, CPT.simple, True, all_context)
    _base.options.plugins.title.text = AttrMeta(
        "plot_title", str, str, CPT.simple, True, all_context)

    # ========================= elements/line ========================

    _base.options.elements = Dict(track_changes=True)
    _ = _base.options.elements.line = Dict(track_changes=True)
    _.tension = AttrMeta(0, float, [0, 1], CPT.advanced, True, [
        ('/type', 'line')])
    _.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, CPT.simple, True, [('/type', 'line')])
    _.borderWidth = AttrMeta(
        2, int, [0, 5], CPT.simple, True, [('/type', 'line')])
    _.borderColor = AttrMeta(
        twt.gray/2, Color, Color, CPT.simple,  True, [('/type', 'line')])
    _.borderCapStyle = AttrMeta(
        "butt", None, None, CPT.TBD, False, [('/type', 'line')])
    _.borderDash = AttrMeta([], None, None, CPT.TBD,
                            False, [('/type', 'line')])
    _.borderDashOffset = AttrMeta(
        0.0, None, None, CPT.TBD, False, [('/type', 'line')])
    _.borderJoinStyle = AttrMeta(
        "miter", None, None, CPT.TBD, False, [('/type', 'line')])
    _.capBezierPoints = AttrMeta(
        True, bool, bool, CPT.advanced, False, [('/type', 'line')])
    _.cubicInterpolationMode = AttrMeta(
        "default", None, None, CPT.TBD, False, [('/type', 'line')])
    _.fill = AttrMeta(None, None, None, CPT.TBD, False, [('/type', 'line')])
    _.stepped = AttrMeta(None, None, None, CPT.TBD,
                         False, [('/type', 'line')])
    # ============================ end elements/line===========================

    _xAxis = _base.options.scales.xAxis
    # _xAxis.grid = Dict()  # TBD
    _xAxis.grid.display = AttrMeta(
        False, bool, bool, CPT.simple, True, [('/type', 'line')])
    _xAxis.grid.color = AttrMeta(
        twt.gray/1, Color, Color, CPT.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.borderColor = AttrMeta(
        twt.gray/2, Color, Color, CPT.simplemore, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.tickColor = AttrMeta(
        twt.gray/1, Color, Color, CPT.simplemore, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.circular = AttrMeta(
        None, None, None, CPT.simple, False, [('/options/scales/xAxis/grid/display', 'line')])  # from for radar chart

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
            print("default val for {attrmeta} ", hexify(cam.default))
            return hexify(cam.default)  # TODO: will deal with later

        case _:
            print("unkown vtype :", cam)
            raise ValueError


def attrupdate(cfgattrmeta, kpath, active):

    print("attrupdate", kpath)
    attrmeta = dget(cfgattrmeta, kpath)
    attrmeta = attrmeta._replace(active=active)
    wf.dupdate(cfgattrmeta, kpath, attrmeta)


def is_visible(attrmeta):
    if attrmeta.vtype != None:
        if attrmeta.group != CPT.TBD:
            return True
    return False


def attrmeta_in_context(ctx, cfgattrmeta):
    for kpath, attrmeta in filter(lambda _: is_visible(_[1]),
                                  dictWalker(cfgattrmeta)
                                  ):
        if ctx in attrmeta.context:
            yield kpath

    pass


def update_cfgattrmeta_kpath(kpath, val, cfgattrmeta, chartcfg):
    """the key function: update cfgattrmeta if context changes
    """
    print(f"update_cfgattrmeta_kpath: {kpath}")
    match(kpath, val):
        case("/type", None):
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", False)
        case("/type", PlotType.Line | 'line'):  # value in justpy is never a python objet
            # TODO: also disable any
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", True)
            for dpath in attrmeta_in_context(('/type', 'line'), cfgattrmeta):
                attrupdate(cfgattrmeta, dpath, True)
            # activate point element
            # activate line element

        case("/options/scales/xAxis/grid/display", True):
            _ = cfgattrmeta.options.scales.xAxis.grid
            for _ in ['color', 'borderColor', 'tickColor']:  # deal with circular later
                attrupdate(
                    cfgattrmeta, f"/options/scales/xAxis/grid/{_}", True)

        case("/options/parsing/value", True):
            match dget(chartcfg, "/type"):
                case PlotType.Line | 'line':
                    attrupdate(cfgattrmeta, f"/options/parsing/xAxisKey", True)
                    attrupdate(cfgattrmeta, f"/options/parsing/yAxisKey", True)
                case PlotType.Bubble:
                    attrupdate(cfgattrmeta, f"/options/parsing/id", True)
