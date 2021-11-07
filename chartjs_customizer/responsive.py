# handle ui changes to options being selected

cfgattr = None


def update_cfg_attrMeta(kpath, val):
    match(kpath, val):
        case("/options/scales/xAxis/grid/display", True):
            _ = cfgattr.options.scales.xAxis.grid
            _.grid.color = CfgattrMeta("", Color, Color, CPT.simple)
            _.grid.borderColor = CfgattrMeta("", Color, Color, CPT.nitpick)
            _.grid.tickColor = CfgattrMeta("", Color, Color, CPT.simplemore)
            _.grid.circular = CfgattrMeta(
                None, None, None, CPT.TBD)  # from for radar chart

        case("/options/scales/xAxis/grid/display", False):
            _ = cfgattr.options.scales.xAxis.grid
            _.grid.pop(color, None)
            _.grid.pop(borderColor, None)
            _.grid.pop(tickColor, None)
            _.grid.pop(circular, None)


def update_chartCfg(cfgattrmeta, cfgchart):
    for key in cfgattrmeta.get_changed_history():
        attrMeta = dget(cfgattrmeta, key)
        evalue = cfgattreval(key, value, colorbank)
        if evalue is not None:
            setattr(cfgchart, key, evalue)


def update_uic(cfgchart):
    for key in cfgchart.get_changed_history():
        tlkey, tier1key = get_ui_category(key)
        if tier1key is None:
            dbref_target_container = dget(refBoard, tlkey)
        else:
            dbref_target_container = dget(refBoard, f"{tlkey}/{tier1key}")
        dbref_target_container.addItems(
            build_uic(key, label, attrMeta, refBoard))
