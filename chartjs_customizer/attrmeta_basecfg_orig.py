
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

from typing import NamedTuple, Any
from addict import Dict
from aenum import Enum, auto
from .dpathutils import dget, dnew, dpop
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


def OptionsScalesAxes(_cfg, base_path):
    _cfg.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, [('/type', 'line')])  # TODO: this condition will change
    _cfg.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [(f"{base_path}/display", True), (f"{base_path}/display", False)])
    pass


def OptionsScalesAxesGrid(_cfg, base_path, ctx):
    _cfg.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, ctx)
    logger.debug(f"base path {base_path}/display")
    _cfg.color = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [(f'{base_path}/display', True), (f'{base_path}/display',  False)])
    _cfg.borderColor = AttrMeta(
        twt.gray/2, Color, Color, uiorgCat.simple, False, [(f'{base_path}/display', True), (f'{base_path}/display', False)])
    _cfg.tickColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [(f'{base_path}/display', True), (f'{base_path}/display', False)])
    _cfg.circular = AttrMeta(
        None, None, None, uiorgCat.simple, False, [(f'{base_path}/display', True), (f'{base_path}/display', False)])  # from for radar chart


def OptionsPluginsTitle(_cfg):
    _cfg.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, all_context)
    _cfg.text = AttrMeta(
        "plot_title", str, str, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])
    _cfg.align = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])
    _cfg.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])
    _cfg.fullSize = AttrMeta(
        False, bool, bool, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])

    _cfg.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])

    _cfg.padding = AttrMeta(
        10, int, int, uiorgCat.simple, False, [('/options/plugins/title/display', True), ('/options/plugins/title/display', False)])


def OptionsPluginsSubtitle(_cfg):
    _cfg.display = AttrMeta(
        False, bool, bool, uiorgCat.simple, True, all_context)
    _cfg.text = AttrMeta(
        "plot_subtitle", str, str, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])
    _cfg.align = AttrMeta(
        TextAlign.center, TextAlign, TextAlign, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])
    _cfg.color = AttrMeta(
        twt.blue/5, Color, Color, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])
    _cfg.fullSize = AttrMeta(
        False, bool, bool, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])

    _cfg.position = AttrMeta(
        Position.top, Position, Position, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])

    _cfg.padding = AttrMeta(
        10, int, int, uiorgCat.simple, False, [('/options/plugins/subtitle/display', True), ('/options/plugins/subtitle/display', False)])


