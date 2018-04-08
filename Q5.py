import MarkovModelClasses as MarkovModel
import ParameterClasses as Parameters
import MarkovSupport as Support

# generate a cohort
CohortAnticoag = MarkovModel.Cohort(
    id = 2,
    therapy= Parameters.Therapy.ANTICOAG
)

# simulate the anticoagulated cohort
CohortAnticoagSim = CohortAnticoag.simulate()

# print survival
Support.print_outcomes('Anticoagulation', CohortAnticoagSim)