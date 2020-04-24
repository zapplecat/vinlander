from unittest.mock import MagicMock
import pytest
import vinlander.soc_preprocessor as soc_preprocessor

class TestLoadXlsxData:

    def test_1(self):
        pass


class TestSetCodeMapping:

    def setup_method(self):
        self.code_map = {}
        self.code = '111'
        self.code_name = 'test_code_name'

    @pytest.mark.parametrize(
        'input_code_type',
        ['major', 'minor', 'broad'])
    def test_acceptable_code_type(self, input_code_type):
        expected_code_map = {
            input_code_type: {self.code: self.code_name}
        }
        actual_code_map = soc_preprocessor.set_code_mapping(
            self.code_map,
            input_code_type,
            self.code,
            self.code_name)
        assert expected_code_map == actual_code_map

    # Raise ValueError when code type is not expected
    def test_code_type_exception(self):
        with pytest.raises(ValueError):
            soc_preprocessor.set_code_mapping(
                self.code_map,
                'error',
                self.code,
                self.code_name)
