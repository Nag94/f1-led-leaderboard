import pytest
import time
from api.data import Data
from config.matrix_config import MatrixConfig
from constants import UPDATE_RATE


class TestData:
    def setup_method(self):
        self.data = Data(MatrixConfig(64, 32))

    @pytest.mark.slow
    def test_should_update(self):
        time.sleep(UPDATE_RATE)
        assert self.data.should_update() is True

    def test_should_update_2(self):
        assert self.data.should_update() is False
