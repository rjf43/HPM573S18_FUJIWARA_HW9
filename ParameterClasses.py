from enum import Enum
import Inputs as Inputs

class HealthState(Enum):
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEAD = 3

class Therapy(Enum):
    NONE = 0
    ANTICOAG = 1

class ParametersFixed:
    def __init__(self, therapy):

        self._delta_t = Inputs.DELTA_T # simulation time steps
        self._initialHealthState = HealthState.WELL # initial health state
        self._therapy = therapy

        # transition probability matrix
        self._prob_matrix = calculate_prob_matrix_no_anticoag()

        # update the probability matrix if on anticoagulation
        if self._therapy == Therapy.ANTICOAG:
            # treatment relative risk of decreased stroke or stroke death
            self._rr_strokeOrDeath = Inputs.RR_DECREASED_STROKE_DEATH
            self._rr_death = Inputs.RR_DEATH
            # calculate treatment probability matrix
            self._prob_matrix = calculate_prob_matrix_anticoag(
                matrix_no_anticoag= self._prob_matrix,
                rr_strokeORdeath= self._rr_strokeOrDeath,
                rr_bleeding= self._rr_death
            )
    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

def calculate_prob_matrix_no_anticoag():
    return Inputs.TRANS_PROB_MATRIX

def calculate_prob_matrix_anticoag(matrix_no_anticoag, rr_strokeORdeath, rr_bleeding):
    """ generates probability matrix if on anticoagulation"""

    # generate empty matrix
    matrix_anticoag = []
    for i in matrix_no_anticoag:
        matrix_anticoag.append([0] * len(i))

    # populate the anticoagulation matrix
    # for WELL, STROKE, and DEAD rows of transition probability matrix
    for j in HealthState:
        for i in HealthState:
            if i != HealthState.POST_STROKE:
                matrix_anticoag[i.value][j.value] = matrix_no_anticoag[i.value][j.value]

    # for POST-STROKE row of transition probability matrix
    x = HealthState.POST_STROKE.value

    # temporarily replace entire POST-STROKE row accounting for relative risk of decreased stroke or death
    for j in HealthState:
        matrix_anticoag[x][j.value] = matrix_no_anticoag[x][j.value] * rr_strokeORdeath

    # account for increased risk of bleeding
    matrix_anticoag[x][HealthState.DEAD.value] = \
        matrix_anticoag[x][HealthState.DEAD.value] * rr_bleeding

    # ensure that POST-STROKE transition probabilities equal 1
    total = 0
    for j in HealthState:
        if j.value != x:
            total += matrix_anticoag[x][j.value]
    matrix_anticoag[x][x] = 1 - total

    return matrix_anticoag


