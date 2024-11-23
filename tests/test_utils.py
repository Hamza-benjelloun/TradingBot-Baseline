import os

from src.utils import is_preprod


def test_is_preprod():
    os.environ["ENV"] = "preprod"
    assert is_preprod() == True
    os.environ["ENV"] = "dev"
    assert is_preprod() == False
