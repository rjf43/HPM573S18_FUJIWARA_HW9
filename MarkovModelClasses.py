import scr.SamplePathClasses as Path
import scr.StatisticalClasses as Stat
import scr.RandomVariantGenerators as Rand
import ParameterClasses as Parameter
import Inputs as Inputs

class Patient:
    def __init__(self, id, parameters):
        """ initialize a single patient"""

        self._id = id
        self._rng = None # random number generator
        self._parameters = parameters # parameters
        self._stateMonitor = PatientStateMonitor(parameters)
        self._delta_t = parameters.get_delta_t()

    def simulate(self, sim_length):
        """ simulate the single patient over a simulation length"""

        # random number generator for this patient
        self._rng = Rand.RNG(self._id)

        k = 0 # current time step

        # while the patient is alive and the simulation length is not yet reached
        while self._stateMonitor.get_if_alive() and k*self._delta_t < sim_length:

            # find the transition probabilities of the future states
            trans_prob = self._parameters.get_transition_prob(self._stateMonitor.get_current_state())
            # create an empirical distribution
            empirical_dist = Rand.Empirical(trans_prob)
            # sample from the empirical distribution to get a new state
            new_state_index = empirical_dist.sample(self._rng)

            # update health state
            self._stateMonitor.update(k, Parameter.HealthState(new_state_index))

            # increment time step
            k +=1

    def get_survival_time(self):
        return self._stateMonitor.get_survival_time()

    def get_number_strokes_individual(self):
        return self._stateMonitor.get_number_strokes()

class PatientStateMonitor:
    """ to update patient outcomes throughout the simulation"""
    def __init__(self, parameters):

        self._currentState = parameters.get_initial_health_state()
        self._delta_t = parameters.get_delta_t()
        self._survivalTime = 0
        self._numberStrokes = 0

    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state
        """
        # if patient has died, do nothing
        if not self.get_if_alive():
            return

        # update survival time
        if next_state == Parameter.HealthState.DEAD:
            self._survivalTime = (k+0.05)*self._delta_t

        # update the number of strokes
        if next_state == Parameter.HealthState.STROKE:
            self._numberStrokes += 1

        # update current health state
        self._currentState = next_state

    def get_if_alive(self):
        result = True
        if self._currentState == Parameter.HealthState.DEAD:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def get_survival_time(self):
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None

    def get_number_strokes(self):
        return self._numberStrokes

class Cohort:
    def __init__(self, id, therapy):
        """ create a cohort of patients"""

        self._initial_pop_size = Inputs.SIM_PATIENTS
        self._patients = []

        # populate the cohort
        for i in range(self._initial_pop_size):
            # create a new patient
            patient = Patient(id*self._initial_pop_size+i, Parameter.ParametersFixed(therapy))
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self):
        # simulate all patients
        for patient in self._patients:
            patient.simulate(Inputs.TIME_STEPS)

        # return the cohort outputs
        return CohortOutput(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients

class CohortOutput:
    def __init__(self, simulated_cohort):

        self._survivalTimes = []
        self._numberStrokes_cohort = []

        # survival curve
        self._survivalCurve = \
            Path.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # get the patient survival time
            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)
                self._survivalCurve.record(survival_time, -1)

        # summary statistic
        self._sumStat_survivalTime = Stat.SummaryStat('Patient survival time', self._survivalTimes)

        # find patients' number of strokes
        for patient in simulated_cohort.get_patients():
            self._numberStrokes_cohort.append(patient.get_number_strokes_individual())

        # summary statistic of strokes
        self._sumStat_numberStrokes = Stat.SummaryStat('Patient number of strokes', self._numberStrokes_cohort)

    def get_survival_times(self):
        return self._survivalTimes

    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime

    def get_survival_curve(self):
        return self._survivalCurve

    def get_number_strokes(self):
        return self._numberStrokes_cohort