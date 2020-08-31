import pyomo.environ as pyo

def constraint_definition(model):
    """
    This function takes in the model object and initialise user-defined constraints
    """
    tsetlist = list(model.t)

    def objective_rule(model):
        """
        This constraint defines the objective function
        """
        return \
            sum(model.VC[w, i, j] * model.WM[w, i, j, t] for t in model.t for w in model.w for i in model.i for j in model.j if model.FR[i, j] == 1) \
            + sum(model.FC[l, i, j] * model.x[l, i, j, t] for t in model.t for l in model.l for i in model.i for j in model.j if model.FR[i, j] == 1)

    def locomotive_balance(model, l, i, t):
        """
        This constraint defines the loco balance around each node i
        """
        if t == 0:
            return model.M[l, i, t] == model.M_init[l, i] \
                - sum(model.x[l, i, j, t] * model.FR[i, j] for j in model.j) \

        else:
            return \
                model.M[l, i, t] == model.M[l, i, t-1] \
                - sum(model.x[l, i, j, t] * model.FR[i, j] for j in model.j) \
                + sum(model.x[l, j, i, t-model.H[j, i]] * model.FR[j, i] for j in model.j if t >= model.H[j, i])

    def wagon_balance(model, w, i, t):
        """
        This constraint defines the wagon balance around each node i
        """
        if t == 0:
            return model.WS[w, i, t] == model.WS_init[w, i] \
                   - sum(model.WM[w, i, j, t] * model.FR[i, j] for j in model.j)

        else:
            return \
                model.WS[w, i, t] == model.WS[w, i, t-1] \
                - sum(model.WM[w, i, j, t] * model.FR[i, j] for j in model.j) \
                + sum(model.WM[w, j, i, t-model.H[j, i]] * model.FR[j, i] for j in model.j if t >= model.H[j, i])

    def container_balance(model, c, g, d, i, t):
        """
        This constraint defines the container balance around each node i
        """
        if t == 0:
            return \
                model.CS[c, g, d, i, t] \
                == model.S[c, g, d, i, t] \
                - sum(model.CM[c, g, d, i, j, t] * model.FR[i, j]for j in model.j)

        else:
            return \
                model.CS[c, g, d, i, t] \
                == model.CS[c, g, d, i, t-1] \
                + model.S[c, g, d, i, t] \
                - sum(model.CM[c, g, d, i, j, t] * model.FR[i, j] for j in model.j) \
                + sum(model.CM[c, g, d, j, i, t-model.H[j, i]] * model.FR[j, i]for j in model.j if t >= model.H[j, i]) \

    def close_the_loop_1(model, l, i):
        """
        This constraint ensures all locos are at their original locations upon completion of a delivery cycle.
        Distribution does not have to be accurate at ID level; as long as locos are of same class, it is operationally okay.
        """
        tf = tsetlist[-1]
        return model.M_init[l, i] == model.M[l, i, tf]

    def close_the_loop_2(model, w, i):
        """
        This constraint ensures all wagons are at their original locations upon completion of a delivery cycle.
        Distribution does not have to be accurate at ID level; as long as wagons are of same class, it is operationally okay.
        """
        tf = tsetlist[-1]
        return model.WS_init[w, i] == model.WS[w, i, tf]

    def operational_limit_1(model, w, t):
        """
        This constraint ensures the total number of wagons in the network does not exceed the number of wagons owned at all times.
        """
        t1 = tsetlist[0]
        return \
            sum(model.WM[w, i, j, t] * model.FR[i, j] for i in model.i for j in model.j) + sum(model.WS[w, i, t] for i in model.i) \
            <= sum(model.WM[w, i, j, t1] * model.FR[i, j] for i in model.i for j in model.j) + sum(model.WS[w, i, t1] for i in model.i)

    def operational_limit_2(model, l, t):
        """
        This constraint ensures the total number of locos in the network does not exceed the number of locos owned at all times.
        """
        t1 = tsetlist[0]
        return \
            sum(model.x[l, i, j, t] * model.FR[i, j] for i in model.i for j in model.j) + sum(model.M[l, i, t] for i in model.i) \
            <= sum(model.x[l, i, j, t1] * model.FR[i, j] for i in model.i for j in model.j) + sum(model.M[l, i, t1] for i in model.i)

    def service_limit(model, i, t):
        """
        This constraint ensures no more than one train is leaving each node at time t
        """
        return \
            sum(model.x[l, i, j, t] * model.FR[i, j] for l in model.l for j in model.j) <= 1

    def storage_limit_1(model, i, t):
        """
        This constraint ensures each node only holds containers up to its storage limit
        """
        return \
            sum(model.CS[c, g, d, i, t] for c in model.c for g in model.g for d in model.d) <= model.NC[i]

    def storage_limit_2(model, i, t):
        """
        This constraint ensures each node only holds locos up to its storage limit
        """
        return \
            sum(model.M[l, i, t] for l in model.l) <= model.NL[i]

    def storage_limit_3(model, i, t):
        """
        This constraint ensures each node only holds wagons up to its storage limit
        """
        return \
            sum(model.WS[w, i, t] for w in model.w) <= model.NW[i]

    def demand_tracking(model, c, g, d):
        """
        This constraint ensures all container deliveries are made in time
        """
        tf = tsetlist[-1]
        return \
            sum(model.S[c, g, d, i, t] for i in model.o for t in model.t) <= sum(model.CS[c, g, d, i, tf] for i in model.i if i == d)

    def transportation_constraint(model, i, j, t):
        """
        This constraint restricts the maximum number of wagons on each service to WMAX
        """
        if model.FR[i, j] == 1:
            return \
                sum(model.x[l, i, j, t] for l in model.l) * model.WMAX >= sum(model.WM[w, i, j, t] for w in model.w)
        else:
            return pyo.Constraint.Skip

    def wagon_mix_1(model, i, j, t):
        """
        This constraint defines the mix of wagon types constituting each service (1)
        """
        if model.FR[i, j] == 1:
            return \
                model.WM["60ft", i, j, t] \
                + model.WM["40ft", i, j, t] \
                >= sum(model.CM["40ft", g, d, i, j, t] for g in model.g for d in model.d)
        else:
            return pyo.Constraint.Skip

    def wagon_mix_2(model, i, j, t):
        """
        This constraint defines the mix of wagon types constituting each service (2)
        """
        if model.FR[i, j] == 1:
            return \
                3 * model.WM["60ft", i, j, t] \
                + 2 * model.WM["40ft", i, j, t] \
                - 2 * sum(model.CM["40ft", g, d, i, j, t] for g in model.g for d in model.d) \
                >= sum(model.CM["20ft", g, d, i, j, t] for g in model.g for d in model.d)
        else:
            return pyo.Constraint.Skip

    # def min_prep_time(model, i, t):
    #     """
    #     This constraint ensures that the services are spaced apart for at least 1 time period
    #     """
    #     tp = t
    #     return \
    #         sum(model.x[l, i, j, tp] for l in model.l for j in model.j for tp in model.t if tp >= t - model.P[i]) \
    #         <= 1

    model.objective_function = pyo.Objective(
        rule=objective_rule,
        sense=pyo.minimize, doc='minimize cost'
    )

    model.constraint1 = pyo.Constraint(
        model.l, model.i, model.t, rule=locomotive_balance,
        doc='refer to locomotive_balance description'
    )

    model.constraint2 = pyo.Constraint(
        model.w, model.i, model.t, rule=wagon_balance,
        doc='refer to wagon_balance description'
    )

    model.constraint3 = pyo.Constraint(
        model.c, model.g, model.d, model.i, model.t, rule=container_balance,
        doc='refer to container_balance description'
    )

    model.constraint4 = pyo.Constraint(
        model.l, model.i, rule=close_the_loop_1,
        doc='refer to close_the_loop_1 description'
    )

    model.constraint5 = pyo.Constraint(
        model.w, model.i, rule=close_the_loop_2,
        doc='refer to close_the_loop_2 description'
    )

    model.constraint6 = pyo.Constraint(
        model.w, model.t, rule=operational_limit_1,
        doc='refer to operational_limit_1 description'
    )

    model.constraint7 = pyo.Constraint(
        model.l, model.t, rule=operational_limit_2,
        doc='refer to operational_limit_2 description'
    )

    model.constraint8 = pyo.Constraint(
        model.i, model.t, rule=service_limit,
        doc='refer to service_limit description'
    )

    model.constraint9 = pyo.Constraint(
        model.i, model.t, rule=storage_limit_1,
        doc='refer to storage_limit_1 description'
    )

    model.constraint10 = pyo.Constraint(
        model.i, model.t, rule=storage_limit_2,
        doc='refer to storage_limit_2 description'
    )

    model.constraint11 = pyo.Constraint(
        model.i, model.t, rule=storage_limit_3,
        doc='refer to storage_limit_3 description'
    )

    model.constraint12 = pyo.Constraint(
        model.c, model.g, model.d, rule=demand_tracking,
        doc='refer to demand_tracking description'
    )

    model.constraint13 = pyo.Constraint(
        model.i, model.j, model.t, rule=transportation_constraint,
        doc='refer to transportation_constraint description'
    )

    model.constraint14 = pyo.Constraint(
        model.i, model.j, model.t, rule=wagon_mix_1,
        doc='refer to wagon_mix_1 description'
    )

    model.constraint15 = pyo.Constraint(
        model.i, model.j, model.t, rule=wagon_mix_2,
        doc='refer to wagon_mix_2 description'
    )

    # model.constraint16 = pyo.Constraint(
    #     model.i, model.t, rule=min_prep_time,
    #     doc='refer to min_prep_time description'
    # )
