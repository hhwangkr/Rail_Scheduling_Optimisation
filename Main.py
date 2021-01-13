## Import built packages ##
from pyomo.environ import *
import pandas as pd
import numpy as np

## Import model components ##
import Sets as fset
import Parameters as fpar
import Variables as fvar
import Constraints as fcon
import Auxiliary_Functions as faux

a = 1

def data_construction(file_name):
    """
    This function constructs the input data object
    """
    # load the sets
    g = ['Maersk', 'Hamburg Sud']
    i = ['A', 'B', 'C', 'D']
    j = ['A', 'B', 'C', 'D']
    o = ['A']
    d = ['B', 'D']
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
    tau = faux.read_par_from_excel(file_name, '3DPar_Tau', (2, 'A'), (4, 'D'), 3)

    # Load Delivery time information
    S = faux.read_par_from_excel(file_name, '5DPar_S', (2, 'A'), (5, 'F'), 5)

    param_input = faux.ParamInput(FR, tau, H, OL, OW, NC, NL, NW, FC, VC, P, WMAX, S, M_init, WS_init)

    return set_input, param_input

class Variable:
    def __init__(self, model, var, index): #Initialisation
        self.model = model
        self.var = var
        self.index = index

    def index_name(self):
        return self.index

    def index_list(self):
        list = []
        for v in self.model.component_objects(Var):
            if v.name == self.var:
                for i in v:
                    list.append(i)
        return list

    def value_list(self):
        list = []
        for v in self.model.component_objects(Var):
            if v.name == self.var:
                for i in v:
                    list.append(v[i].value)
        return list

    def var_dataframe(self):
        df = pd.DataFrame(self.value_list(), index=self.index_list(), columns=['Value'])
        df['Value'] = df['Value'].fillna(0)
        return df

