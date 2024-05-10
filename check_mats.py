import os.path
import xml.etree.ElementTree as ElementTree
import sys

import yaml
from logbook import Logger, NestedSetup, StreamHandler, TimedRotatingFileHandler

from scraper import Scraper


my_log = Logger(__name__)


def check_mats(config: dict) -> dict:
    s = Scraper(config)
    s.load_blocks()

    bp_file = "bp.sbc"
    tree = ElementTree.parse(bp_file)

    used_blocks = {}
    for element in tree.getroot().iter("CubeGrid"):  # only works for one subgrid ??
        cube_blocks = element.find("CubeBlocks")
        for block in cube_blocks:
            sub_type_name = block.find("SubtypeName").text

            # it's possible there is no sub type name so try to make one up instead
            if sub_type_name is None:
                for k, v in block.attrib.items():
                    sub_type_name = v.split("_")[1]
                my_log.info(f"trying: {sub_type_name}")

            if sub_type_name in used_blocks.keys():
                used_blocks[sub_type_name] += 1
            else:
                used_blocks[sub_type_name] = 1

    return {"blocks": used_blocks}


if __name__ == "__main__":
    with open("config.yaml", "r") as config_yaml:
        config = yaml.safe_load(config_yaml.read())

    log_setup = NestedSetup([
            StreamHandler(sys.stdout, level=config["logger"]["level"], bubble=False),
            TimedRotatingFileHandler(
                    os.path.abspath("yawm-log"),
                    level=0,
                    backup_count=3,
                    bubble=True,
                    date_format="%Y-%m-%d")
        ]
    )

    with log_setup:
        my_log.info("Starting check_mats")
        mats = check_mats(config)
        print(mats)
