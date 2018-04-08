import ParameterClasses as Parameters
import Inputs as Inputs

# print the transition probability matrix with anticoagulation
print(Parameters.calculate_prob_matrix_anticoag(
    matrix_no_anticoag= Inputs.TRANS_PROB_MATRIX,
    rr_strokeORdeath= Inputs.RR_DECREASED_STROKE_DEATH,
    rr_bleeding= Inputs.RR_DEATH)
)
