import pyomo.environ as pyo

def parameter_initialisation(optimisation_model, fixed_par_input):
    """
    This function takes the model input (optimisation_model) and the
    parameter input objects to initialise the model's parameters
    """
    optimisation_model.tau = pyo.Param(
                             optimisation_model.g, optimisation_model.o,
                             optimisation_model.d,
                             initialize = fixed_par_input.tau,
                             doc = 'Max. time allowable for delivery of containers from o to d for customer g'
                             )

    optimisation_model.r = pyo.Param(
                           optimisation_model.i,
                           initialize = fixed_par_input.r,
                           doc = 'loading time at node i'
                           )

    optimisation_model.u = pyo.Param(
                           optimisation_model.i,
                           initialize = fixed_par_input.u,
                           doc = 'unloading time at i'
                           )

    optimisation_model.H = pyo.Param(
                           optimisation_model.i, optimisation_model.j,
                           initialize = fixed_par_input.H,
                           doc = 'time spent by locomotives to travel from node i to j'
                           )

    optimisation_model.FC = pyo.Param(
                            optimisation_model.l, optimisation_model.i,
                            optimisation_model.j,
                            initialize = var_par_input.FC,
                            doc = 'fixed cost of running a service with locomotive (of type l) from i to j'
                            )

    optimisation_model.VC = pyo.Param(
                            optimisation_model.w, optimisation_model.i,
                            optimisation_model.j,
                            initialize = var_par_input.VC,
                            doc = 'incremental cost of moving an extra wagon (of type w) from i to j'
                            )

    optimisation_model.OL = pyo.Param(
                            optimisation_model.l,
                            initialize = fixed_par_input.OL,
                            doc = 'number of locomotives (of type l) owned'
                            )

    optimisation_model.OW = pyo.Param(
                            optimisation_model.w,
                            initialize = fixed_par_input.OW,
                            doc = 'number of wagons (of type l) owned'
                            )

    optimisation_model.P = pyo.Param(
                           optimisation_model.i,
                           initialize = var_par_input.P,
                           doc = 'preparation time required between consecutive services at node i'
                           )



    optimisation_model.WMAX = pyo.Param(
                              initialize = var_par_input.WMAX,
                              doc = 'max. # wagons per service'
                              )

    optimisation_model.S = pyo.Param(
                           optimisation_model.c, optimisation_model.g,
                           optimisation_model.i, optimisation_model.d,
                           optimisation_model.t,
                            initialize = fixed_par_input.S,
                            doc = 'supply of containers (of type c) at time t for customer g at node i for destination d'
                            )

    optimisation_model.NC = pyo.Param(
                            optimisation_model.i,
                            initialize = fixed_par_input.NC,
                            doc = 'storage capacity (container) at node i')
 
    optimisation_model.NL = pyo.Param(
                            optimisation_model.i,
                            initialize = fixed_par_input.NL,
                            doc = 'storage capacity (locomotive) at node i')

    optimisation_model.NW = pyo.Param(
                            optimisation_model.i,
                            initialize = fixed_par_input.NW,
                            doc = 'storage capacity (wagon) at node i')
    
    optimisation_model.M_init = pyo.Param(
                                optimisation_model.l, optimisation_model.l,
                                initialize = var_par_input.M_init,
                                doc = 'initial # locomotives (of type l) stationed at i')
    
    optimisation_model.WS_init = pyo.Param(
                                 optimisation_model.w, optimisation_model.i,
                                 initialize = fixed_par_input.WS_init,
                                 doc = 'initial # wagons (of type l) stationed at i')
