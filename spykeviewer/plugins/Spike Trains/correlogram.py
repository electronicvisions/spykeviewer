import quantities as pq
import neo

from spykeutils.plugin import analysis_plugin, gui_data
from spykeutils import plot

class CorrelogramPlugin(analysis_plugin.AnalysisPlugin):
    bin_size = gui_data.FloatItem('Bin size', 1.0, 0.1, 10000.0, unit='ms')
    cut_off = gui_data.FloatItem('Cut off', 50.0, 2.0, 10000.0, unit='ms')
    data_source = gui_data.ChoiceItem('Data source', ('Units', 'Selections'))
    count_per = gui_data.ChoiceItem('Counts per', ('Second', 'Segment'))
    border_correction = gui_data.BoolItem('Border correction', default=True)

    def get_name(self):
        return 'Correlogram'

    def start(self, current, selections):
        current.progress.begin('Creating correlogram...')
        if self.data_source == 0:
            d = current.spike_trains_by_unit()
        else:
            # Prepare dictionary for correlogram():
            # One entry of spike trains for each selection
            d = {}
            for s in selections:
                d[neo.Unit(s.name)] = s.spike_trains()

        plot.cross_correlogram(d, self.bin_size*pq.ms,
            self.cut_off*pq.ms, self.border_correction,
            self.count_per == 0,
            progress=current.progress)





