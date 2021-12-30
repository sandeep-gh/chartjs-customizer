import logging
from addict import Dict, walker as dictWalker
from dpath.exceptions import PathNotFound
from dpath.util import get as dget, set as dset, new as dnew, delete as dpop
from . import attrmeta
from versa_engine.common.plot_utils import pick_colors_from_anchors


def build_pltcfg(chart_cfg):
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
    for kpath, val in map(lambda _: to_chartcfg_path(_[0], _[1]), dictWalker(chart_cfg)):
        dnew(plt_cfg, kpath, val)

    return plt_cfg


def update_chartCfg(cfgattrmeta, cjscfg):
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
        print(f"update_chartCfg: cfgattrmeta:change{kpath}")
        try:
            dpop(cjscfg, kpath, None)
        except PathNotFound as e:
            logging.info("skipping {kpath} as its not found in cjs_cfg")
            pass  # skip if path is not in chartcfg

    for kpath in filter(lambda kpath: dget(cfgattrmeta, kpath).active,
                        cfgattrmeta.get_changed_history()):
        evalue = attrmeta.get_defaultVal(dget(cfgattrmeta, kpath))
        dnew(cjscfg, kpath, evalue)
    # cfgattrmeta.clear_changed_history()


def update_cfgattrmeta(chartcfg, cfgAttrMeta):
    """update cfgattrmeta corresponding to changes in chartcfg
    """

    for kpath in chartcfg.get_changed_history():
        attrmeta.update_cfgattrmeta_kpath(kpath, dget(
            chartcfg, kpath), cfgAttrMeta, chartcfg)


# ===================== all things plotting data =====================
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
        yield dataitem


def add_dataset(chartcfg):
    """add plotting to chartcfg
    """

    chartcfg.data.datasets = [_ for _ in datagen(labels, datavals)]
