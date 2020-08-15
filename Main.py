## Import built packages ##
from pyomo.environ import *

## Import model components ##
import Sets as fset
import Parameters as fpar
import Variables as fvar
import Constraints as fcon
import Auxiliary_Functions as faux


def data_construction(file_name):
    """
    This function constructs the input data object
    """
    # load the sets
    g = ['Maersk']
    i = ['A', 'B', 'C', 'D']
    j = ['A', 'B', 'C', 'D']
    o = ['A']
    d = ['D']
    l = ['Diesel', 'Electric']
    c = ['20ft', '40ft']
    w = ['40ft', '60ft']
    t = [n for n in range(0, 49)]

    set_input = faux.SetInput(g, i, j, o, d, l, c, w, t)

    # Maximum number of wagons on each service
    WMAX = 30

    # load single-dimension parameters of set 'i'
    P = faux.read_par_from_excel(file_name, '1DPar_i', (2, 'A'), (6, 'B'), 1)
    NC = faux.read_par_from_excel(file_name, '1DPar_i', (2, 'A'), (6, 'C'), 1)
    NL = faux.read_par_from_excel(file_name, '1DPar_i', (2, 'A'), (6, 'D'), 1)
    NW = faux.read_par_from_excel(file_name, '1DPar_i', (2, 'A'), (6, 'E'), 1)

    # load asset ownership information
    OL = faux.read_par_from_excel(file_name, '1DPar_OL', (2, 'A'), (4, 'B'), 1)
    OW = faux.read_par_from_excel(file_name, '1DPar_OW', (2, 'A'), (4, 'B'), 1)

    # load feasible routes bool
    FR = faux.read_par_from_excel(file_name, '2DPar_FR', (2, 'A'), (18, 'C'), 2)

    # load journey time of feasible legs
    H = faux.read_par_from_excel(file_name, '2DPar_H', (2, 'A'), (18, 'C'), 2)
    H = {key: val for key, val in H.items() if val != 0}

    # load initial number of stationary wagons and locomotives at each node
    M_init = faux.read_par_from_excel(file_name, '2DPar_M0', (2, 'A'), (10, 'C'), 2)
    WS_init = faux.read_par_from_excel(file_name, '2DPar_lw0', (2, 'A'), (10, 'C'), 2)

    # Load cost information
    FC = faux.read_par_from_excel(file_name, '3DPar_FC', (2, 'A'), (34, 'D'), 3)
    FC = {key: val for key, val in FC.items() if val != 0}
    VC = faux.read_par_from_excel(file_name, '3DPar_VC', (2, 'A'), (34, 'D'), 3)
    VC = {key: val for key, val in VC.items() if val != 0}

    # Load Delivery time information
    tau = faux.read_par_from_excel(file_name, '3DPar_Tau', (2, 'A'), (3, 'D'), 3)

    # Load Delivery time information
    S = faux.read_par_from_excel(file_name, '5DPar_S', (2, 'A'), (100, 'F'), 5)

    fixed_var = faux.ParaFixedInput(FR, tau, H, OL, OW, NC, NL, NW)

    variable_par = faux.ParaVarInput(FC, VC, P, WMAX, S, M_init, WS_init)

    return set_input, fixed_var, variable_par


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    # initialise the concreteModel
    RSO_model = ConcreteModel()

    # get the data input as objects
    file_name = 'Pyomo_RSO_Parameter_Input.xlsx'
    set_input, fixed_par, variable_par = data_construction(file_name)

    # set initialisation
    fset.set_initialisation(RSO_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(RSO_model, fixed_par, variable_par)

    # variable initialisation
    fvar.variable_initialisation(RSO_model)

    # constraint initialisation
    fcon.constraint_definition(RSO_model)

    # set up the model
    opt = SolverFactory('gurobi')

    results = opt.solve(RSO_model, tee=True, symbolic_solver_labels=True)

    RSO_model.solutions.store_to(results)

    results.write(filename='solution.yml')


if __name__ == '__main__':
    main()
