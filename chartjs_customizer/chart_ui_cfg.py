"""all things required to build/update/maintain chart and ui cfg"""
from addict import Dict
from typing import NamedTuple, Any
from webapp_framework.uic_generator_attrMeta import AttrMeta
from justpy_chartjs.tags.cfg_template import Color, CPT
from justpy_chartjs.tags.style_values import Align, Position
from justpy_chartjs.tags.style_values import Axis
from aenum import Enum, auto
from dpath.util import get as dget, set as dset, new as dnew


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


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    vtype: Any
    vrange: Any
    decor_type: Any
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
    _base.type = AttrMeta(PlotType.Undef, PlotType, PlotType, CPT.simple, True)
    _base.options.responsive = AttrMeta(
        True, bool, bool, CPT.perf, True)
    _base.options.aspectRatio = AttrMeta(
        2, int, [1, 4], CPT.advanced, True)
    _base.options.resizeDelay = AttrMeta(
        4, int, [1, 9], CPT.perf, True)
    _base.options.devicePixelRatio = AttrMeta(
        1, int, [1, 5], CPT.advanced, True)
    _base.options.parsing = AttrMeta(False, FalseDict,
                                     {
                                     }, CPT.advanced, True)

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
            print("FalseDict class")
            return cam.default

        case "<aenum 'Position'>" | "<aenum 'PlotType'>":
            return cam.default

        case "<aenum 'Color'>":
            print("position class")
            return None  # TODO: will deal with later

        case _:
            print("no match ", cam.vtype)
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
    def is_active(kpath):
        attrmeta = dget(cfgattrmeta, kpath)
        return attrmeta.active
    for kpath in filter(is_active, cfgattrmeta.get_changed_history()):
        attrmeta = dget(cfgattrmeta, kpath)
        print(kpath)
        # print(attrmeta)
        evalue = eval_attrmetadefault(kpath, attrmeta)
        dnew(cjs_cfg, kpath, evalue)
    cfgattrmeta.clear_changed_history()


# ======================== end update_chartCfg =======================

# ============================= func def =============================


def update_cfgattrmeta_kpath(kpath, val, cfgattrmeta):
    """
    add/delete attrMeta in cfgMeta based on new attr settings
    """
    match(kpath, val):
        case("/type", None):
            _ = cfgattrmeta.options.scales.xAxis.grid
            _.pop("display", None)
            _.display = AttrMeta(
                False, bool, bool, CPT.simple, False)

        case("/type", PlotType.Line):
            _ = cfgattrmeta.options.scales.xAxis.grid
            _.pop("display", None)
            _.display = AttrMeta(
                False, bool, bool, CPT.simple, True)

        case("/options/scales/xAxis/grid/display", True):
            _ = cfgMeta.options.scales.xAxis.grid
            _.pop('color', None)
            _.pop('borderColor', None)
            _.pop('tickColor', None)
            _.pop('circular', None)
            _.color = AttrMeta("", Color, Color, CPT.simple, True)
            _.borderColor = AttrMeta(
                "", Color, Color, CPT.nitpick, False)
            _.tickColor = AttrMeta(
                "", Color, Color, CPT.simplemore, False)
            _.circular = AttrMeta(
                None, None, None, CPT.TBD, False)  # from for radar chart

        case("/options/parsing", True):
            _ = cfgMeta.options.parsing
            _.pop('xAxisKey', None)
            _.pop('yAxisKey', None)
            _.xAxisKey = AttrMeta(
                'x', str,  str, CPT.config, True)
            _.yAxisKey = AttrMeta(
                'y', str,  str, CPT.config, True)
            _

# ====================== end update_cfgattrmeta ======================


# ============================= func def ============================
def update_cfgattrmeta_chartcfg(chartcfg, cfgAttrMeta):
    for kpath in chartcfg.get_changed_history():
        update_cfgattrmeta_kpath(kpath, dget(cjs_cfg, kpath), cfgAttrMeta)
    chartcfg.clear_changed_history()
# ================== end update_cfgattrmeta_chartcfg =================
