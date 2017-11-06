# configuration parser
import json


def get_params(fn):
    class Parameters(object):
        pass

    data = json.loads(open(fn, "r").read())
    ps = Parameters()

    for key in data.keys():
        setattr(ps, key, data[key])

    return ps