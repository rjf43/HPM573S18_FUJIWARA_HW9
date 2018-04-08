import Q3 as NoAnticoag
import Q5 as Anticoag
import scr.FigureSupport as Fig

NoAnticoag = NoAnticoag.CohortSim.get_number_strokes()
Anticoag = Anticoag.CohortAnticoagSim.get_number_strokes()

# generate histograms
Fig.graph_histograms(
    data_sets= [NoAnticoag, Anticoag],
    title= 'Number of strokes',
    x_label= 'Number of strokes',
    y_label= 'Number of patients',
    legend= ['No Anticoagulation', 'Anticoagulation']
)
