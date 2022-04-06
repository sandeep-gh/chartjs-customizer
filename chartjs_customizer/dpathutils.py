"""use json-ng to provide same functionality as dpath.util
"""
#from jsonpath_ng import jsonpath, parse
from dpath.util import get as dpath_get, new as dpath_new, delete as dpath_delete


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


def list_walker(alist, ppath="", guards=None):
    """
    to be used in conjuction with walker; navigates the list
    part of the dict.
    todo; make guards over list part
    """
    for i, value in enumerate(alist):
        if isinstance(value, dict):
            yield from walker(value, ppath + f"/{i}", guards=guards)
        elif isinstance(value, list):
            yield from list_walker(value,  ppath + f"/{i}", guards=guards)


def walker(adict, ppath="", guards=None):
    for key, value in adict.items():
        try:
            if guards:
                if f"{ppath}/{key}" in guards:
                    print(f"stoping at guard for {key}")
                    yield (f"{ppath}/{key}", value)
                    continue  # stop at the guard
            if isinstance(value, dict):
                yield from walker(value, ppath + f"/{key}", guards=guards)
            elif isinstance(value, list):
                yield from list_walker(value, ppath + f"/{key}", guards=guards)

            else:
                yield (f"{ppath}/{key}", value)
                pass

        except Exception as e:
            print(f"in walker exception {ppath} {key} {e}")
            raise ValueError
