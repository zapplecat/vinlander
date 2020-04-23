from unittest.mock import MagicMock
import pytest


class TestLoadXlsxData:

    def test_1(self):
        pass


class TestSetCodeMapping:

    @pytest.mark.parametrize(
        'input_code_type',
        ['major', 'minor', 'broad'])
    def test_acceptable_code_type(self, input_code_type):
        pass
