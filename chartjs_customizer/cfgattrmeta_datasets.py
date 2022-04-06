

from addict import Dict
from .attrmeta_basecfg_orig import OptionsElementsLineCfg, OptionsElementsPoint


def add_datacfg(cfg, datasets):
    """
    add configurations for each data in datasets
    """

    cfg.data.datasets = []
    for data in datasets:
        datacfg = Dict(track_changes=True)
        DatasetsDataCfg(datacfg)
        #datacfg.line = Dict(track_changes=True)
        # OptionsElementsLineCfg(datacfg.line)
        #datacfg.point = Dict(track_changes=True)
        # OptionsElementsPoint(datacfg.point)
        cfg.data.datasets.append(datacfg)

    pass
