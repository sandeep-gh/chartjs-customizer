"""wrapper over dpath.util to 
"""
import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

#from jsonpath_ng import jsonpath, parse
from dpath.util import get as dpath_get, new as dpath_new, delete as dpath_delete
from addict import Dict

# def locate(dictobj, dpath):
#     if "." in dpath:
#         raise ValueError(f"symbol . not allowed in  {dpath}")
#     arr = dpath.split("/")
#     if arr[0] == "":
#         arr[0] = "$"
#     else:
#         arr.insert(0, "$")
#     path = ".".join(arr)

#     jsonpath_expr = parse(path)
#     res = [match
#            for match in jsonpath_expr.find(dictobj)]
#     if len(res) == 0:
#         raise ValueError(f"no path: {path} exists in {dictobj}")
#     if len(res) > 1:
#         raise ValueError(f"More than one path matched for {path} in {dictobj}")
#     return res[0].value


def dget(dictobj, dpath):
    return dpath_get(dictobj, dpath)


def dnew(dictobj, dpath, value):
    if '[' in dpath and ']' in dpath:
        raise ValueError(f"cannot process array in {dpath}")

    dpath_new(dictobj, dpath, value)


def dpop(dictobj, dpath):
    if '[' in dpath and ']' in dpath:
        raise ValueError(f"cannot process array in {dpath}")

    dpath_delete(dictobj, dpath)


def list_walker(alist, ppath="", guards=None, internal=False):
    """
    to be used in conjuction with walker; navigates the list
    part of the dict.
    todo; make guards over list part
    """
    if internal:
        yield (f"{ppath}/__arr", len(alist))
    for i, value in enumerate(alist):
        if isinstance(value, dict):
            yield from walker(value, ppath + f"/{i}", guards=guards, internal=internal)
        elif isinstance(value, list):
            yield from list_walker(value,  ppath + f"/{i}", guards=guards, internal=internal)


def walker(adict, ppath="", guards=None, internal=False):
    """
    if internal is True; __arr path will be exposed

    """
    for key, value in adict.items():
        try:
            if guards:
                if f"{ppath}/{key}" in guards:
                    print(f"stoping at guard for {key}")
                    yield (f"{ppath}/{key}", value)
                    continue  # stop at the guard
            if isinstance(value, dict):
                yield from walker(value, ppath + f"/{key}", guards=guards, internal=internal)
            elif isinstance(value, list):
                yield from list_walker(value, ppath + f"/{key}", guards=guards, internal=internal)

            else:
                yield (f"{ppath}/{key}", value)
                pass

        except Exception as e:
            print(f"in walker exception {ppath} {key} {e}")
            raise ValueError


def stitch_from_dictiter(from_iter):
    """create/stitch a dictionary back from paths obtained from from_dictwalker after apply
    from
    """
    res_dict = Dict()
    arr_kpaths = {}
    for kpath, val in from_iter:
        if "__arr" in kpath:

            # TODO: not the best approach; use list constructor
            logger.debug(f"arr_create {kpath[:-6]}")
            dnew(res_dict, kpath[:-6], [Dict() for _ in range(val)])
            # arr_kpaths[kpath] = dget(res_dict, kpath)
            logger.debug(f"saw __arr in {kpath}")
        else:
            if val is not None:
                # if kpath in arr_kpaths:
                #     ppath, idx = get_path_idx(kpath)
                #     arr_kpaths[ppath].apppend(val)
                dnew(res_dict, kpath, val)
    return res_dict
