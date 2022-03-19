"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

from typing import NamedTuple, Any
from addict import Dict, walker as dictWalker
from aenum import Enum, auto
from dpath.util import get as dget, set as dset, new as dnew, delete as dpop
from justpy_chartjs.tags.style_values import Align, Position
from justpy_chartjs.tags.style_values import Axis
import webapp_framework as wf
import tailwind_tags as twt
from tailwind_tags import color2hex as hexify
from .attrmeta_basecfg_helper import AttrMeta, PlotType, uiorgCat, Color, BorderCapStyle, LineJoinStyle, CubicInterpolationMode, FalseDict, is_visible


# class AttrMeta(NamedTuple):
#     """
#     metadata about ui component
#     """
#     default: Any
#     vtype: Any
#     vrange: Any
#     group: Any
#     active: Any
#     context: Any  # describes all scenarios when attribute is active


# class uiorgCat(Enum):
#     """attrmeta belongs to one of the categories
#     """
#     simple = "simple"
#     simplemore = "simplemore"
#     nitpick = "nitpick"
#     ocd = "ocd"
#     perf = "perf"
#     config = "config"
#     advanced = "advanced"
#     required = "required"
#     TBD = "tbd"
#     ninja = "ninja"
#     initial = "initial"
#     all = "all"


# class PlotType(Enum):
#     Line = "line"
#     Bar = "bar"
#     Scatter = "scatter"
#     Bubble = "bubble"
#     Undef = None


# class PointStyle(Enum):
#     circle = 'circle'
#     cross = 'cross'
#     crossRot = 'crossRot'
#     dash = 'dash'
#     line = 'line'
#     rect = 'rect'
#     rectRounded = 'rectRounded'
#     rectRot = 'rectRot'
#     star = 'star'
#     triangle = 'triangle'


# class CubicInterpolationMode(Enum):
#     default = "default"
#     monotone = "monotone"


# class LineJoinStyle(Enum):
#     bevel = "bevel"
#     roundo = "round"
#     miter = "miter"


# class BorderCapStyle(Enum):
#     butt = "butt"
#     roundo = "round"
#     square = "square"


# class TextAlign(Enum):
#     start = "start"
#     center = "center"
#     end = "end"


# class Color(Enum):
#     pass


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
    logger.debug(f"attrupdate {kpath} {active} {bool(active)}")
    attrmeta = dget(cfgattrmeta, kpath)
    attrmeta = attrmeta._replace(active=bool(active))
    wf.dupdate(cfgattrmeta, kpath, attrmeta)


def attradd(cfgattrmeta, kpath, metaval):
    dnew(cfgattrmeta, kpath, metaval)


def is_visible(attrmeta):
    if attrmeta.vtype != None:
        if attrmeta.group != uiorgCat.TBD:
            return True
    return False


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
    logger.info(f"update_cfgattrmeta_kpath: {kpath} {ctx}")
    kpaths_in_context = [_ for _ in attrmeta_in_context(ctx, cfgattrmeta)]

    for dpath in kpaths_in_context:
        attrupdate(cfgattrmeta, dpath, val)
        logger.debug(f"{dpath}")

    logger.debug("landmakr 1")
    match(kpath, val):
        case("/type", None):
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", False)
        case("/type", PlotType.Line | 'line'):  # value in justpy is never a python objet
            # TODO: also disable any
            attrupdate(cfgattrmeta, "/options/scales/xAxis/grid/display", True)
            for dpath in attrmeta_in_context(('/type', 'line'), cfgattrmeta):
                # update all things in the ('/type', 'line') context
                attrupdate(cfgattrmeta, dpath, True)
            # activate point element
            # activate line element

        case("/options/scales/xAxis/grid/display", True):
            for _ in ['color', 'borderColor', 'tickColor']:  # deal with circular later
                attrupdate(
                    cfgattrmeta, f"/options/scales/xAxis/grid/{_}", True)
        case("/options/parsing/value", True):
            # TODO: make it more generic by using FalseDict type
            # parsing_metaval = cfgattrmeta.options.parsing.value
            # for k, v in parsing_metaval.vrange.items():
            #    logger.debug(f"adding /options/parsing/{k} to cfgattrmeta")
            #    attradd(cfgattrmeta, f"/options/parsing/{k}", v)
            match dget(chartcfg, "/type"):
                case PlotType.Line | 'line':
                    attrupdate(cfgattrmeta, "/options/parsing/x", True)
                    attrupdate(cfgattrmeta, "/options/parsing/y", True)
                case PlotType.Bubble:
                    attrupdate(cfgattrmeta, "/options/parsing/id", True)
