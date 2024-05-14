import os.path
import xml.etree.ElementTree as ElementTree

from logbook import Logger

from models import Block


my_log = Logger(__name__)


class Scraper:
    """
    Scrapes SE directories for block data

    :return: None
    """
    def __init__(self, config: dict) -> None:
        """
        Create a scraper class
        """
        self.all_blocks = {}
        self.config = config

    def load_blocks(self) -> None:
        """
        Load the blocks from files in content directory

        :return: None
        """
        cube_blocks_path = self.config["se_path"]

        for file in os.listdir(cube_blocks_path):
            cube_blocks_file = os.path.join(cube_blocks_path, file)

            try:
                tree = ElementTree.parse(cube_blocks_file)
                for element in tree.getroot().iter("Definition"):
                    block = Block()
                    block.from_element(element)

                    if block.type_id is None:
                        my_log.warn(f"Skipped due to None type_id: {cube_blocks_file}")
                        continue
                    self.all_blocks[block.sub_type_id] = block.as_dict()

            except ElementTree.ParseError:
                my_log.warn(f"Skipped due to ParseError: {cube_blocks_file}")
                continue
