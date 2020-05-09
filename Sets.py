# from pyomo.environ import *
import pyomo.environ as pyo


def set_initialisation(optimisation_model, set_class):
    """
    This function takes in the model object and the set input (set_class)
    and initialise the set for the model
    """
    # set of monomer production plants
    optimisation_model.G = pyo.Set(initialize = set_class.G,
                         doc = 'customers', ordered = True)
    
    optimisation_model.i = pyo.Set(initialize = set_class.i,
                         doc = 'node1', ordered = True)

    optimisation_model.j = pyo.Set(initialize = set_class.j,
                         doc = 'node2', ordered = True)

    optimisation_model.o = pyo.Set(initialize = set_class.o,
                         doc = 'origins', ordered = True)

    optimisation_model.d = pyo.Set(initialize = set_class.d,
                         doc = 'destinations', ordered = True)

    optimisation_model.l = pyo.Set(initialize = set_class.L,
                         doc = 'Locomotive type', ordered = True)

    optimisation_model.c = pyo.Set(initialize = set_class.C,
                         doc = 'Container type', ordered = True)

    optimisation_model.w = pyo.Set(initialize = set_class.W,
                         doc = 'Wagon type', ordered = True)

    optimisation_model.t = pyo.Set(initialize = set_class.T,
                         doc = 'time periods', ordered = True)    
