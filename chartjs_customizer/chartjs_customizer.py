"""main entry point to chartjs customizer
"""
import traceback
import logging
import os
if logging:  # pin code here so that ide doesn't move around the import statements
    try:
        os.remove("chartjs_customizer.log")
    except:
        pass
    logging.basicConfig(filename="chartjs_customizer.log", level=logging.DEBUG)

if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict

import justpy as jp

import webapp_framework as wf
from .attrmeta import get_basecfg, uiorgCat
from .chartcfg import (add_dataset, build_pltcfg, update_cfgattrmeta,
                       update_chartCfg)
from dpath.util import get as dget, set as dset,  new as dnew, search as dsearch

from addict import Dict
from aenum import extend_enum, auto
import jsbeautifier
from .chartjs_customizer_components import cfggroup_panel_
import json

# ========================== init cjs_cfg =========================
# chartjs configuration as nested-addict-AttrMeta
cfgAttrMeta = get_basecfg()
# cjs_cfg: Json version of cfgAttrMeta
cjs_cfg = Dict(track_changes=True)
update_chartCfg(cfgAttrMeta, cjs_cfg)
cfgAttrMeta.clear_changed_history()

add_dataset(cjs_cfg)
dnew(cjs_cfg, "/data/labels", "[1,2,4,5]")
dset(cjs_cfg, "/type", "line")
update_cfgattrmeta(cjs_cfg, cfgAttrMeta)
update_chartCfg(cfgAttrMeta, cjs_cfg)
cfgAttrMeta.clear_changed_history()
cjs_cfg.clear_changed_history()

# ================================ end ===============================
extend_enum(wf.ReactTag_UI, 'UpdateChart', 'UpdateChart')


def page_body(wp: jp.WebPage):
    """
    webpage body content
    """
    dbref_span = wf.Span_("testing", "testing")(wp, "")
    cfggroup_panel_(uiorgCat.all, cjs_cfg, cfgAttrMeta)
    opts = jsbeautifier.default_options()
    #print(jsbeautifier.beautify(json.dumps(stubStore), opts))
    #print(jsbeautifier.beautify(json.dumps(cjs_cfg), opts))
    # print(cjs_cfg)
    wf.Container_(cgens=[stubStore.uiorg_all.topPanel])(wp)


@jp.SetRoute('/customize_chartjs')
def launcher(request):
    wp = wf.WebPage_("wp_index", page_type='quasar', head_html_stmts=[
        """<script src = "https://cdn.jsdelivr.net/npm/chart.js"></script >"""])()
    logging.info("this is info")
    logging.debug("this is debug")
    #wp = jp.QuasarPage()
    #wp.tailwind = False
    # wp.head_html = """
    # \n
    # <script src="https://cdn.tailwindcss.com/"></script>
    # <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css">
    # """

    # ================ initialize chart and ui configs ===============
    try:
        page_body(wp)
    except Exception as e:
        print("error occured ", e)
        traceback. print_exc()
        raise e
    return wp
