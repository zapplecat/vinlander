'''
This preprocessor is used to digest Standard Occupational Classification
information via the Spreadsheet from US Bureau of Labor Statistics.
'''

import networkx
import os
import openpyxl

from pprint import pprint

ACCEPTED_SOC_CODE_TYPES = ['major', 'minor', 'broad', 'detailed']


def main():
    filepath = os.path.join(
        os.path.abspath('./data'), 'soc_2018_definitions.xlsx')
    graph = networkx.Graph()
    # Keeping this structure to add other types data to the graph easier
    code_map, graph = load_soc_xlsx_data(filepath, graph)

    # TODO: Take this graph and calculate relationship between each node's
    # description, and assign edge weights
    print(graph.nodes)

    # TODO: Take the code map, and draw hierical-structural edges for
    # for processed graph
    pprint(code_map)

    # TODO: Save graph in some form of file cache so we can save resources
    # and only regenerate this when necessary (e.g. better model)


def load_soc_xlsx_data(filepath, graph):
    """Loads in soc xlsx data to memory.

    :param filepath: file location of the spreadsheet. In the
        format of US BLS Standard Occupational Classification
    :type filepath: str
    :param graph: a networkx graph object. Adds nodes from the spreadsheet
        to the graph object. A node is a "detailed" soc code, with appropriate
        attributes like job_title and description
    :type graph: networkx.Graph
    :return: tuple of modified networkx.Graph and dict of non-"detailed" soc
        codes
    :rtype: tuple
    """
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
        soc_code = soc_code_raw.replace('-', '')
        soc_code_name = row[2].lower()
        soc_code_description = row[3].lower()
        if soc_code_type == 'detailed':
            graph.add_node(
                soc_code,
                job_title=soc_code_name,
                job_description=soc_code_description)
        soc_code_map = set_code_mapping(
            soc_code_map, soc_code_type, soc_code, soc_code_name)
    workbook.close()
    return (soc_code_map, graph)


def set_code_mapping(code_map, code_type, code, code_name):
    if code_type not in ACCEPTED_SOC_CODE_TYPES:
        raise ValueError(
            'code_type is not part of the known types for SOC dataset')
    code_map[code] = code_name
    return code_map


if __name__ == '__main__':
    main()
