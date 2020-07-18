# from pyomo.environ import *
import pyomo.environ as pyo


def set_initialisation(optimisation_model, set_class):
    """
    This function takes in the model object and the set input (set_class)
    and initialise the set for the model
    """
    
    optimisation_model.g = pyo.Set(initialize = set_class.g,
                         doc = 'customers', ordered = True)
    
    optimisation_model.i = pyo.Set(initialize = set_class.i,
                         doc = 'node1', ordered = True)

    optimisation_model.j = pyo.Set(initialize = set_class.j,
                         doc = 'node2', ordered = True)

    optimisation_model.o = pyo.Set(initialize = set_class.o,
                         doc = 'origins', ordered = True)

    optimisation_model.d = pyo.Set(initialize = set_class.d,
                         doc = 'destinations', ordered = True)
    
    optimisation_model.l = pyo.Set(initialize = set_class.l,
                         doc = 'Locomotive type', ordered = True)

    optimisation_model.c = pyo.Set(initialize = set_class.c,
                         doc = 'Container type', ordered = True)

    optimisation_model.w = pyo.Set(initialize = set_class.w,
                         doc = 'Wagon type', ordered = True)

    optimisation_model.t = pyo.Set(initialize = set_class.t,
                         doc = 'time periods', ordered = True)    
