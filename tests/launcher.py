#from chartjs_customizer.getChartdata_sbs_wp import launcher
from chartjs_customizer.dashboard_step_by_step import launcher
#from chartjs_customizer.just_chartjs_plt import launcher
import justpy as jp

app = jp.app
jp.justpy(launcher, start_server=False)
