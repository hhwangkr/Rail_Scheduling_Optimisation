###############################################
# This documents contains all the auxiliary ###
# functions and classes being used in the #####
# model. ######################################

# Import nccessary packages
import xlrd


class SetInput():
    """
    This is an object that initialise the input sets
    """
    def __init__(self, g, i, j, o, d, l, c, w, t):
        self.g = g
        self.i = i
        self.j = j
        self.o = o
        self.d = d
        self.l = l
        self.c = c
        self.w = w
        self.t = t

class ParaFixedInput():
    """
    This is an object that initialise the fixed parameters
    """
    def __init__(self, tau, r, u, H, OL, OW, NC, NL, NW):
        self.tau = tau
        self.H = H
        self.OL = OL
        self.OW = OW
        self.NC = NC
        self.NL = NL
        self.NW = NW

class ParaVarInput():
    """
    This is an object that initialise the varying parameters
    """
    def __init__(self, FC, VC, P, WMAX, S, M_init, WS_init):
        self.FC = FC
        self.VC = VC
        self.P = P
        self.WMAX = WMAX
        self.S = S
        self.M_init = M_init
        self.WS_init = WS_init

def cell_loc_conversion(user_input_loc):
    """
    This function takes in the excel cell number (x, A) where x is the
    row number and A is the column letter and convert it into a loc
    tuple which python can read
    """
    return user_input_loc[0] - 1, ord(user_input_loc[1].lower()) - 97
        
def result_data_load(optimisation_model, var_list):
    """
    This function takes the model and the list of variables
    and return the solutions as a dictionary
    """
    result_data = {}
    for i in var_list:
        var_obj = getattr(optimisation_model, i)
        result_data[i] = {}
        for k in var_obj.keys():
            result_data[i][k] = var_obj[k].value
    return result_data

def read_set_from_excel(file_name, sheet_name, start_loc, end_loc, n_set):
    """
    This function takes in the excel and the sheet_name + the location
    of the set to be retrieved and returns the dictionary that can be 
    used for the optimisation model
    """
    start_loc = cell_loc_conversion(start_loc)
    end_loc = cell_loc_conversion(end_loc)
    
    for sheet in xlrd.open_workbook(file_name).sheets():
        if sheet.name == sheet_name:
            set_list = [
            sheet.cell(row, start_loc[1]).value
            for row in range(start_loc[0] + 1, end_loc[0] + 1)
            ]

    return set_list            
            
def read_par_from_excel(file_name, sheet_name, start_loc, end_loc, n_set):
    """
    This function takes in the excel and the sheet_name + the location
    of the parameter to be retrieved and the paramter dimention
    and returns the dictionary that can be used for the optimisation model
    """
    start_loc = cell_loc_conversion(start_loc)
    end_loc = cell_loc_conversion(end_loc)

    if n_set == 1:
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                sheet.cell(row, start_loc[1]).value
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

                dic_values = [
                sheet.cell(row, end_loc[1]).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]
                
    elif n_set == 2:
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                (sheet.cell(row, start_loc[1]).value,
                sheet.cell(row, start_loc[1] + 1).value)
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

                dic_values = [
                sheet.cell(row, end_loc[1]).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]
    
    elif n_set == 3:
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                (sheet.cell(row, start_loc[1]).value,
                sheet.cell(row, start_loc[1] + 1).value,
                sheet.cell(row, start_loc[1] + 2).value)
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

                dic_values = [
                sheet.cell(row, end_loc[1]).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

    elif n_set == 4:
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                (sheet.cell(row, start_loc[1]).value,
                sheet.cell(row, start_loc[1] + 1).value,
                sheet.cell(row, start_loc[1] + 2).value,
                sheet.cell(row, start_loc[1] + 3).value)
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

                dic_values = [
                sheet.cell(row, end_loc[1]).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

    elif n_set == 5:
        for sheet in xlrd.open_workbook(file_name).sheets():
            if sheet.name == sheet_name:
                dic_keys = [
                (sheet.cell(row, start_loc[1]).value,
                sheet.cell(row, start_loc[1] + 1).value,
                sheet.cell(row, start_loc[1] + 2).value,
                sheet.cell(row, start_loc[1] + 3).value,
                sheet.cell(row, start_loc[1] + 4).value)
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]

                dic_values = [
                sheet.cell(row, end_loc[1]).value
                if sheet.cell_type(row, col) != xlrd.XL_CELL_EMPTY else 0
                for row in range(start_loc[0] + 1, end_loc[0] + 1)
                ]
                
    par_dict = dict(zip(dic_keys, dic_values))
    return par_dict
