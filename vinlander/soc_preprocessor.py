'''
This preprocessor is used to digest Standard Occupational Classification
information via the Spreadsheet from US Bureau of Labor Statistics.
'''

import networkx
import os
import openpyxl
import re

from pprint import pprint


def main():
    filepath = os.path.join(
        os.path.abspath('./data'), 'soc_2018_definitions.xlsx')
    graph = networkx.Graph()
    # Keeping this structure to add other types data to the graph easier
    code_map, graph = load_soc_xlsx_data(filepath, graph)
    print(graph.nodes)
    pprint(code_map)


def load_soc_xlsx_data(filepath, graph):
    workbook = openpyxl.load_workbook(filepath)
    worksheet = workbook.worksheets[0]
    '''
    soc mapping is composed of a 6 digit code aa-bbcd.
    aa: major group
    bb: minor group
    c: broad job
    d: detailed job and description
    '''
    soc_code_map = {}
    for row in worksheet.values:
        soc_code_type = row[0].lower()
        soc_code_raw = row[1]
        soc_code = soc_code_raw.strip('-')
        soc_code_name = row[2].lower()
        if soc_code_type == 'detailed':
            # TODO: Add the rest of the attributes in here
            graph.add_node(soc_code, title=soc_code_name)
        else:
            if soc_code_type not in soc_code_map:
                soc_code_map[soc_code_type] = {}
            soc_code_map = set_code_mapping(
                soc_code_map, soc_code_type, soc_code, soc_code_name)
    workbook.close()
    return (soc_code_map, graph)


def set_code_mapping(code_map, code_type, code, code_name):
    if code_type not in ['major', 'minor', 'broad']:
        raise ValueError(
            'code_type is not part of the known types for SOC dataset')
    elif code_type not in code_map:
        code_map[code_type] = {}
    code_map[code_type][code] = code_name
    return code_map


if __name__ == '__main__':
    main()
