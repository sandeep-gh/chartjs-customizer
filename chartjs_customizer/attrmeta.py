"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

from typing import NamedTuple, Any
from addict import Dict
from .dpathutils import walker as dictWalker
from aenum import Enum, auto
from .dpathutils import dget
from justpy_chartjs.tags.style_values import Align, Position
from justpy_chartjs.tags.style_values import Axis
import webapp_framework as wf
import tailwind_tags as twt
from tailwind_tags import color2hex as hexify
from .attrmeta_basecfg_helper import AttrMeta, PlotType, uiorgCat, Color, BorderCapStyle, LineJoinStyle, CubicInterpolationMode, FalseDict, is_visible


def get_defaultVal(attrmeta):  # TODO: ask SO if there is a better way to
    '''get default value of attrmeta
    '''
    cam = attrmeta
    match str(cam.vtype):
        case "<class 'int'>" | "<class 'bool'>" | "<class 'str'>" | "<class 'float'>":

            return cam.default

        case "<aenum 'FalseDict'>":
            return cam.default

        case "<aenum 'Position'>" | "<aenum 'PlotType'>" | "<aenum 'TextAlign'>" | "<aenum 'PointStyle'>" | "<aenum 'CubicInterpolationMode'>" | "<aenum 'BorderJoinStyle'>" | "<aenum 'BorderCapStyle'>" | "<aenum 'LineJoinStyle'>":
            return cam.default.value

        case "<aenum 'Color'>":
            return hexify(cam.default)  # TODO: will deal with later

        case _:
            print("unkown vtype :", cam)
            raise ValueError


def attrupdate(cfgattrmeta, kpath, active):

    attrmeta = dget(cfgattrmeta, kpath)
    attrmeta = attrmeta._replace(active=bool(active))
    wf.dupdate(cfgattrmeta, kpath, attrmeta)


# def is_visible(attrmeta):
#     if attrmeta.vtype != None:
#         if attrmeta.group != uiorgCat.TBD:
#             return True
#     return False


def attrmeta_in_context(ctx, cfgattrmeta):
    for _ in dictWalker(cfgattrmeta):
        if is_visible(_[1]):
            if ctx in _[1].context:
                yield _[0]
    # for kpath, attrmeta in filter(lambda _: is_visible(_[1]),
    #                               dictWalker(cfgattrmeta)
    #                               ):
    #     if ctx in attrmeta.context:
    #         yield kpath

    pass


def update_cfgattrmeta_kpath(kpath, val, cfgattrmeta, chartcfg):
    """the key function: update cfgattrmeta if context changes
    """

    ctx = (kpath, val)
    logger.info(
        f"=============update_cfgattrmeta_kpath: {kpath} {ctx}================")
    # TODO: we cannot be doing nested loop operation
    kpaths_in_context = [_ for _ in attrmeta_in_context(ctx, cfgattrmeta)]
    logger.debug(f"kpaths_in_context = {kpaths_in_context}")
    for dpath in kpaths_in_context:
        attrupdate(cfgattrmeta, dpath, bool(val))
        # as an example we have made x1/grid/display inactive with value None
        # when we next activate it .. its value would be False.
        # but in UI it would be true
        # either make it true in cjs_cfg/cfgattrmeta or make it false in ui
        # going with latter option as it is simpler
        logger.debug(f"update:cfgattrmeta: {dpath} active={bool(val)} ")
        logger.info(
            f"==========end update_cfgattrmeta_kpath: {kpath} {ctx}================")
