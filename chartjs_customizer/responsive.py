# handle ui changes to options being selected
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


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    vtype: Any
    vrange: Any
    decor_type: Any
    disabled: Any


def update_cfg_attrMeta(kpath, val, cfgMeta):
    match(kpath, val):
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

            _


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

    # def update_chartCfg(cfgattrmeta, cfgchart):
    #     for key in cfgattrmeta.get_changed_history():
    #         attrMeta = dget(cfgattrmeta, key)
    #         evalue = cfgattreval(key, value, colorbank)
    #         if evalue is not None:
    #             setattr(cfgchart, key, evalue)

    # def update_uic(cfgchart): #for advanced version
    #     for key in cfgchart.get_changed_history():
    #         tlkey, tier1key = get_ui_category(key)
    #         if tier1key is None:
    #             dbref_target_container = dget(refBoard, tlkey)
    #         else:
    #             dbref_target_container = dget(refBoard, f"{tlkey}/{tier1key}")
    #         dbref_target_container.addItems(
    #             build_uic(key, label, attrMeta, refBoard))
