import os

import yaml

os.environ["ENV"] = yaml.safe_load(open("./config.yaml").read()).get("env", "dev")
