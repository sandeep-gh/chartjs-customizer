"""all things required to build/update/maintain chart and ui cfg"""
from addict import Dict
from typing import NamedTuple, Any
from webapp_framework.uic_generator_attrMeta import AttrMeta
#from justpy_chartjs.tags.cfg_template import Color
from justpy_chartjs.tags.style_values import Align, Position
from justpy_chartjs.tags.style_values import Axis
from aenum import Enum, auto
from dpath.util import get as dget, set as dset, new as dnew, delete as dpop
from dpath.exceptions import PathNotFound
import webapp_framework as wf
import traceback


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
def get_baseCfgAttrMeta():
    _base = cfgAttrMeta_base = Dict(track_changes=True)
    _base.type = AttrMeta(PlotType.Undef, PlotType,
                          PlotType, CPT.initial, True)
    _base.options.responsive = AttrMeta(
        True, bool, bool, CPT.perf, True)
    _base.options.aspectRatio = AttrMeta(
        2, int, [1, 4], CPT.advanced, True)
    _base.options.resizeDelay = AttrMeta(
        4, int, [1, 9], CPT.perf, True)
    _base.options.devicePixelRatio = AttrMeta(
        1, int, [1, 5], CPT.advanced, True)
    _base.options.parsing.value = AttrMeta(False, FalseDict,
                                           {'xAxisKey': AttrMeta('x', str, str, CPT.initial, False),
                                            'yAxisKey': AttrMeta('y', str, str, CPT.initial, False),
                                            'key': AttrMeta('id', str, str, CPT.initial, False)
                                            }, CPT.initial, True)

    _base.options.parsing.xAxisKey = AttrMeta(
        'x', str, str, CPT.initial, False)
    _base.options.parsing.yAxisKey = AttrMeta(
        'y', str, str, CPT.initial, False)
    _base.options.parsing.id = AttrMeta('id', str, str, CPT.initial, False)

    #_base.options.plugins = Dict()
    #_base.options.plugins.legend = Dict()
    _base.options.plugins.legend.position = AttrMeta(
        Position.top, Position, Position, CPT.simplemore, True)

    #_base.options.plugins.title = Dict()
    _base.options.plugins.title.display = AttrMeta(
        True, bool, bool, CPT.simple, True)
    _base.options.plugins.title.text = AttrMeta(
        "plot_title", str, str, CPT.simple, True)

    _xAxis = _base.options.scales.xAxis
    # _xAxis.grid = Dict()  # TBD
    _xAxis.grid.display = AttrMeta(
        False, bool, bool, CPT.simple, False)
    _xAxis.grid.color = AttrMeta(
        "", Color, Color, CPT.simple, False)
    _xAxis.grid.borderColor = AttrMeta(
        "", Color, Color, CPT.nitpick, False)
    _xAxis.grid.tickColor = AttrMeta(
        "", Color, Color, CPT.simplemore, False)
    _xAxis.grid.circular = AttrMeta(
        None, None, None, CPT.TBD, False)  # from for radar chart

    return _base

# ==================== end get_baseCfgAttrMeta ===================


# ============================= fund def =============================
def eval_attrmetadefault(key, cam):
    '''
    cam: CfgattrMeta
    '''
    match str(cam.vtype):
        case "<class 'int'>" | "<class 'bool'>" | "<class 'str'>":

            return cam.default

        case "<aenum 'FalseDict'>":
            return cam.default

        case "<aenum 'Position'>" | "<aenum 'PlotType'>":
            return cam.default

        case "<aenum 'Color'>":
            return None  # TODO: will deal with later

        case _:
            raise ValueError

# ===================== end eval_attrmetadefault =====================

# ============================= func def =============================


def update_chartCfg(cfgattrmeta, cjs_cfg, ui_cfg):
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
            pass  # skip if path is not in chartcfg

    for kpath in filter(lambda kpath: dget(cfgattrmeta, kpath).active,
                        cfgattrmeta.get_changed_history()):
        attrmeta = dget(cfgattrmeta, kpath)
        evalue = eval_attrmetadefault(kpath, attrmeta)
        dnew(cjs_cfg, kpath, evalue)
    cfgattrmeta.clear_changed_history()


# ======================== end update_chartCfg =======================

# ============================= func def =============================

def attrupdate(addict, kpath, active):
    attrmeta = dget(addict, kpath)
    attrmeta = attrmeta._replace(active=active)
    wf.dupdate(addict, kpath, attrmeta)


def update_cfgattrmeta_kpath(kpath, val, cfgattrmeta, chartcfg):
    """
    add/delete attrMeta in cfgMeta based on new attr settings
    """
    print("update_cfgattrmeta_kpath: for kpath = ", kpath, " val = ", val)
    match(kpath, val):
        case("/type", None):
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", False)
        case("/type", PlotType.Line):
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", True)
        case("/options/scales/xAxis/grid/display", True):
            _ = cfgMeta.options.scales.xAxis.grid
            for _ in ['color', 'borderColor', 'tickColor', 'circular']:
                attrupdate(
                    cfgattrmeta, f"/options/scales/xAxis/grid/{_}", True)

        case("/options/parsing/value", True):
            print("in /options/parsing/value")
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

    for kpath in cfgAttrMeta.get_changed_history():
        print(f"changed cfgAttrMeta: {kpath}")
    chartcfg.clear_changed_history()
# ================== end update_cfgattrmeta_chartcfg =================
