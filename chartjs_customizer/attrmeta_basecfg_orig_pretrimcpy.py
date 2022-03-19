
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

from .attrmeta_basecfg_helper import AttrMeta, PlotType, uiorgCat, Color, BorderCapStyle, LineJoinStyle, CubicInterpolationMode, TextAlign, FalseDict, PointStyle

all_context = [('*', '*')]


def OptionsElementsLineCfg(_cfg):

    _cfg.tension = AttrMeta(0, float, [0, 1], uiorgCat.advanced, True, [
        ('/type', 'line')])

    _cfg.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, True, [('/type', 'line')])
    _cfg.borderWidth = AttrMeta(
        2, int, [0, 5], uiorgCat.simple, True, [('/type', 'line')])
    _cfg.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simple,  True, [('/type', 'line')])
    _cfg.borderCapStyle = AttrMeta(
        BorderCapStyle.butt, BorderCapStyle, BorderCapStyle, uiorgCat.nitpick, True, [('/type', 'line')])

    # TODO: handle this later; require idea of segment
    #     segments
    # An Array of numbers that specify distances to alternately draw a line and a gap (in coordinate space units). If the number of elements in the array is odd, the elements of the array get copied and concatenated. For example, [5, 15, 25] will become [5, 15, 25, 5, 15, 25]. If the array is empty, the line dash list is cleared and line strokes return to being solid.
    _cfg.borderDash = AttrMeta([], None, None, uiorgCat.TBD,
                               False, [('/type', 'line')])
    _cfg.borderDashOffset = AttrMeta(
        0.0, float, float, uiorgCat.nitpick, True, [('/type', 'line')])
    _cfg.borderJoinStyle = AttrMeta(
        LineJoinStyle.miter, LineJoinStyle, LineJoinStyle, uiorgCat.nitpick, True, [('/type', 'line')])
    _cfg.capBezierPoints = AttrMeta(
        True, bool, bool, uiorgCat.advanced, False, [('/type', 'line')])
    _cfg.cubicInterpolationMode = AttrMeta(
        CubicInterpolationMode.default, CubicInterpolationMode, CubicInterpolationMode, uiorgCat.advanced, True, [('/type', 'line')])
    _cfg.fill = AttrMeta(None, None, None, uiorgCat.TBD,
                         False, [('/type', 'line')])  # TODO: bool/string
    _cfg.stepped = AttrMeta(False, bool, bool, uiorgCat.simple,
                            False, [('/type', 'line')])


def OptionsPluginsLegend(_cfg):
    _cfg.display = AttrMeta(
        True, bool, bool, uiorgCat.simple, True, all_context)

    _cfg.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.align = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.maxHeight = AttrMeta(
        20, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.maxWidth = AttrMeta(
        80, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.fullSize = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.reverse = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.rtl = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])


def OptionsPluginsLegendLabels(_cfg):

    _cfg.boxWidth = AttrMeta(
        40, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])
    _cfg.boxHeight = AttrMeta(
        12, int, int, uiorgCat.simple, True,  [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])
    _cfg.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, False, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    # TODO: labels.fond

    _cfg.padding = AttrMeta(
        40, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    # TODO: filter, sort
    _cfg.usePointStyle = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _cfg.pointStyle = AttrMeta(PointStyle.circle,   PointStyle, PointStyle, uiorgCat.simple, True, [
        ('/options/plugins/legend/labels/usePointStyle', True), ('/options/plugins/legend/labels/usePointStyle', False)])

    _cfg.textAlign = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, False, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])


def OptionsPluginsLegendTitle(_cfg):
    _cfg.display = AttrMeta(
        True, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])  # TODO: fix bug adict changed during iteration;

    _cfg.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, True, [('/options/plugins/legend/title/display', True), ('/options/plugins/legend/title/display', False)])
    # # TODO:font
    _cfg.paddding = AttrMeta(
        0, int, int, uiorgCat.simple, True,  [('/options/plugins/legend/title/display', True), ('/options/plugins/legend/title/display', False)])

    _cfg.text = AttrMeta(
        "legend_title", str, str, uiorgCat.simple, False, [('/options/plugins/legend/title/display', True), ('/options/plugins/legend/title/display', False)])


def OptionsScalesXAxisGrid(_cfg):
    _cfg.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/type', 'line')])
    _cfg.color = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _cfg.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _cfg.tickColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _cfg.circular = AttrMeta(
        None, None, None, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])  # from for radar chart