def OptionsElementsPoint(_cfg):
    _cfg.radius = AttrMeta(3, int, [0, 5], uiorgCat.simple, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.pointStyle = AttrMeta(PointStyle.circle,   PointStyle, PointStyle, uiorgCat.simple, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.rotation = AttrMeta(0, int, int, uiorgCat.advanced, True,  [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.backgroundColor = AttrMeta(
        twt.gray/1, Color, Color, uiorgCat.simple, False, [(
            '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.borderWidth = AttrMeta(1, int, [0, 5], uiorgCat.simple, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.borderColor = AttrMeta(
        twt.gray/4, Color, Color, uiorgCat.simple, False, [(
            '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.hitRadius = AttrMeta(1, int, [0, 5], uiorgCat.nitpick, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.hoverRadius = AttrMeta(4, int, [0, 5], uiorgCat.nitpick, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])
    _cfg.hoverBorderWidth = AttrMeta(1, int, [0, 5], uiorgCat.nitpick, True, [(
        '/type', 'line'), ('/type', 'radar'), ('/type', 'bubble')])


def add_axes_cfgattributes(_axes, base_path):
    """
    _axes: is an axes element. add axes attributes like grid etc.
    """

    # TODO: add other properties as well

    OptionsScalesAxes(_axes, base_path)
    _axes.grid = Dict(track_changes=True)
    OptionsScalesAxesGrid(_axes.grid, f"{base_path}/grid", [
                          (f"{base_path}/display", True), (f"{base_path}/display", False)])


def get_basecfg(choices):
    """generate canonical attrmeta
    choices defines user choices made in  initial setup
    -- mostly for scales
    """

    _base = cfgAttrMeta_base = Dict(track_changes=True)
    _base.type = AttrMeta(choices.plottype, PlotType,
                          PlotType, uiorgCat.initial, True, all_context)

    def Options():
        options = _base.options = Dict(track_changes=True)
        print("post options addition ", _base)

        def Elements():
            elements = options.elements = Dict(track_changes=True)

            def Line():  # called if selected in choice
                linecfg = elements.line = Dict(track_changes=True)
                OptionsElementsLineCfg(linecfg)
            Elements.Line = Line

            def Point():
                point = elements.point = Dict(track_changes=True)
                OptionsElementsPoint(point)
            Elements.Point = Point
            # choose elements based on plot type
            match choices.plottype:
                case 'line' | PlotType.Line:
                    # Elements.Line() #TODO: open up later
                    # Elements.Point() #TODO: open up later
                    pass
        Elements()
        Options.Elements = Elements

        def Plugins():
            plugins = options.plugins = Dict(track_changes=True)

            def Title():
                title = plugins.title = Dict(track_changes=True)
                OptionsPluginsTitle(title)
            Plugins.Title = Title

            def Subtitle():
                subtitle = plugins.subtitle = Dict(track_changes=True)
                OptionsPluginsSubtitle(subtitle)

            Plugins.Subtitle = Subtitle

            def Legend():
                legend = plugins.legend = Dict(track_changes=True)
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
            # all charts will have these
            Title()
            Subtitle()
            Legend()
            # Tooltips()  # open up later
        # Plugins()  #open up later
        Options.Plugins = Plugins

        def Scales():
            scales = options.scales = Dict(track_changes=True)
            # scales.choices = []

            def XAxes(xaxes_type='x'):
                if xaxes_type == 'x':
                    base_path = "/options/scales/x"
                    xAxis = scales.x = Dict(track_changes=True)
                    add_axes_cfgattributes(xAxis, base_path)

                elif isinstance(xaxes_type, list):
                    for eax in xaxes_type:
                        logger.debug(f"now building xaes cfg for {eax}")
                        #xAxis = scales[eax['id']] = Dict(track_changes=True)
                        dnew(scales, eax['id'], Dict(track_changes=True))
                        xAxis = dget(scales, eax['id'])
                        base_path = f"/options/scales/{eax['id']}"
                        add_axes_cfgattributes(xAxis, base_path)
                        logger.debug(dget(_base, "/options/scales/x1/display"))
            # XAxis()

            Scales.XAxes = XAxes
        Scales()
        Options.Scales = Scales
    Options()
    # Options.Plugins.Title()
    # Options.Plugins.Subtitle()
    # Options.Elements.Point()
    # Options.Elements.Line()
    match choices.plottype:
        case 'line' | PlotType.Line:
            # resorting to simple ifs -- types and match is tricky
            Options.Scales.XAxes(choices.scales.xaxes)
            # if choices.scales.xaxes == 'x':
            #     Options.Scales.XAxes()
            # elif isinstance(choices.scale.xaxes, list):
            #     Options.Scales.XAxes(choices.line.xaxes)
            #     pass

        case  'bar':
            pass

        case 'radial':
            pass

    # _base.options.responsive = AttrMeta(
    #     True, bool, bool, uiorgCat.perf, True, all_context)
    # _base.options.aspectRatio = AttrMeta(
    #     2, int, [1, 4], uiorgCat.advanced, True, all_context)
    # _base.options.resizeDelay = AttrMeta(
    #     4, int, [1, 9], uiorgCat.perf, True, all_context)
    # _base.options.devicePixelRatio = AttrMeta(
    #     1, int, [1, 5], uiorgCat.advanced, True, all_context)

    # _base.options.parsing.value = AttrMeta(False, FalseDict,
    #                                        Dict({'x': AttrMeta('x', str, str, uiorgCat.initial,
    #                                                            False, [('/options/parsing/', True)]),
    #                                              'y': AttrMeta('y', str, str,  uiorgCat.initial, False, [('/options/parsing/', True)]),
    #                                              'id': AttrMeta('id', str, str, uiorgCat.initial, False, [('/options/parsing/', True)])
    #                                              }), uiorgCat.TBD, True, all_context)

    # _base.options.parsing.x = AttrMeta(
    #     'x', str, str, uiorgCat.TBD, False, [('options/parsing', True)])  # active only if /options/parsing is True
    # _base.options.parsing.y = AttrMeta(
    #     'y', str, str, uiorgCat.TBD, False, [('options/parsing', True)])
    # _base.options.parsing.id = AttrMeta('id', str, str, uiorgCat.TBD, False, [
    #     ('options/parsing', 'True')])

    return _base

# ==================== end get_baseCfgAttrMeta ===================
