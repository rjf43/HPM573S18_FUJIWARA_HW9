import MarkovModelClasses as MarkovModel
import ParameterClasses as Parameters
import MarkovSupport as Support

# create a cohort
Cohort = MarkovModel.Cohort(
    id= 1,
    therapy= Parameters.Therapy.NONE
)

# simulate the cohort
CohortSim = Cohort.simulate()

# print outcomes
Support.print_outcomes('No anticoagulation', CohortSim)