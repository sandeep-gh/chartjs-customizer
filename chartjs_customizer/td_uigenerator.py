from
chartdata_initialcfg = Dict()
cfg.options.parsing.xAxisKey = CfgattrMeta(
    'x', str, str, CPT.required)

cfg.options.parsing.yAxisKey = CfgattrMeta(
    'y', str, str, CPT.required)
cfg.type = CfgattrMeta(
    'line', str, ['line', 'bar'], CPT.required)


generator(CPT.required)
