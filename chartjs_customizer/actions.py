from chart_ui_cfg import update_chartCfg, update_cfgattrmeta


def update_ui_component():
    """
    update ui on ui state change;
    eventually this should be called update_ui only
    """
    wf.refresh(refBoard_)
    for kpath, attrmeta in cfggroup_iter():
        if attrmeta.active:
            if dget(cjs_cfg, kpath) != refBoard_[kpath].val:
                print(f"update chartcfg {kpath}")
                wf.dupdate(cjs_cfg, kpath, refBoard_[kpath].val)

    update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
    for kpath in cfgAttrMeta.get_changed_history():
        attrmeta = dget(cfgAttrMeta, kpath)
        dbref = refBoard_[kpath]._go.target
        if attrmeta.active and 'hidden' in dbref.classes:
            dbref.remove_class("hidden")
            print(kpath, " ", dbref.classes)
        elif not attrmeta.active and not 'hidden' in dbref.classes:
            dbref.set_class("hidden")
