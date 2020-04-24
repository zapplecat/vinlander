from unittest.mock import MagicMock
import pytest
import vinlander.soc_preprocessor as soc_preprocessor

class TestLoadXlsxData:

    def test_1(self):
        pass


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
