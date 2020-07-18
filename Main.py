## Import built packages ##
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition

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
    t = [n for n in range(0,49)]

    set_input = faux.SetInput(g, i, j, o, d, l, c, w, t)

    # load single-dimension parameters of set 'i'
    P = faux.read_par_from_excel('Pyomo_RSO_Parameter_Input.xlsx','1DPar_i', (2, 'A'), (6, 'B'), 1)
    NC = faux.read_par_from_excel('Pyomo_RSO_Parameter_Input.xlsx','1DPar_i', (2, 'A'), (6, 'C'), 1)
    NL = faux.read_par_from_excel('Pyomo_RSO_Parameter_Input.xlsx','1DPar_i', (2, 'A'), (6, 'D'), 1)
    NW = faux.read_par_from_excel('Pyomo_RSO_Parameter_Input.xlsx','1DPar_i', (2, 'A'), (6, 'E'), 1)

    # load asset ownership information
    OL = faux.read_par_from_excel('Pyomo_RSO_Parameter_Input.xlsx','1DPar_OL', (2, 'A'), (4, 'B'), 1)
    OW = faux.read_par_from_excel('Pyomo_RSO_Parameter_Input.xlsx','1DPar_OW', (2, 'A'), (4, 'B'), 1)

    # load journey time of feasible legs
    LT = faux.read_par_from_excel(file_name,
                'WarehousesShipping', (5, 'C'), (6, 'E'), (0, 1))

    IH_low = faux.read_par_from_excel(file_name,
                'WarehousesShipping', (9, 'C'), (19, 'F'), (1, 1))

    # Load the parameters for availability scenarios
    f = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (15, 'D'), (16, 'I'), (0, 1))

    phi = faux.read_par_from_excel(file_name,
                'ScenarioAvailability', (19, 'D'), (30, 'J'), (1, 1))


    # Load the parameters for sales scenarios
    D = faux.read_par_from_excel(file_name,
                'ScenarioSales', (7, 'D'), (67, 'K'), (2, 1))

    SP = faux.read_par_from_excel(file_name,
                'ScenarioSales', (74, 'D'), (134, 'K'), (2, 1))

    SO = faux.read_par_from_excel(file_name,
                'ScenarioSales', (137, 'D'), (145, 'J'), (1, 1))

    # Loead the parameters for purchases scenarios
    PC = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (26, 'D'), (34, 'J'), (1, 1))

    IC_ini_level = faux.read_par_from_excel(file_name,
                'ScenarioPurchases', (38, 'D'), (39, 'K'), (0, 1))


    # initialise HC
    HCYES = faux.read_par_from_excel(file_name,
                'set', (25, 'E'), (28, 'K'), (1, 1))

    HC = {keys : 1 if values == 'yes' else 0
          for keys, values in HCYES.items()}

    # Initialise other parameters
    IC_low = {
    material : 0 for material in m
    }
    S_ini_level = {
    material : 0 for material in m
    }

    fixed_var = faux.ParaFixedInput(p_min, p_max, PR, tao, miu,
                                    n, LT, IC_low, IH_low, IC_upper, HC)

    variable_par = faux.ParaVarInput(f, phi, D, SP, SO, PC, OC, OP,
                                     IC_ini_level, S_ini_level)

    return set_input, fixed_var, variable_par


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    # initialise the concreteModel
    PSE_model = ConcreteModel()

    # get the data input as objects
    Excel_file = 'Borouge_Data_Scott_Demo.xlsx'
    set_input, fixed_par, variable_par = data_construction(Excel_file)
    #print(fixed_par.IH_low)
    #print(variable_par.SP)
    # set initialisation
    fset.set_initialisation(PSE_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(PSE_model, fixed_par, variable_par)

    # variable initialisation
    fvar.variable_initialisation(PSE_model)

    # constraint initialisation
    fcon.constraint_definition(PSE_model)

    # set up the model
    opt = SolverFactory('cplex')
    #opt.options['mipgap'] = 0.001
    #opt.options['threads'] = 0

    results = opt.solve(PSE_model, tee = True,
    symbolic_solver_labels = True)

    PSE_model.solutions.store_to(results)
    results.write(filename = 'solution.yml')

    # for m in PSE_model.m:
    #     for t in PSE_model.t:
    print(sum (PSE_model.QC[c, g, h, t].value * PSE_model.SP[c, g, t]
    for g in PSE_model.g for c in PSE_model.c
    for h in PSE_model.h for t in PSE_model.t))
    print(sum(PSE_model.S[m, t].value * PSE_model.SO[m, t]
        for m in PSE_model.m
        for t in PSE_model.t))

    print(sum (PSE_model.QC[c, g, h, t].value
    for g in PSE_model.g for c in PSE_model.c
    for h in PSE_model.h for t in PSE_model.t))

    print(sum(PSE_model.tao[g, j]
                for g in PSE_model.g for j in PSE_model.j))
    #total_Psale = PSE_model.QC#['KSC (UAE)', 'gPE1', 'UAE', '3'].value
    # total_Psale = sum (
    # PSE_model.QC[c, g, h, t].value * PSE_model.SP[c, g, t].value \
    # for g in PSE_model.g for c in PSE_model.c
    # for h in PSE_model.h for t in PSE_model.t)
    #print(total_Psale)
    # result_dict = faux.result_data_load(PSE_model, ['PP'])
    # print(result_dict)
if __name__ == '__main__':
    main()
© 2020 GitHub, Inc.
