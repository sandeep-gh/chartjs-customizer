
"""all things required to build/update/maintain chart and ui cfg"""
import logging
from addict import Dict
from typing import NamedTuple, Any
from webapp_framework.uic_generator_attrMeta import AttrMeta
# from justpy_chartjs.tags.cfg_template import Color
from justpy_chartjs.tags.style_values import Align, Position
from justpy_chartjs.tags.style_values import Axis
from aenum import Enum, auto
from dpath.util import get as dget, set as dset, new as dnew, delete as dpop
from dpath.exceptions import PathNotFound
import webapp_framework as wf
import traceback
from versa_engine.common.plot_utils import pick_colors_from_anchors


def is_visible(attrmeta):
    if attrmeta.vtype != None:
        if attrmeta.group != CPT.TBD:
            return True
    return False


def addict_walker(adict, ppath=""):
    for key, value in adict.items():
        if isinstance(value, Dict):
            yield from addict_walker(value, ppath + f"/{key}")
        else:
            yield (f"{ppath}/{key}", value)
            pass


class Color(Enum):
    pass


class CPT(Enum):
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


class FalseDict(Enum):
    """
    value is either False or a dict
    """
    pass


class PlotType(Enum):
    Line = "line"
    Bar = "bar"
    Scatter = "scatter"
    Bubble = "bubble"
    Undef = None


# =========================== func def ===========================
all_context = [('*', '*')]


def attrmeta_in_context(ctx, cfgattrmeta):
    for kpath, attrmeta in filter(lambda _: is_visible(_[1]),
                                  addict_walker(cfgattrmeta)
                                  ):
        if ctx in attrmeta.context:
            yield kpath

    pass


