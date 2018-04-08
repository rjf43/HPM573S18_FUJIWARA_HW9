import Q3 as NoneAnticoag
import Q5 as Anticoag
import scr.SamplePathClasses as Path

# generate sample paths
x = NoneAnticoag.CohortSim.get_survival_curve()
y = Anticoag.CohortAnticoagSim.get_survival_curve()

# graph the survival curves
Path.graph_sample_paths(
    sample_paths= [x, y],
    title= 'Survival curve',
    x_label= 'Simulation time steps',
    y_label= 'Number of alive patients',
    legends= ['No anticoagulation', 'Anticoagulation']
)