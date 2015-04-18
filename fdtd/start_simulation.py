"""
Startsimulation.m
"""
import fdtd.interactive_fdtd as interactive_fdtd
import fdtd.define_general_parameters as dgp

PARAMS = dgp.PARAMS

interactive_fdtd.ANSWER_SIM[7] = interactive_fdtd.SCALE_FACTOR_2

NUM_LINES = 1
DEFAULT_ANSWER = interactive_fdtd.ANSWER_SIM

# answersim2 = user input
# if no user input, use defaults

PLOT_VARS = [0 for _ in range(10)]

PLOT_VARS[0] = interactive_fdtd.ANSWER_SIM[1]
PLOT_VARS[1] = interactive_fdtd.ANSWER_SIM[0]
PLOT_VARS[2] = interactive_fdtd.ANSWER_SIM[2]
PLOT_VARS[3] = interactive_fdtd.ANSWER_SIM[3]
PLOT_VARS[4] = interactive_fdtd.ANSWER_SIM[7]
PLOT_VARS[5] = interactive_fdtd.ANSWER_SIM[5]

PLOT_VARS[7] = interactive_fdtd.ANSWER_SIM[8]
PLOT_VARS[8] = interactive_fdtd.ANSWER_SIM[9]
PLOT_VARS[9] = interactive_fdtd.ANSWER_SIM[4]

ANZEIGE = interactive_fdtd.ANSWER_SIM[6]
if ANZEIGE == 0:
    ANZ = dgp.PMLWIDTH + 1
elif ANZEIGE == 1:
    ANZ = 1

# PML Vorkehrungen
PARAMS.set_x_arr(-max(PARAMS.get_x_arr()) * PARAMS.del_x,
                 max(PARAMS.get_x_arr()) + dgp.PMLWIDTH * PARAMS.del_x,
                 len(PARAMS.get_x_arr()) + 2 * dgp.PMLWIDTH)
PARAMS.set_y_arr(-max(PARAMS.get_y_arr()) * PARAMS.del_y,
                 max(PARAMS.get_y_arr()) + dgp.PMLWIDTH * PARAMS.del_y,
                 len(PARAMS.get_y_arr()) + 2 * dgp.PMLWIDTH)
PARAMS.set_grid()
