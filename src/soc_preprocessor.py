'''
This preprocessor is used to digest Standard Occupational Classification
information via the Spreadsheet from US Bureau of Labor Statistics.
'''

import os
import openpyxl
import networkx


def main():
    filepath = os.path.join(
        os.path.abspath('./data'), 'soc_2018_definitions.xlsx')
    graph = networkx.Graph()
    # Keeping this structure to add other types data to the graph easier
    graph = load_soc_data(filepath, graph)


def load_soc_data(filepath, graph):
    workbook = openpyxl.load_workbook(filepath)
    worksheet = workbook.worksheets[0]
    for row in worksheet.values:
        graph.add_node(row)
    workbook.close()


if __name__ == '__main__':
    main()
