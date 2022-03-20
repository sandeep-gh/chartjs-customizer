import os
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import pprint
from itertools import chain

import webapp_framework as wf
import webapp_framework_extn as wfx
#from .attrmeta import get_basecfg, uiorgCat, FalseDict
from .attrmeta_basecfg_helper import uiorgCat, FalseDict
from .attrmeta_basecfg import get_basecfg
from .cfgattr_uic import build_uic_iter
from addict import Dict, walker as dictWalker
if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict, refBoard

cfgAttrMeta = get_basecfg()


def cfgattr_groupInitial():
    """
        iterator over attrmeta belonging to uiorgCat.initial
    """
    def is_in_group(kpath, attrmeta):
        # if 'parsing' in kpath:
        #     logger.debug(f"typecheck {type(attrmeta.vrange)} ")
        # # if isinstance(attrmeta.vtype,  FalseDict):
        # if kpath in '/options/parsing/value':
        #     filter(lambda _: is_in_group(
        #         _[0], _[1]), dictWalker(attrmeta.vrange))
        # if 'parsing' in kpath:
        #    logger.debug(f"evaluation {kpath} {attrmeta} ")

        if attrmeta.group == uiorgCat.initial:  # TODO: should we filter based on is_active
            if "/type" in kpath:
                return True

        return False
    yield from filter(lambda _: is_in_group(_[0], _[1]), dictWalker(cfgAttrMeta))


def on_submit_click(dbref, msg):
    print("go  on ...build the chart")


submit_ = wf.Wrapdiv_(wf.Button_(
    "Submit",  "Submit", "Build Chart", on_submit_click))


def no_action(dbref, msg):
    pass


uic_iter = build_uic_iter(cfgattr_groupInitial()
                          )

wf.Subsection_("cfghcs", "Initial Configuration",
               wf.StackW_("attrhc",
                          build_uic_iter(
                              cfgattr_groupInitial()
                          )
                          )
               )
wf.StackV_("topPanel", cgens=[
           stubStore.cfghcs, submit_])
