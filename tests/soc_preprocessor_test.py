from unittest import mock
from unittest.mock import MagicMock
from vinlander import soc_preprocessor
import pytest


# TODO: Add additional test cases for conditionals in data loading
class TestLoadXlsxData:
    global mock_workbook
    mock_workbook = MagicMock()

    @classmethod
    def setUpClass(cls):
        global mock_workbook
        cls.mock_workbook = mock_workbook

    @mock.patch('vinlander.soc_preprocessor.openpyxl.load_workbook',
                return_value=mock_workbook)
    @mock.patch('networkx.Graph')
    def test_close_workbook(self, mock_graph, mock_openpyxl_load):
        soc_preprocessor.load_soc_xlsx_data(
            'file', mock_graph)
        mock_openpyxl_load.assert_called_with('file')
        # Using this assert for better test visibility
        assert mock_workbook.close.called


class TestSetCodeMapping:

    def setup_method(self):
        self.empty_code_map = {}

    @pytest.mark.parametrize(
        'code_type',
        ['major', 'minor', 'broad'])
    def test_acceptable_code_type(self, code_type):
        code = '111'
        code_name = 'test_code_name'
        expected_code_map = {
            code_type: {code: code_name}
        }
        actual_code_map = soc_preprocessor.set_code_mapping(
            self.empty_code_map,
            code_type,
            code,
            code_name)
        assert expected_code_map == actual_code_map

    # Raise ValueError when code type is not expected
    def test_code_type_exception(self):
        code = '111'
        code_name = 'test_code_name'
        with pytest.raises(ValueError):
            soc_preprocessor.set_code_mapping(
                self.empty_code_map,
                'error',
                code,
                code_name)

    # Setting multiple codes of the same code type
    @pytest.mark.parametrize(
        'code_type',
        ['major', 'minor', 'broad'])
    def test_set_multiple_same_code_type(self, code_type):
        code_1 = '111'
        code_name_1 = 'test_code_name_1'
        code_2 = '222'
        code_name_2 = 'test_code_name_2'
        expected_code_map = {
            code_type: {
                code_1: code_name_1,
                code_2: code_name_2
            }
        }
        actual_code_map = soc_preprocessor.set_code_mapping(
            self.empty_code_map,
            code_type,
            code_1,
            code_name_1)
        actual_code_map = soc_preprocessor.set_code_mapping(
            actual_code_map,
            code_type,
            code_2,
            code_name_2)
        assert expected_code_map == actual_code_map

    # Setting multiple codes of the different code types
    @pytest.mark.parametrize(
        'first_code_type, second_code_type',
        [('major', 'minor'), ('major', 'broad'), ('minor', 'major'),
         ('broad', 'major'), ('broad', 'minor')])
    def test_set_multiple_diff_code_type(
            self, first_code_type, second_code_type):
        code_1 = '111'
        code_name_1 = 'test_code_name_1'
        code_2 = '222'
        code_name_2 = 'test_code_name_2'
        expected_code_map = {
            first_code_type: {
                code_1: code_name_1,
            },
            second_code_type: {
                code_2: code_name_2
            }
        }
        actual_code_map = soc_preprocessor.set_code_mapping(
            self.empty_code_map,
            first_code_type,
            code_1,
            code_name_1)
        actual_code_map = soc_preprocessor.set_code_mapping(
            actual_code_map,
            second_code_type,
            code_2,
            code_name_2)
        assert expected_code_map == actual_code_map
