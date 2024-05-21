import argparse
import json
import os.path
import sys

import yaml
from logbook import Logger, NestedSetup, StreamHandler, TimedRotatingFileHandler

from bp_checker import BluePrintChecker
from scraper import Scraper


my_log = Logger(__name__)


def check_mats(**kwargs) -> dict:
    scraper = Scraper()
    scraper.load_blocks(os.path.join(kwargs["config"]["se_path"], "Data", "CubeBlocks"))

    if kwargs["modded_blocks"]:
        modded_dirs = next(os.walk(kwargs["config"]["mods_path"]))[1]
        for mod in modded_dirs:
            scraper.load_blocks(os.path.join(kwargs["config"]["mods_path"], mod, "Data", "CubeBlocks"))

    bp_file = "blueprints/bp.sbc"
    if "file" in kwargs.keys():
        bp_file = kwargs["file"]

    bpc = BluePrintChecker(scraper.all_blocks)

    return bpc.check_blueprint(bp_file)


if __name__ == "__main__":
    """       
    usage: check_mats.py [-h] -f FILE [-c [CONFIG]] [-mb | --modded-blocks]
    
    Determine the blocks that make up a blueprint
    
    options:
      -h, --help                      show this help message and exit
      -f FILE, --file FILE            a blueprint to check
      -c [CONFIG], --config [CONFIG]  override config.yaml with another, better yaml file
      -mb, --modded-blocks            load modded blocks from mods path
    """
    argp = argparse.ArgumentParser(prog="check_mats.py",
                                   description="Determine the blocks that make up a blueprint")
    argp.add_argument("-f", "--file",
                      help="a blueprint to check",
                      type=str,
                      required=True)
    argp.add_argument("-c", "--config",
                      help="override config.yaml with another, better yaml file",
                      type=str,
                      nargs="?")
    argp.add_argument("-mb", "--modded-blocks",
                      help="load modded blocks from mods path",
                      action=argparse.BooleanOptionalAction,
                      default=False)
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

    if log_handlers is None:
        my_log.error("No log handlers configured")
        quit()

    log_setup = NestedSetup(log_handlers)

    with log_setup:
        my_log.info("Starting check_mats")
        my_log.info(f"With options: {vars(args)}")
        my_log.info(f"With config: {config}")
        mats = check_mats(config=args.config, file=args.file, modded_blocks=args.modded_blocks)
        print(mats)
