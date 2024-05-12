import argparse
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
    """       
    usage: check_mats.py [-h] [-c [CONFIG]]
    
    Determine the blocks that make up a blueprint
    
    options:
      -h, --help                        show this help message and exit
      -c [CONFIG], --config [CONFIG]    override config.yaml with another, better yaml file
    """
    argp = argparse.ArgumentParser(prog="check_mats.py",
                                   description="Determine the blocks that make up a blueprint")
    argp.add_argument("-c", "--config",
                      help="override config.yaml with another, better yaml file",
                      type=str,
                      nargs="?")
    args = argp.parse_args()

    if not args.config:
        args.config = "config.yaml"

    with open(args.config, "r") as config_yaml:
        config = yaml.safe_load(config_yaml.read())
        args.config = config

    log_handlers = []
    if "handlers" in config["logger"].keys():
        for handler, options in config["logger"]["handlers"].items():
            if handler == "stream":
                log_handlers.append(StreamHandler(sys.stdout, **options))
            if handler == "timed_rotating_file":
                log_handlers.append(TimedRotatingFileHandler(os.path.abspath("log/bulk-add-role-groups"), **options))

    log_setup = NestedSetup(log_handlers)  # TODO: what if there are none?

    with log_setup:
        my_log.info("Starting check_mats")
        my_log.info(f"With options: {vars(args)}")
        my_log.info(f"With config: {config}")
        mats = check_mats(**vars(args))
        print(mats)
