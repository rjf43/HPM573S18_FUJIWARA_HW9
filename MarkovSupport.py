import Inputs as Inputs
import scr.FormatFunctions as Format

def print_outcomes(therapy, simulation_output):
    """
    :param therapy: whether patient received anticoagulation
    :param simulation_output: simulated output
    :return: print the outcomes
    """

    # mean and confidence interval text of patient survival time
    survival_mean_CI = Format.format_estimate_interval(
        estimate= simulation_output.get_sumStat_survival_times().get_mean(),
        interval= simulation_output.get_sumStat_survival_times().get_t_CI(Inputs.ALPHA),
        deci=2
    )

    # print
    print(therapy)
    print('Estimate of mean survival time and {:.{prec}%} CI:'.format(1-Inputs.ALPHA, prec=0),
          survival_mean_CI)