def get_baseCfgAttrMeta():
    _base = cfgAttrMeta_base = Dict(track_changes=True)
    _base.type = AttrMeta(PlotType.Undef, PlotType,
                          PlotType, CPT.initial, True, all_context)
    _base.options.responsive = AttrMeta(
        True, bool, bool, CPT.perf, True, [('*', '*')])
    _base.options.aspectRatio = AttrMeta(
        2, int, [1, 4], CPT.advanced, True, [('*', '*')])
    _base.options.resizeDelay = AttrMeta(
        4, int, [1, 9], CPT.perf, True, [('*', '*')])
    _base.options.devicePixelRatio = AttrMeta(
        1, int, [1, 5], CPT.advanced, True, [('*', '*')])
    _base.options.parsing.value = AttrMeta(False, FalseDict,
                                           {'xAxisKey': AttrMeta('x', str, str, CPT.initial, False, [('/options/parsing/', True)]),
                                            'yAxisKey': AttrMeta('y', str, str, CPT.initial, False, [('/options/parsing/', True)]),
                                            'key': AttrMeta('id', str, str, CPT.initial, False, [('/options/parsing/', True)])
                                            }, CPT.initial, True, [('*', '*')])

    _base.options.parsing.xAxisKey = AttrMeta(
        'x', str, str, CPT.initial, False, [('options/parsing', 'True')])  # active only if /options/parsing is True
    _base.options.parsing.yAxisKey = AttrMeta(
        'y', str, str, CPT.initial, False, [('options/parsing', 'True')])
    _base.options.parsing.id = AttrMeta('id', str, str, CPT.initial, False, [
        ('options/parsing', 'True')])

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
        "", Color, Color, CPT.simple, True, [('/type', 'line')])
    _.borderWidth = AttrMeta(
        2, int, [0, 5], CPT.simple, True, [('/type', 'line')])
    _.borderColor = AttrMeta(
        "", Color, Color, CPT.simple,  True, [('/type', 'line')])
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
        "", Color, Color, CPT.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.borderColor = AttrMeta(
        "", Color, Color, CPT.simplemore, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.tickColor = AttrMeta(
        "", Color, Color, CPT.simplemore, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.circular = AttrMeta(
        None, None, None, CPT.simple, False, [('/options/scales/xAxis/grid/display', 'line')])  # from for radar chart

    return _base

# ==================== end get_baseCfgAttrMeta ===================


# ============================= fund def =============================
def eval_attrmetadefault(cam):
    '''
    cam: CfgattrMeta
    '''
    match str(cam.vtype):
        case "<class 'int'>" | "<class 'bool'>" | "<class 'str'>" | "<class 'float'>":

            return cam.default

        case "<aenum 'FalseDict'>":
            return cam.default

        case "<aenum 'Position'>" | "<aenum 'PlotType'>":
            return cam.default.value

        case "<aenum 'Color'>":
            return None  # TODO: will deal with later

        case _:
            print("unkown vtype :", cam)
            raise ValueError

# ===================== end eval_attrmetadefault =====================

# ============================= func def =============================


def build_plt_cfg(chart_cfg):
    """
    translate chart_cfg
    """
    def to_chartcfg_path(kpath, val):
        match kpath, val:
            case '/options/parsing/value', False:
                return '/options/parsing', False
            case '/options/parsing/value', True:
                return None  # let xkeys and ykeys take care of it
            case _:
                return kpath, val

    plt_cfg = Dict()
    for kpath, val in map(lambda _: to_chartcfg_path(_[0], _[1]), addict_walker(chart_cfg)):
        dnew(plt_cfg, kpath, val)

    return plt_cfg


def update_chartCfg(cfgattrmeta, cjs_cfg):
    """
    there are two copies of cfg: cjs_cfg and ui_cfg.
    cjs_cfg is used for chartjs.
    ui_cfg is for ui drawing.
    value of ui_cfg is a tuple (bool, default_value). In the
    cjs_cfg is what gets shipped to chartjs.
    """

    # remove everything thats changed and put it
    # back in only the active ones: this enables deletion
    for kpath in cfgattrmeta.get_changed_history():

        try:
            dpop(cjs_cfg, kpath, None)
        except PathNotFound as e:
            logging.info("skipping {kpath} as its not found in cjs_cfg")
            pass  # skip if path is not in chartcfg

    for kpath in filter(lambda kpath: dget(cfgattrmeta, kpath).active,
                        cfgattrmeta.get_changed_history()):
        attrmeta = dget(cfgattrmeta, kpath)
        evalue = eval_attrmetadefault(attrmeta)
        dnew(cjs_cfg, kpath, evalue)
    cfgattrmeta.clear_changed_history()


# ======================== end update_chartCfg =======================

# ============================= func def =============================

def attrupdate(cfgattrmeta, kpath, active):
    attrmeta = dget(cfgattrmeta, kpath)
    attrmeta = attrmeta._replace(active=active)
    wf.dupdate(cfgattrmeta, kpath, attrmeta)


def update_cfgattrmeta_kpath(kpath, val, cfgattrmeta, chartcfg):
    """
     add/delete attrMeta in cfgMeta based on new attr settings
    """
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

# ====================== end update_cfgattrmeta ======================


# ============================= func def ============================
def update_cfgattrmeta(chartcfg, cfgAttrMeta):
    for kpath in chartcfg.get_changed_history():
        update_cfgattrmeta_kpath(kpath, dget(
            chartcfg, kpath), cfgAttrMeta, chartcfg)

# ================== end update_cfgattrmeta_chartcfg =================


# ========================== add data items ==========================
colorSchemes = {"default": ["#7f3b08", "#f7f7f7", "#2d004b"]
                }

colorset = default_colorset = pick_colors_from_anchors(
    colorSchemes["default"], 8)


labels = ["ds1", "ds2", "ds3", "ds4", "ds5"]
datavals = [[{'x': 1, 'y': 3}, {'x': 5, 'y': 5}],
            [{'x': 1, 'y': 7}, {'x': 5, 'y': 2}],
            [{'x': 1, 'y': 0}, {'x': 5, 'y': 8}],
            [{'x': 1, 'y': 13}, {'x': 5, 'y': 2}],
            [{'x': 1, 'y': 2}, {'x': 5, 'y': 6}],
            [{'x': 1, 'y': 9}, {'x': 5, 'y': 7}],
            ]


def datagen(labels, datavals):
    for idx, label, dataval in zip(range(len(labels)), labels, datavals):
        dataitem = Dict()
        dataitem.label = label
        dataitem.data = dataval
        dataitem.borderColor = colorset[idx]
        dataitem.backgroundColor = colorset[idx]
        # dataitem.stack = None #treeshake it; defines a group
        # dataitem.borderWidth = 2 #decor parameter
        # dataitem.borderRadius = 5 #decor parameter
        # dataitem.borderDash = [3, 3] #decor param
        # dataitem.yAxisID = 'y' #config param
        # dataitem.fill = False #decor param
        # if pltctx.plttype in ['line']:
        #     dataitem.cubicInterpolationModel = 'cubic' #decor param
        #     dataitem.tension = 0.5
        yield dataitem


def add_dataset(chartcfg):
    chartcfg.data.datasets = [_ for _ in datagen(labels, datavals)]

# =============================== done ===============================
