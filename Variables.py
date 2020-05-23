import pyomo.environ as pyo

def variable_initialisation(optimisation_model):
    """
    This function takes in the optimisation_model as the input and
    initialises the variables, their characteristics and bounds
    """
    
    optimisation_model.x = pyo.Var(
                            optimisation_model.l, optimisation_model.i,
                            optimisation_model.j, optimisation_model.t,
                            within = pyo.Binary,
                            doc = 'locomotive (of type l) leaving i for j at period t'
                            )
    
    optimisation_model.M = pyo.Var(
                           optimisation_model.l, optimisation_model.i,
                           optimisation_model.t,
                           within = pyo.NonNegativeIntegers,
                           doc = '# locomotives (of type l) stationed at i at period t'
                           )

    optimisation_model.WM = pyo.Var(
                            optimisation_model.w, optimisation_model.i,
                            optimisation_model.j, optimisation_model.t,
                            within = pyo.NonNegativeIntegers,
                            doc = '# Wagons (of type w) leaving i for j at period t'
                            )

    optimisation_model.WS = pyo.Var(
                            optimisation_model.w, optimisation_model.i,
                            optimisation_model.t,
                            within = pyo.NonNegativeIntegers,
                            doc = '# Wagons (of type w) stationed at i at period t'
                            )

    optimisation_model.CM = pyo.Var(
                            optimisation_model.c, optimisation_model.g,
                            optimisation_model.o, optimisation_model.i,
                            optimisation_model.j, optimisation_model.t,
                            within = pyo.NonNegativeIntegers,
                            doc = '# Containers (of type c for customer g, to be delivered from o) leaving i for j at period t'
                            )

    optimisation_model.CS = pyo.Var(
                            optimisation_model.c, optimisation_model.g,
                            optimisation_model.o, optimisation_model.i,
                            optimisation_model.t,
                            within = pyo.NonNegativeIntegers,
                            doc = '# Containers (of type c for customer g, to be delivered from o) staioned at i at period t'
                            )
