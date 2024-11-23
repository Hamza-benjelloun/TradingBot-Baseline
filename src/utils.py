import os


def is_preprod():
    return os.environ.get("ENV", "dev") == "preprod"
