# Simulation parameters
SIM_PATIENTS = 2000 # cohort size
TIME_STEPS = 50 # duration of simulation
ALPHA = 0.05 # significance level
DELTA_T = 1 # years

# transition matrix
TRANS_PROB_MATRIX = [
    [0.75,  0.15,   0.0,    0.1], # Well
    [0.0,   0.0,    1.0,    0.0], # Stroke
    [0.0,   0.25,   0.55,   0.2], # Post-stroke
    [0.0,   0.0,    0.0,    1.0]  # Dead
    ]

# treatment relative risks
RR_DECREASED_STROKE_DEATH =  0.65
RR_DEATH = 1.05
