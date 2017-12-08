import pytest


class TestClass(object):
    def test_pytest(self):
        x = "this"
        assert 'h' in x
        with pytest.raises(ValueError):
            raise ValueError('Pytest can test this')
