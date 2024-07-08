import os.path
import xml.etree.ElementTree as ElementTree

from logbook import Logger

from models import Block, Recipe


my_log = Logger(__name__)


class Scraper:
    """
    Scrapes SE directories for block data

    :return: None
    """
    def __init__(self) -> None:
        """
        Create a scraper class
        """
        self.all_blocks = {}
        self.all_recipes = {}

    def load_blocks(self, cube_blocks_path: str) -> None:
        """
        Load the blocks from files in a content directory

        :return: None
        """
        if not os.path.isdir(cube_blocks_path):
            my_log.warn(f"cube_blocks_path does not exist = {cube_blocks_path}")
            return None

        for file in os.listdir(cube_blocks_path):
            if not file.endswith(".sbc"):
                continue

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

    def load_recipes(self, recipes_file: str) -> None:
        """
        Load the recipes from the recipes blueprint file

        :return: None
        """
        if not os.path.isfile(recipes_file):
            my_log.warn(f"recipes_file does not exist = {recipes_file}")
            return None

        try:
            tree = ElementTree.parse(recipes_file)
            for element in tree.getroot().iter("Blueprint"):
                recipe = Recipe()
                recipe.from_element(element)

                if recipe.output_type_id is None:
                    continue

                self.all_recipes[recipe.output_type_id] = recipe.as_dict()

        except ElementTree.ParseError:
            my_log.warn(f"Skipped due to ParseError: {recipes_file}")
