import os.path
import xml.etree.ElementTree as ElementTree

from models import Block


class Scraper:
    """
    Scrapes SE directories for block data
    """
    def __init__(self, config):
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
        cube_blocks_path = os.path.join(self.config["drive"], self.config["se_path"])

        for file in os.listdir(cube_blocks_path):
            cube_blocks_file = os.path.join(cube_blocks_path, file)
            tree = ElementTree.parse(cube_blocks_file)

            for element in tree.getroot().iter("Definition"):
                block = Block(element)
                if block.type_id is not None:
                    self.all_blocks[block.type_id] = block.as_dict()