def main():
    """
    This is the main function which calls all other functions to solve the optimisation model
    """
    # initialise the concreteModel
    RSO_model = ConcreteModel()

    # get the data input as objects
    file_name = 'Pyomo_RSO_Parameter_Input.xlsx'
    set_input, param_input = data_construction(file_name)

    # set initialisation
    fset.set_initialisation(RSO_model, set_input)

    # parameter initialisation
    fpar.parameter_initialisation(RSO_model, param_input)

    # variable initialisation
    fvar.variable_initialisation(RSO_model)

    # constraint initialisation
    fcon.constraint_definition(RSO_model)

    # set up the model
    opt = SolverFactory('cbc', executable="cbc-win64\cbc")

    results = opt.solve(RSO_model, tee=True, symbolic_solver_labels=True, timelimit=60)

    RSO_model.solutions.store_to(results)

    indexname = Variable(RSO_model, 'M', ['c', 'g', 'd', 'i', 't']).index_name()
    print(indexname)

    # tidy up variable results
    var_dict = {}

    for v in RSO_model.component_objects(Var, active=True):
        var_key = []
        for index in v:
            var_key.append([index, v[index].value])
            var_dict[v.name] = var_key

    # feasible routes dataframe
    list_FR = [key for key, val in param_input.FR.items() if val != 0]
    df_FR = pd.DataFrame(list_FR, columns=['i', 'j'])

    # journey time dataframe
    list_H = {key:val for key, val in param_input.H.items() if val != 0}
    df_H = pd.DataFrame(list_H.items(), columns=['Leg', 'JourneyTime'])
    df_H[['i', 'j']] = pd.DataFrame(df_H['Leg'].tolist(), index=df_H.index)
    df_H = df_H[['i', 'j', 'JourneyTime']]

    # create dataframe for variable 'x'
    df_x_extract = pd.DataFrame.from_dict(var_dict['x'])
    df_x_extract[['l', 'i', 'j', 't']] = pd.DataFrame(df_x_extract[0].tolist(),
                                                      index=df_x_extract.index)
    df_x_extract['Value'] = df_x_extract[1].fillna(0)
    df_x_extract = pd.merge(df_x_extract, df_FR, how='inner', left_on=['i', 'j'], right_on=['i', 'j'])
    df_x = pd.crosstab([df_x_extract.l, df_x_extract.i, df_x_extract.j],
                       [df_x_extract.t],
                       values=df_x_extract.Value,
                       aggfunc='sum',
                       dropna=True)

    # create dataframe for no. of trains moving ('nx')
    df_x_timejoined = pd.merge(df_x_extract, df_H, how='left', left_on=['i', 'j'], right_on=['i', 'j'])
    df_x_unaffected = df_x_timejoined[df_x_timejoined['Value'] == 0]
    df_x_affected = df_x_timejoined[df_x_timejoined['Value'] > 0]
    df_x_affected_dup = df_x_affected.loc[df_x_affected.index.repeat(df_x_affected['JourneyTime'])].drop(['JourneyTime'], axis=1)
    df_x_affected_dup['ind'] = df_x_affected_dup.index

    ID = ['ind', 'l', 'i', 'j', 't']
    isdup = df_x_affected_dup.duplicated(subset=ID)
    df_x_dups, df_x_uniques = df_x_affected_dup[isdup], df_x_affected_dup[~isdup]

    for i, row in df_x_dups.iterrows():
        while (row[ID] == df_x_uniques[ID]).all(axis=1).any():
            row.loc['t'] += 1
        df_x_uniques = df_x_uniques.append(row)

    df_x_uniques_groupby = df_x_uniques.groupby(['l', 'i', 'j', 't'])['Value'].sum().reset_index()
    df_nx = df_x_uniques_groupby.append(df_x_unaffected)
    df_nx_final = pd.crosstab([df_nx.l, df_nx.i, df_nx.j],
                              [df_nx.t],
                              values=df_nx.Value,
                              aggfunc='sum',
                              dropna=True)

    # create dataframe for variable 'WM'
    df_WM_extract = pd.DataFrame.from_dict(var_dict['WM'])
    df_WM_extract[['w', 'i', 'j', 't']] = pd.DataFrame(df_WM_extract[0].tolist(),
                                                       index=df_WM_extract.index)
    df_WM_extract['Value'] = df_WM_extract[1].fillna(0)
    df_WM_extract = pd.merge(df_WM_extract, df_FR, how='inner', left_on=['i', 'j'], right_on=['i', 'j'])
    df_WM = pd.crosstab([df_WM_extract.w, df_WM_extract.i, df_WM_extract.j],
                        [df_WM_extract.t],
                        values=df_WM_extract.Value,
                        aggfunc='sum',
                        dropna=True)

    # create dataframe for variable CM'
    df_CM_extract = pd.DataFrame.from_dict(var_dict['CM'])
    df_CM_extract[['c', 'g', 'd', 'i', 'j', 't']] = pd.DataFrame(df_CM_extract[0].tolist(),
                                                       index=df_CM_extract.index)
    df_CM_extract['Value'] = df_CM_extract[1].fillna(0)
    df_CM_extract = pd.merge(df_CM_extract, df_FR, how='inner', left_on=['i', 'j'], right_on=['i', 'j'])
    df_CM = pd.crosstab([df_CM_extract.c, df_CM_extract.g, df_CM_extract.d, df_CM_extract.i, df_CM_extract.j],
                        [df_CM_extract.t],
                        values=df_CM_extract.Value,
                        aggfunc='sum',
                        dropna=True)

    # create dataframe for variable WS'
    df_WS_extract = pd.DataFrame.from_dict(var_dict['WS'])
    df_WS_extract[['w', 'i', 't']] = pd.DataFrame(df_WS_extract[0].tolist(),
                                                       index=df_WS_extract.index)
    df_WS_extract['Value'] = df_WS_extract[1].fillna(0)
    df_WS = pd.crosstab([df_WS_extract.w, df_WS_extract.i],
                        [df_WS_extract.t],
                        values=df_WS_extract.Value,
                        aggfunc='sum',
                        dropna=True)

    # create dataframe for variable CS'
    df_CS_extract = pd.DataFrame.from_dict(var_dict['CS'])
    df_CS_extract[['c', 'g', 'd', 'i', 't']] = pd.DataFrame(df_CS_extract[0].tolist(),
                                                       index=df_CS_extract.index)
    df_CS_extract['Value'] = df_CS_extract[1].fillna(0)
    df_CS = pd.crosstab([df_CS_extract.c, df_CS_extract.g, df_CS_extract.d, df_CS_extract.i],
                        [df_CS_extract.t],
                        values=df_CS_extract.Value,
                        aggfunc='sum',
                        dropna=True)

    # export all variable dataframes
    with pd.ExcelWriter('results.xlsx', engine='xlsxwriter') as writer:
        df_x.to_excel(writer, sheet_name='x')
        df_nx_final.to_excel(writer, sheet_name='nx')
        df_WM.to_excel(writer, sheet_name='WM')
        df_CM.to_excel(writer, sheet_name='CM')
        df_WS.to_excel(writer, sheet_name='WS')
        df_CS.to_excel(writer, sheet_name='CS')

        # format cells
        workbook = writer.book
        worksheet_x = writer.sheets['x']
        worksheet_nx = writer.sheets['nx']
        worksheet_WM = writer.sheets['WM']
        worksheet_CM = writer.sheets['CM']
        worksheet_WS = writer.sheets['WS']
        worksheet_CS = writer.sheets['CS']

        format_highlight = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#FF0000', 'bold': True})
        format_others = workbook.add_format({'font_color': '#D3D3D3'})

        start_row = 1
        start_col_x, end_row_x, end_col_x = len(df_x.index.names), df_x.shape[0], len(df_x.index.names) + df_x.shape[1] - 1
        start_col_nx, end_row_nx, end_col_nx = len(df_nx_final.index.names), df_nx_final.shape[0], len(df_nx_final.index.names) + df_nx_final.shape[1] - 1
        start_col_WM, end_row_WM, end_col_WM = len(df_WM.index.names), df_WM.shape[0], len(df_WM.index.names) + df_WM.shape[1] - 1
        start_col_CM, end_row_CM, end_col_CM = len(df_CM.index.names), df_CM.shape[0], len(df_CM.index.names) + df_CM.shape[1] - 1
        start_col_WS, end_row_WS, end_col_WS = len(df_WS.index.names), df_WS.shape[0], len(df_WS.index.names) + df_WS.shape[1] - 1
        start_col_CS, end_row_CS, end_col_CS = len(df_CS.index.names), df_CS.shape[0], len(df_CS.index.names) + df_CS.shape[1] - 1

        worksheet_x.conditional_format(start_row, start_col_x, end_row_x, end_col_x,
                                     {'type': 'cell','criteria': '>','value': 0,'format': format_highlight})
        worksheet_x.conditional_format(start_row, start_col_x, end_row_x, end_col_x,
                                       {'type': 'cell', 'criteria': '=', 'value': 0, 'format': format_others})
        worksheet_nx.conditional_format(start_row, start_col_nx, end_row_nx, end_col_nx,
                                       {'type': 'cell', 'criteria': '>', 'value': 0, 'format': format_highlight})
        worksheet_nx.conditional_format(start_row, start_col_nx, end_row_nx, end_col_nx,
                                       {'type': 'cell', 'criteria': '=', 'value': 0, 'format': format_others})
        worksheet_WM.conditional_format(start_row, start_col_WM, end_row_WM, end_col_WM,
                                       {'type': 'cell','criteria': '>','value': 0,'format': format_highlight})
        worksheet_WM.conditional_format(start_row, start_col_WM, end_row_WM, end_col_WM,
                                       {'type': 'cell', 'criteria': '=', 'value': 0, 'format': format_others})
        worksheet_CM.conditional_format(start_row, start_col_CM, end_row_CM, end_col_CM,
                                       {'type': 'cell','criteria': '>','value': 0,'format': format_highlight})
        worksheet_CM.conditional_format(start_row, start_col_CM, end_row_CM, end_col_CM,
                                       {'type': 'cell', 'criteria': '=', 'value': 0, 'format': format_others})
        worksheet_WS.conditional_format(start_row, start_col_WS, end_row_WS, end_col_WS,
                                       {'type': 'cell','criteria': '>','value': 0,'format': format_highlight})
        worksheet_WS.conditional_format(start_row, start_col_WS, end_row_WS, end_col_WS,
                                       {'type': 'cell', 'criteria': '=', 'value': 0, 'format': format_others})
        worksheet_CS.conditional_format(start_row, start_col_CS, end_row_CS, end_col_CS,
                                       {'type': 'cell','criteria': '>','value': 0,'format': format_highlight})
        worksheet_CS.conditional_format(start_row, start_col_CS, end_row_CS, end_col_CS,
                                       {'type': 'cell', 'criteria': '=', 'value': 0, 'format': format_others})

        writer.save()

if __name__ == '__main__':
    main()
