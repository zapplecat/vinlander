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
        soc_preprocessor.set_code_mapping(
            self.code_map,
            input_code_type,
            self.code,
            self.code_name)

    def test_code_type_exception(self):
        pass
