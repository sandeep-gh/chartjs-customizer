from addict import Dict
from chartjs_customizer.responsive import Color, AttrMeta, CPT, update_cfg_attrMeta


cfgMeta = Dict(track_changes=True)

cfgMeta.options.scales.xAxis.grid.display = False
_ = cfgMeta.options.scales.xAxis

_.grid.color = AttrMeta("", Color, Color, CPT.simple, True)
_.grid.borderColor = AttrMeta("", Color, Color, CPT.nitpick, True)
_.grid.tickColor = AttrMeta("", Color, Color, CPT.simplemore, True)
_.grid.circular = AttrMeta(
    None, None, None, CPT.TBD, True)  # from for radar chart

cfgMeta.clear_changed_history()


def iter_cfgMeta(cfgMeta, prefix=""):
    for attr, val in cfgMeta.items():
        if isinstance(val, Dict):
            yield from iter_CfgMeta(val, f"{prefix}/{attr}")
        else:
            yield (f"{prefix}/{attr}", val)


def build_chart_ui_cfg(cfgMetaIter):
    chartcfg = Dict()
    uicfg = Dict()
    for kpath, attrMeta in cfgMetaIter:
        is_disabled, default_val = attrMeta_eval(cfgMetaIter)
        dset(kpath, uicfg, [is_disabled, default_val])
        if not is_disabled:
            dset(kpath, chartcfg, default_val)

    return [uicfg, chartcfg]


update_cfg_attrMeta("/options/scales/xAxis/grid/display", True, cfgMeta)

for kpath in cfgMeta.get_changed_history():
    print(kpath)
