"""use json-ng to provide same functionality as dpath.util
"""
from jsonpath_ng import jsonpath, parse
from dpath.util import new as dpath_new, delete as dpath_delete


def locate(dictobj, dpath):
    if "." in dpath:
        raise ValueError(f"symbol . not allowed in  {dpath}")
    print("dpath = ", dpath)
    arr = dpath.split("/")
    print("arr = ", arr)
    if arr[0] == "":
        arr[0] = "$"
    else:
        arr.insert(0, "$")
    path = ".".join(arr)

    print(f"dget path = {path}")
    jsonpath_expr = parse(path)
    res = [match
           for match in jsonpath_expr.find(dictobj)]
    if len(res) == 0:
        raise ValueError(f"no path: {path} exists in {dictobj}")
    if len(res) > 1:
        raise ValueError(f"More than one path matched for {path} in {dictobj}")
    return res[0].value


def dget(dictobj, dpath):
    return locate(dictobj, dpath)


def dnew(dictobj, dpath, value):
    if '[' in dpath and ']' in dpath:
        raise ValueError(f"cannot process array in {dpath}")

    dpath_new(dictobj, dpath, value)


def dpop(dictobj, dpath, value):
    if '[' in dpath and ']' in dpath:
        raise ValueError(f"cannot process array in {dpath}")

    dpath_delete(dictobj, dpath, value)


def walker(adict, ppath="", guards=None):

    for key, value in adict.items():
        try:
            if guards:
                if f"{ppath}/{key}" in guards:
                    print(f"stoping at guard for {key}")
                    yield (f"{ppath}/key", value)
                    continue  # stop at the guard
            if isinstance(value, dict):
                yield from walker(value, ppath + f"/{key}", guards=guards)
            elif isinstance(value, list):
                for i, value in enumerate(value):
                    yield from walker(value, ppath + f"/{key}[{i}]", guards=guards)
            else:
                yield (f"{ppath}/{key}", value)
                pass

        except Exception as e:
            print(f"in walker exception {ppath} {key} {e}")
            raise ValueError
