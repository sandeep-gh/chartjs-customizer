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
import jsbeautifier
import json


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
            case '/options/scales/xaxes/__arr/':
                pass  # convert this to array
            case _:
                return kpath, val

    plt_cfg = Dict()
    for kpath, val in map(lambda _: to_chartcfg_path(_[0], _[1]), dictWalker(chart_cfg)):
        if val is not None:
            dnew(plt_cfg, kpath, val)

    #print("done build_pltcfg")
    return plt_cfg


def update_chartCfg(cfgattrmeta, cjscfg):
    """

    """
    logger.debug("=========== start update_chartCfg  ===============")
    # remove everything thats changed and put it
    # back in only the active ones: this enables deletion
    inactive_kpaths = set()
    for kpath in cfgattrmeta.get_changed_history():
        logger.debug(f"path {kpath} changed in cfgattrmeta")
        try:
            # logger.debug("what bakwas")
            # opts = jsbeautifier.default_options()
            # logger.debug(jsbeautifier.beautify(json.dumps(cjscfg), opts))
            dpop(cjscfg, kpath)
            inactive_kpaths.add(kpath)
        except PathNotFound as e:
            logger.info(f"skipping: {kpath} not found in cjscfg {e}")
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
        if kpath in inactive_kpaths:
            inactive_kpaths.remove(kpath)
        logger.debug(f"path {kpath} updated with {evalue} in cjscfg")

    # cfgattrmeta.clear_changed_history()
    if inactive_kpaths:
        logger.debug(f"paths that became inactive: {inactive_kpaths}")
    logger.debug("=========== done update_chartCfg  ===============")
    return inactive_kpaths


def update_cfgattrmeta(chartcfg, cfgAttrMeta, new_inactive_kpaths=[]):
    """update cfgattrmeta corresponding to changes in chartcfg
        new_inactive_paths: dict.change_history can only detect changes in value; and not popped out
        so all popped stuff is send separately
    """
    logger.info("update cfgattrmeta: to reflect chartcfg changes")
    for kpath in chartcfg.get_changed_history():
        new_val = dget(chartcfg, kpath)
        logger.debug(f"{kpath} has changed in chartcfg new_value={new_val}")
        # TODO: in addition to default value in cfgattrmeta -- also maintain the current value

        # e.g. x1/display is False then make the corresponding  cfgattrmeta false as well
        # logger.debug(
        #    f"fishy: update cfgattrmeta: active {kpath} to value={bool(new_val)}")
        #attrmeta.attrupdate(cfgAttrMeta, kpath, bool(new_val))

        # update all cfgs that ctx is above
        attrmeta.update_cfgattrmeta_kpath(
            kpath, new_val, cfgAttrMeta, chartcfg)

    for kpath in new_inactive_kpaths:
        # if the path is delete then set active to False
        attrmeta.attrupdate(cfgAttrMeta, kpath, False)
        # update all dependent attributes
        attrmeta.update_cfgattrmeta_kpath(kpath, False, cfgAttrMeta, chartcfg)

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
