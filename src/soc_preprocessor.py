'''
This preprocessor is used to digest Standard Occupational Classification
information via the Spreadsheet from US Bureau of Labor Statistics.
'''

import os


def main():
    data_file = os.path.join(
        os.path.abspath('./data'),
        'soc_2018_definitions.xlsx')
    with open(data_file, mode="r") as fp:
        return


if __name__ == '__main__':
    main()