def get_basecfg():
    """generate canonical attrmeta
    """

    _base = cfgAttrMeta_base = Dict(track_changes=True)
    _base.type = AttrMeta(PlotType.Undef, PlotType,
                          PlotType, uiorgCat.initial, True, all_context)

    def Options():
        options = _base.options

        def Elements():
            elements = options.elements

            def Line():
                linecfg = elements.line
                OptionsElementsLineCfg(linecfg)
            Elements.Line = Line

        Elements()
        Options.Elements = Elements

        def Plugins():
            plugins = options.plugins

            def Legend():
                legend = plugins.legend
                OptionsPluginsLegend(legend)
                legendtitle = legend.title
                OptionsPluginsLegendTitle(legendtitle)

                legendlabels = legend.labels
                OptionsPluginsLegendLabels(legendlabels)

            Plugins.Legend = Legend

            def Tooltips():
                tooltips = plugins.tooltips
                # TODO:tobe filled uplater
                print("will deal with later")
                pass
            Plugins.Tooltips = Tooltips
        Plugins()
        Options.Plugins = Plugins

        def Scales():
            scales = options.scales

            def XAxis():
                xAxis = scales.xAxis

                def Grid():
                    grid = xAxis.grid
                    OptionsScalesXAxisGrid(grid)
                XAxis.Grid = Grid
            XAxis()
            Scales.XAxis = XAxis
        Scales()
        Options.Scales = Scales
    Options()

    _base.options.responsive = AttrMeta(
        True, bool, bool, uiorgCat.perf, True, all_context)
    _base.options.aspectRatio = AttrMeta(
        2, int, [1, 4], uiorgCat.advanced, True, all_context)
    _base.options.resizeDelay = AttrMeta(
        4, int, [1, 9], uiorgCat.perf, True, all_context)
    _base.options.devicePixelRatio = AttrMeta(
        1, int, [1, 5], uiorgCat.advanced, True, all_context)

    _base.options.parsing.value = AttrMeta(False, FalseDict,
                                           Dict({'x': AttrMeta('x', str, str, uiorgCat.initial,
                                                               False, [('/options/parsing/', True)]),
                                                 'y': AttrMeta('y', str, str,  uiorgCat.initial, False, [('/options/parsing/', True)]),
                                                 'id': AttrMeta('id', str, str, uiorgCat.initial, False, [('/options/parsing/', True)])
                                                 }), uiorgCat.TBD, True, all_context)

    _base.options.parsing.x = AttrMeta(
        'x', str, str, uiorgCat.TBD, False, [('options/parsing', True)])  # active only if /options/parsing is True
    _base.options.parsing.y = AttrMeta(
        'y', str, str, uiorgCat.TBD, False, [('options/parsing', True)])
    _base.options.parsing.id = AttrMeta('id', str, str, uiorgCat.TBD, False, [
        ('options/parsing', 'True')])

    # _base.options.plugins = Dict()
    # _base.options.plugins.legend = Dict()

    _base.options.plugins.legend.display = AttrMeta(
        True, bool, bool, uiorgCat.simple, True, all_context)

    _base.options.plugins.legend.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.align = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.maxHeight = AttrMeta(
        20, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.maxWidth = AttrMeta(
        80, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.fullSize = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.reverse = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.rtl = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    # ========================== end legend ==========================

    # ========================= legend.labels ========================

    _base.options.plugins.legend.labels.boxWidth = AttrMeta(
        40, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])
    _base.options.plugins.legend.labels.boxHeight = AttrMeta(
        12, int, int, uiorgCat.simple, True,  [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])
    _base.options.plugins.legend.labels.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, False, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    # TODO: labels.fond

    _base.options.plugins.legend.labels.padding = AttrMeta(
        40, int, int, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    # TODO: filter, sort
    _base.options.plugins.legend.labels.pointStyle = AttrMeta(PointStyle.circle,   PointStyle, PointStyle, uiorgCat.simple, True, [
                                                              ('/options/plugins/legend/labels/usePointStyle', True), ('/options/plugins/legend/labels/usePointStyle', False)])

    _base.options.plugins.legend.labels.textAlign = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, False, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.labels.usePointStyle = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    # ======================= end legend.labels ======================

    # ========================= legend.title =========================
    # _base.options.plugins.legend.title = Dict(track_changes=True)

    # _base.options.plugins.legend.title.display = AttrMeta(True, bool, bool, uiorgCat.simple, True, [
    # ('/options/plugins/legend/display', True), ('/options/plugins/legend/display', False)])

    _base.options.plugins.legend.title.display = AttrMeta(
        True, bool, bool, uiorgCat.simple, True, all_context)  # TODO: fix bug adict changed during iteration;

    _base.options.plugins.legend.title.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, True, all_context)
    # # TODO:font
    _base.options.plugins.legend.title.paddding = AttrMeta(
        0, int, int, uiorgCat.simple, True,  all_context)

    _base.options.plugins.legend.title.text = AttrMeta(
        "legend_title", str, str, uiorgCat.simple, False, all_context)

    # ======================= end legend.title =======================

    _base.options.plugins.title.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, all_context)
    _base.options.plugins.title.text = AttrMeta(
        "plot_title", str, str, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])
    _base.options.plugins.title.align = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])
    _base.options.plugins.title.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])
    _base.options.plugins.title.fullSize = AttrMeta(
        False, bool, bool, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])

    _base.options.plugins.title.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])

    _base.options.plugins.title.padding = AttrMeta(
        10, int, int, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])

    _base.options.plugins.subtitle.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, all_context)
    _base.options.plugins.subtitle.text = AttrMeta(
        "plot_subtitle", str, str, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])
    _base.options.plugins.subtitle.align = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])
    _base.options.plugins.subtitle.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])
    _base.options.plugins.subtitle.fullSize = AttrMeta(
        False, bool, bool, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])

    _base.options.plugins.subtitle.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])

    _base.options.plugins.subtitle.padding = AttrMeta(
        10, int, int, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])

    def Options():
        options = _base.options

        def Plugins():
            plugins = options.plugins

            def Tooltips():
                tooltips = plugins.tooltips
                # TODO:tobe filled uplater
                print("will deal with later")
                pass
            Plugins.Tooltips = Tooltips
        Plugins()
        Options.Plugins = Plugins
    Options()
    print("hope")
    Options.Plugins.Tooltips()
    # ========================= elements/line ========================
    _base.options.elements.line.tension = AttrMeta(0, float, [0, 1], uiorgCat.advanced, True, [
        ('/type', 'line')])
    _ = _base.options.elements.line
    _.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, True, [('/type', 'line')])
    _.borderWidth = AttrMeta(
        2, int, [0, 5], uiorgCat.simple, True, [('/type', 'line')])
    _.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simple,  True, [('/type', 'line')])
    _.borderCapStyle = AttrMeta(
        BorderCapStyle.butt, BorderCapStyle, BorderCapStyle, uiorgCat.nitpick, True, [('/type', 'line')])

    # TODO: handle this later; require idea of segment
    #     segments
    # An Array of numbers that specify distances to alternately draw a line and a gap (in coordinate space units). If the number of elements in the array is odd, the elements of the array get copied and concatenated. For example, [5, 15, 25] will become [5, 15, 25, 5, 15, 25]. If the array is empty, the line dash list is cleared and line strokes return to being solid.
    _.borderDash = AttrMeta([], None, None, uiorgCat.TBD,
                            False, [('/type', 'line')])
    _.borderDashOffset = AttrMeta(
        0.0, float, float, uiorgCat.nitpick, True, [('/type', 'line')])
    _.borderJoinStyle = AttrMeta(
        LineJoinStyle.miter, LineJoinStyle, LineJoinStyle, uiorgCat.nitpick, True, [('/type', 'line')])
    _.capBezierPoints = AttrMeta(
        True, bool, bool, uiorgCat.advanced, False, [('/type', 'line')])
    _.cubicInterpolationMode = AttrMeta(
        CubicInterpolationMode.default, CubicInterpolationMode, CubicInterpolationMode, uiorgCat.advanced, True, [('/type', 'line')])
    _.fill = AttrMeta(None, None, None, uiorgCat.TBD,
                      False, [('/type', 'line')])  # TODO: bool/string
    _.stepped = AttrMeta(False, bool, bool, uiorgCat.simple,
                         False, [('/type', 'line')])
    # ============================ end elements/line===========================
    _base.options.elements.point.radius = AttrMeta(3, int, [0, 5], uiorgCat.simple, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.pointStyle = AttrMeta(PointStyle.circle,   PointStyle, PointStyle, uiorgCat.simple, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.rotation = AttrMeta(0, int, int, uiorgCat.advanced, True,  [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [(
            '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.borderWidth = AttrMeta(1, int, [0, 5], uiorgCat.simple, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.borderColor = AttrMeta(
        twt.gray/4, Color, Color, uiorgCat.simple, False, [(
            '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.hitRadius = AttrMeta(1, int, [0, 5], uiorgCat.nitpick, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.hoverRadius = AttrMeta(4, int, [0, 5], uiorgCat.nitpick, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _base.options.elements.point.hoverBorderWidth = AttrMeta(1, int, [0, 5], uiorgCat.nitpick, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])

    # ==================== options.elements.points ===================

    # ============================== end =============================

    _xAxis = _base.options.scales.xAxis
    # _xAxis.grid = Dict()  # TBD
    _xAxis.grid.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/type', 'line')])
    _xAxis.grid.color = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.tickColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])
    _xAxis.grid.circular = AttrMeta(
        None, None, None, uiorgCat.simple, False, [('/options/scales/xAxis/grid/display', 'line')])  # from for radar chart

    return _base

# ==================== end get_baseCfgAttrMeta ===================
