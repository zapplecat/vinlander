'''
This preprocessor is used to digest Standard Occupational Classification
information via the Spreadsheet from US Bureau of Labor Statistics.
'''

import matplotlib.pyplot as pyplot
import networkx
import os
import openpyxl

from pprint import pprint

ACCEPTED_SOC_CODE_TYPES = ['major', 'minor', 'broad', 'detailed']


def main():
    filepath = os.path.join(
        os.path.abspath('./data'), 'soc_2018_definitions.xlsx')
    graph = networkx.DiGraph()
    # Keeping this structure to add other types data to the graph easier
    code_map, graph = load_soc_xlsx_data(filepath, graph)

    # Draws graph for example purposes
    graph = get_branch_subgraph(
        graph,
        '119000',
        include_parent=True)
    networkx.draw(graph, with_labels=True)
    pyplot.show()

    # TODO: Take graph and calculate relationship between each node's
    # description, and assign edge weights

    # TODO: Take the code map, and draw hierical-structural edges for
    # for processed graph
    pprint(code_map)

    # TODO: Save graph in some form of file cache so we can save resources
    # and only regenerate this when necessary (e.g. better model)


# TODO: This is not a preprocessor API
def get_branch_subgraph(graph,
                        starting_node,
                        include_parent=False):
    """Gets a subgraph using dfs from a starting node.
    The subgraph is read only.

    :param starting_node: node to retrieve subgraph from.
    :param include_parent: whether to include the parent node of the
        starting node
    :type includ_parent: bool
    """
    branch = networkx.dfs_tree(graph, source=starting_node)
    if include_parent:
        edge = graph.in_edges(starting_node)
        return networkx.subgraph_view(
            graph,
            filter_node=lambda node: (
                node in branch or node is list(edge)[0][0]))
    return networkx.subgraph_view(
        graph,
        filter_node=lambda node: node in branch)


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
    soc mapping is composed of a 6 digit code aa-bccd.
    aa: major group
    b: minor group
    cc: broad job
    d: detailed job and description
    '''
    soc_code_map = {
        accepted_code_type: {}
        for accepted_code_type in ACCEPTED_SOC_CODE_TYPES
    }
    for row in worksheet.values:
        soc_code_type = row[0].lower()
        soc_code_raw = row[1]
        soc_code = soc_code_raw.replace('-', '')
        soc_code_name = row[2].lower()
        # Does not account for scrambled files, might be brittle
        # TODO: Might be better to rely on code mapping for edge drawing
        # so I don't overload this
        if soc_code_type == 'detailed':
            soc_code_description = row[3].lower()
            graph.add_node(
                soc_code,
                job_title=soc_code_name,
                job_description=soc_code_description,
                soc_type=soc_code_type)
            # TODO: Fix this jerry rig
            soc_parent_code = soc_code[:-1] + '0'
            alt_parent_code = int(soc_parent_code) - 1
            alt_parent_code = str(alt_parent_code)[:-1] + '0'
            if soc_parent_code in graph:
                graph.add_edge(soc_parent_code, soc_code)
            elif alt_parent_code in graph:
                # Catches cases where detailed category extends beyond single
                # digit in above schema and soc mapping becomes aa-bcdd
                graph.add_edge(alt_parent_code, soc_code)
            else:
                raise RuntimeError(
                    '{} detailed code not loaded'.format(soc_code))
        elif soc_code_type == 'broad':
            graph.add_node(
                soc_code,
                job_title=soc_code_name,
                soc_type=soc_code_type)
            # TODO: Fix this jerry rig
            soc_parent_code = soc_code[:-2] + '00'
            soc_parent_code_alt = soc_code[:-3] + '000'
            if soc_parent_code in graph:
                graph.add_edge(soc_parent_code, soc_code)
            elif soc_parent_code_alt in graph:
                graph.add_edge(soc_parent_code_alt, soc_code)
        elif soc_code_type == 'minor':
            graph.add_node(
                soc_code,
                job_title=soc_code_name,
                soc_type=soc_code_type)
            soc_parent_code = soc_code[:-4] + '0000'
            if soc_parent_code in graph:
                graph.add_edge(soc_parent_code, soc_code)
        elif soc_code_type == 'major':
            if soc_code not in graph:
                graph.add_node(
                    soc_code,
                    job_title=soc_code_name,
                    soc_type=soc_code_type)
        soc_code_map = set_code_mapping(
            soc_code_map, soc_code_type, soc_code, soc_code_name)
    workbook.close()
    return (soc_code_map, graph)


def set_code_mapping(code_map, code_type, code, code_name):
    if code_type not in ACCEPTED_SOC_CODE_TYPES:
        raise ValueError(
            'code_type is not part of the known types for SOC dataset')
    code_map[code_type][code] = code_name
    return code_map


if __name__ == '__main__':
    main()
