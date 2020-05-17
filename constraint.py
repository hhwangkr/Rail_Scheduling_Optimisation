import pyomo.environ as pyo

def constraint_definition(model):
    """
    This function takes in the model object and initialise
    user-defined constraints
    """
    hsetlist = list(model.h)

    def objective_rule(model):
        """
        This constraint defines the objective function
        """
        return \
          sum (model.VC[w, i, j] * model.OM[w, i, j, t] for t in model.t for w in model.w for i in model.i for j in model.j)\
        + sum (model.FC[l, i, j] * model.OM[l, i, j, t] for t in model.t for l in model.l for i in model.i for j in model.j)


    def locomotive_balance(model, l, i, t):
        """
        This constraint defines the loco balance around a given node i.
        'ix' refers to i' from formulation
        
        [does the balance require initial level parameter for t0?]
        """
        return \
        model.M[l, i, t] = model.M[l, i, t-1] \
                           - sum (model.x[l, i, ix, t-model.r[i]] for ix in model.i if ix != i) \
                           + sum (model.x[l, ix, i, t-model.u[i]-model.H[ix,i]] for ix in model.i if ix != i)


    def wagon_balance(model, w, i, t):
        """
        This constraint defines the wagon balance around a given node i.
        'ix' refers to i' from formulation
        
        [does the balance require initial level parameter for t0?]
        """
        return \
        model.WS[w, i, t] = model.WS[w, i, t-1] \
                           - sum (model.WM[w, i, ix, t-model.r[i]] for ix in model.i if ix != i) \
                           + sum (model.WS[w, ix, i, t-model.u[i]-model.H[ix,i]] for ix in model.i if ix != i)

    def container_balance(model, c, i, t):
        """
        This constraint defines the container balance around a given node i.
        'ix' refers to i' from formulation
        
        [does the balance require initial level parameter for t0?]
        """
        return \
        sum (model.CS[c, g, o, d, i, t] for g in model.g for o in model.o for d in model.d) = \
        sum (model.CS[c, g, o, d, i, t-1] for g in model.g for o in model.o for d in model.d) \
        - sum (model.CM[c, g, o, d, i, ix, t-model.r[i]] for ix in model.i if ix != i for g in model.g for o in model.o for d in model.d) \
        + sum (model.CM[c, g, o, d, ix, i, t-model.u[i]-model.H[ix,i]] for ix in model.i if ix != i for g in model.g for o in model.o for d in model.d)

    def close_the_loop_1(model, l, i):
        """
        This constraint ensures all locos are at their original locations upon completion of a delivery cycle.
        Distribution does not have to be accurate at ID level; as long as locos are of same class, it is operationally okay.
        
        [how do you relate t == t0 and t == tf in the constraint?]
        """
        return \
        model.M[l, i, t0] = model.M[l, i, tf]

    def close_the_loop_2(model, w, i):
        """
        This constraint ensures all wagons are at their original locations upon completion of a delivery cycle.
        Distribution does not have to be accurate at ID level; as long as wagons are of same class, it is operationally okay.
        
        [how do you relate t == t0 and t == tf in the constraint?]
        """
        return \
        model.WS[w, i, t0] = model.WS[w, i, tf]

    def operational_limit_1(model, w, t):
        """
        This constraint ensures the total number of wagons in the network does not exceed the number of wagons owned at all times.
        """
        return \
        sum (model.WM[w, i, j, t] for i in model.i for j in model.j) + \
        sum (model.WS[w, i, t] for i in model.i) = model.OW[w]
        
    def operational_limit_2(model, l, t):
        """
        This constraint ensures the total number of locos in the network does not exceed the number of locos owned at all times.
        """
        return \
        sum (model.x[l, i, j, t] for i in model.i for j in model.j) + \
        sum (model.M[l, i, t] for i in model.i) = model.OL[l]

    def service_limit(model, i, t):
        """
        This constraint ensures no more than one train is leaving each node at time t
        """
        return \
        sum (model.x[l, i, j, t] for l in model.l for j in model.j) <= 1

    def storage_limit_1(model, i, t):
        """
        This constraint ensures each node only holds containers up to its storage limit
        """
        return \
        sum (model.CS[c, g, o, d, i, t] for c in model.c for g in model.g for o in model.o for d in model.d) <= model.NC[i]

    def storage_limit_2(model, i, t):
        """
        This constraint ensures each node only holds locos up to its storage limit
        """
        return \
        sum (model.M[l, i, t] for l in model.l) <= model.NL[i]
        
    def storage_limit_3(model, i, t):
        """
        This constraint ensures each node only holds wagons up to its storage limit
        """
        return \
        sum (model.WS[w, i, t] for w in model.w) <= model.NW[i]

    def demand_tracking(model, c, g, o, d):
        """
        This constraint ensures all container deliveries are made in time
        """
        return \
        sum (model.WS[w, i, t] for w in model.w) <= model.NW[i]



    model.objective_function = pyo.Objective(
                               rule = objective_rule,
                               sense = pyo.maximize, doc = 'maximise revenue'
                               )


    model.constraint1 = pyo.Constraint(
                        model.g, model.j, model.t, rule = constraint_rule_1,
                        doc = 'refer to constraint_rule_1'
                        )

    model.constraint2 = pyo.Constraint(
                        model.g, model.j, model.t, rule = constraint_rule_2,
                        doc = 'refer to constraint_rule_2'
                        )

    model.constraint3 = pyo.Constraint(
                        model.j, model.t, rule = constraint_rule_3,
                        doc = 'refer to constraint_rule_3'
                        )

    model.constraint4 = pyo.Constraint(
                        model.m, model.t, rule = constraint_rule_4,
                        doc = 'refer to constraint_rule_4'
                        )

    model.constraint5 = pyo.Constraint(
                        model.g, model.h, model.t, rule = constraint_rule_5,
                        doc = 'refer to constraint_rule_5'
                        )

    model.constraint6 = pyo.Constraint(
                        model.g, model.c, model.t, rule = constraint_rule_6,
                        doc = 'refer to constraint_rule_6'
                        )

    model.constraint7 = pyo.Constraint(
                        model.i, model.t, rule = constraint_rule_7,
                        doc = 'refer to constraint_rule_7'
                        )
