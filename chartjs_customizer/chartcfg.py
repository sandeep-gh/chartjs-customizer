import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
from addict import Dict
from .dpathutils import walker as dictWalker
from dpath.exceptions import PathNotFound
from .dpathutils import dget, dnew, dpop
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
    for kpath, val in map(lambda _: to_chartcfg_path(_[0], _[1]), dictWalker(chart_cfg, guards=["/data"])):
        print("build_pltcfg ", kpath, " ", val)
        dnew(plt_cfg, kpath, val)

    #print("done build_pltcfg")
    return plt_cfg


def update_chartCfg(cfgattrmeta, cjscfg):
    """

    """
    logger.debug("=========== startupdate_chartCfg  ===============")
    # remove everything thats changed and put it
    # back in only the active ones: this enables deletion
    for kpath in cfgattrmeta.get_changed_history():
        #logger.debug(f"path {kpath} changed in cfgattrmeta")
        try:
            dpop(cjscfg, kpath, None)
        except PathNotFound as e:
            #logger.info(f"skipping: {kpath} not found in cjscfg")
            pass  # skip if path is not in chartcfg

    # def logdebug(kpath):
    #     if 'title' in kpath:
    #         logger.debug(f"kuchkuch {kpath} {dget(cfgattrmeta, kpath)}")
    #     return dget(cfgattrmeta, kpath).active
    # for kpath in filter(logdebug,
    #                     cfgattrmeta.get_changed_history()):

    for kpath in filter(lambda kpath: dget(cfgattrmeta, kpath).active,
                        cfgattrmeta.get_changed_history()):

        evalue = attrmeta.get_defaultVal(dget(cfgattrmeta, kpath))
        dnew(cjscfg, kpath, evalue)
        logger.debug(f"path {kpath} updated with {evalue} in cjscfg")
    logger.debug("=========== done update_chartCfg  ===============")
    # cfgattrmeta.clear_changed_history()


def update_cfgattrmeta(chartcfg, cfgAttrMeta):
    """update cfgattrmeta corresponding to changes in chartcfg
    """
    logger.info("update cfgattrmeta: to reflect chartcfg changes")
    for kpath in chartcfg.get_changed_history():
        logger.info(f"{kpath} has changed in chartcfg")
        attrmeta.update_cfgattrmeta_kpath(kpath, dget(
            chartcfg, kpath), cfgAttrMeta, chartcfg)

    logger.debug("done update_cfgattrmeta...")


# ===================== all things plotting data =====================
colorSchemes = {"default": ["#7f3b08", "#f7f7f7", "#2d004b"]
                }

colorset = default_colorset = pick_colors_from_anchors(
    colorSchemes["default"], 8)

labels = ["ds1", "ds2", "ds3", "ds4", "ds5"]
datavals = [[{'x': 1, 'y': 3}, {'x': 5, 'y': 5}, {'x': 7, 'y': 7}],
            [{'x': 1, 'y': 7}, {'x': 5, 'y': 2}, {'x': 7, 'y': 3}],
            [{'x': 1, 'y': 0}, {'x': 5, 'y': 8}, {'x': 7, 'y': 5}],
            [{'x': 1, 'y': 13}, {'x': 5, 'y': 2}, {'x': 7, 'y': 1}],
            [{'x': 1, 'y': 2}, {'x': 5, 'y': 6}, {'x': 7, 'y': 6}],
            [{'x': 1, 'y': 9}, {'x': 5, 'y': 7}, {'x': 7, 'y': 9}],
            ]


def datagen(labels, datavals):
    for idx, label, dataval in zip(range(len(labels)), labels, datavals):
        dataitem = Dict(track_changes=True)
        dataitem.label = label
        dataitem.data = dataval
        dataitem.borderColor = colorset[idx]
        dataitem.backgroundColor = colorset[idx]
        yield dataitem


def add_dataset(chartcfg):
    """add plotting to chartcfg
    """

    chartcfg.data.datasets = [_ for _ in datagen(labels, datavals)]
