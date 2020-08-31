import pyomo.environ as pyo

def parameter_initialisation(optimisation_model, param_input):

    """
    This function takes the model input (optimisation_model) and the
    parameter input objects to initialise the model's parameters
    """

    optimisation_model.FR = pyo.Param(
        optimisation_model.i, optimisation_model.j,
        initialize=param_input.FR,
        doc='Boolean to indicate feasible routes'
        )

    optimisation_model.tau = pyo.Param(
        optimisation_model.g, optimisation_model.o,
        optimisation_model.d,
        initialize=param_input.tau,
        doc='Max. time allowable for delivery of containers from o to d for customer g'
        )

    optimisation_model.H = pyo.Param(
        optimisation_model.i, optimisation_model.j,
        default = 0,
        initialize=param_input.H,
        doc='time spent by locomotives to travel from node i to j'
        )

    optimisation_model.FC = pyo.Param(
        optimisation_model.l, optimisation_model.i,
        optimisation_model.j,
        initialize=param_input.FC,
        doc='fixed cost of running a service with locomotive (of type l) from i to j'
        )

    optimisation_model.VC = pyo.Param(
        optimisation_model.w, optimisation_model.i,
        optimisation_model.j,
        initialize=param_input.VC,
        doc='incremental cost of moving an extra wagon (of type w) from i to j'
        )

    optimisation_model.OL = pyo.Param(
        optimisation_model.l,
        initialize=param_input.OL,
        doc='number of locomotives (of type l) owned'
        )

    optimisation_model.OW = pyo.Param(
        optimisation_model.w,
        initialize=param_input.OW,
        doc='number of wagons (of type l) owned'
        )

    optimisation_model.P = pyo.Param(
        optimisation_model.i,
        initialize=param_input.P,
        doc='preparation time required between consecutive services at node i'
        )

    optimisation_model.WMAX = pyo.Param(
        initialize=param_input.WMAX,
        doc='max. # wagons per service'
        )

    optimisation_model.S = pyo.Param(
        optimisation_model.c, optimisation_model.g,
        optimisation_model.d, optimisation_model.i,
        optimisation_model.t,
        default=0,
        initialize=param_input.S,
        doc='supply of containers (of type c) at time t for customer g at node i for destination d'
        )

    optimisation_model.NC = pyo.Param(
        optimisation_model.i,
        initialize=param_input.NC,
        doc='storage capacity (container) at node i'
        )

    optimisation_model.NL = pyo.Param(
        optimisation_model.i,
        initialize=param_input.NL,
        doc='storage capacity (locomotive) at node i'
        )

    optimisation_model.NW = pyo.Param(
        optimisation_model.i,
        initialize=param_input.NW,
        doc='storage capacity (wagon) at node i'
        )

    optimisation_model.M_init = pyo.Param(
        optimisation_model.l, optimisation_model.i,
        initialize=param_input.M_init,
        doc='initial # locomotives (of type l) stationed at i'
        )

    optimisation_model.WS_init = pyo.Param(
        optimisation_model.w, optimisation_model.i,
        initialize=param_input.WS_init,
        doc='initial # wagons (of type l) stationed at i'
        )