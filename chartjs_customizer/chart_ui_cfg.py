"""all things required to build/update/maintain chart and ui cfg"""

from typing import NamedTuple, Any
from webapp_framework.uic_generator_attrMeta import AttrMeta
from justpy_chartjs.tags.cfg_template import Color, CPT
from aenum import Enum, auto


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


class UI_State(Enum):
    enabled = auto()
    disabled = auto()


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    vtype: Any
    vrange: Any
    decor_type: Any
    ui_state: Any


class FalseDict:
    """
    value is either False or a dict
    """
    pass


_ = cfgAttrMeta_base = Dict()
_.options.responsive = AttrMeta(True, bool, bool, CPT.perf, UI_State.enabled)
_.options.aspectRatio = AttrMeta(
    2, int, [1, 4], CPT.advanced, UI_State.enabled)
_.options.resizeDelay = AttrMeta(4, int, [1, 9], CPT.perf, UI_State.enabled)
_.options.devicePixelRatio = AttrMeta(
    1, int, [1, 5], CPT.advanced, UI_State.enabled)
_.options.parsing = AttrMeta(False, FalseDict, {'xAxisKey': AttrMeta(
    'x', str,  str, CPT.config, UI_State.disabled)
    'yAxisKey': AttrMeta(
    'y', str,  str, CPT.config, UI_State.disabled)
}, CPT.advanced, UI_State.enabled)

cfg.options.plugins = Dict()
cfg.options.plugins.legend = Dict()
cfg.options.plugins.legend.position = AttrMeta(
    Position.top, Position, Position, CPT.simplemore, UI_State.enabled)

cfg.options.plugins.title = Dict()
cfg.options.plugins.title.display = AttrMeta(
    True, bool, bool, CPT.simple, UI_State.enabled)
cfg.options.plugins.title.text = AttrMeta(
    cfgctx["plot_title"], str, str, CPT.simple, UI_State.enabled)


_ = cfg.options.scales.xAxis = Dict()
_.grid = Dict()  # TBD
_.grid.display = AttrMeta(False, bool, bool, CPT.simple, UI_State.disabled)
_.grid.color = AttrMeta("", Color, Color, CPT.simple, UI_State.disabled)
_.grid.borderColor = AttrMeta("", Color, Color, CPT.nitpick, UI_State.disabled)
_.grid.tickColor = AttrMeta(
    "", Color, Color, CPT.simplemore, UI_State.disabled)
_.grid.circular = AttrMeta(
    None, None, None, CPT.TBD, UI_State.disabled)  # from for radar chart


def update_chartCfg(cfgattrmeta, cjs_cfg, ui_cfg):
    """
    there are two copies of cfg: cjs_cfg and ui_cfg. 
    cjs_cfg is used for chartjs.
    ui_cfg is for ui drawing. 
    value of ui_cfg is a tuple (bool, default_value). In the 
    cjs_cfg is what gets shipped to chartjs.
    """
    for kpath in cfgMeta.get_changed_history():
        print(kpath)

    pass


def update_cfgMeta(kpath, val, cfgMeta):
    """
    add/delete attrMeta to cfgMeta based on new attr settings
    """
    match(kpath, val):
        case("/type", PlotType.Line):
            _ = cfg.options.scales.xAxis.grid
            _.pop("display", None)
            _.display = AttrMeta(
                False, bool, bool, CPT.simple, UI_State.enabled)

        case("/options/scales/xAxis/grid/display", True):
            _ = cfgMeta.options.scales.xAxis.grid
            _.pop('color', None)
            _.pop('borderColor', None)
            _.pop('tickColor', None)
            _.pop('circular', None)
            _.color = AttrMeta("", Color, Color, CPT.simple, False)
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
                'x', str,  str, CPT.config, UI_State.enabled)
            _.yAxisKey = AttrMeta(
                'y', str,  str, CPT.config, UI_State.enabled)
            _
