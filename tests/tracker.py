import functools
from addict import Dict
import jsbeautifier
import logging
import json

from webapp_framework_extn import dbrefBoard

logger = logging.getLogger(__name__)

_hcs = Dict()
refBoard = Dict()
_currTracker = _hcs
_currSpath = "/"
session_dict = {}


# def build_hcdbref():
#     """build a replica for _hcs
#     but with values as dbref instead of stub
#     """
#     hcdbref = Dict()
#     for k, v in walker(_hcs):
#         dnew(hcdbref, k, v.key)

#     return hcdbref


# def get_sref(spath):
#     return dget(_currTracker, spath)


# def get_dbref(spath):
#     """spath: stub path
#     """
#     hcgen = dget(_currTracker, spath)

#     return hcgen.target

def save_sty(model: Dict, arg: Dict):
    logger.debug("In save sty")
    styreport = session_dict['styj']
    opts = jsbeautifier.default_options()
    res = jsbeautifier.beautify(json.dumps(session_dict['styj']), opts)
    with open("styreport.json", "w") as fh:
        fh.write(res)
    pass


def load_sty(model: Dict, arg: Dict):
    logger.debug("loading sty")
    with open("styreport.json", "r") as fh:
        session_dict['styj'] = Dict(json.loads(fh.read()))


class uictx:
    def __init__(self, ctx, **kwargs):

        self.ctx = ctx
        pass

    def __enter__(self):
        global _currTracker
        global _currSpath
        if self.ctx not in _currTracker:
            _currTracker[self.ctx] = Dict()
        self.pctx = _currTracker
        self.pspath = _currSpath
        _currTracker = _currTracker[self.ctx]
        _currSpath = _currSpath + f"{self.ctx}/"
        return _currTracker

    def __exit__(self, type, value, traceback):
        global _currTracker
        global _currSpath
        _currTracker = self.pctx
        _currSpath = self.pspath
        pass


def hcGen_register(func):
    @functools.wraps(func)
    def hcGen_wrapper(*args, **kwargs):
        """
        wrapper for _f/generator function in htmlcomponents
        """
        if args and args[0] == None:  # skip the _f(None, None) call
            return func(*args, **kwargs)

        hcref = func(
            *args, **kwargs)  # this is the chance to add dbref to dbrefBoard
        # we store the stub/func; use func.target
        #print("register ", func, " ", hcref.stub, " ", hcref.key)
        # TODO: pick it up: its a mystry why func !=
        #dbrefBoard.register(refBoard, func, hcref)
        dbrefBoard.register(refBoard, hcref.stub, hcref)
        return hcref

    return hcGen_wrapper


def register(func):
    """
    register the stub in _hcs/stubStore
    """
    @functools.wraps(func)
    def stubGen_wrapper(*args, **kwargs):
        hcgen = func(*args, **kwargs)
        _currTracker[hcgen.key] = hcgen
        hcgen.spath = _currSpath + hcgen.key
        return hcgen

    return stubGen_wrapper
