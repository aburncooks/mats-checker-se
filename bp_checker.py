import xml.etree.ElementTree as ElementTree

from logbook import Logger


my_log = Logger(__name__)


class BluePrintChecker:
    """
    Checks blue print details
    """
    def __init__(self, blocks: dict) -> None:
        """
        Create a BluePrintChecker class

        :param blocks: a dict with all the blocks in
        :return: None
        """
        print(blocks)
        self.blocks = blocks  # for calculating component costs later

    def check_blueprint(self, bp_file: str) -> dict:
        """
        Check a blueprint

        :param bp_file: path to an xml blueprint file
        :return: dict
        """
        tree = self.open_blueprint(bp_file)

        used_blocks = {}
        for element in tree.getroot().iter("CubeGrid"):  # only works for one subgrid ??
            cube_blocks = element.find("CubeBlocks")
            for block in cube_blocks:
                sub_type_name = self.get_block_name(block)

                if sub_type_name in used_blocks.keys():
                    used_blocks[sub_type_name] += 1
                else:
                    used_blocks[sub_type_name] = 1

        return {"blocks": used_blocks}

    @staticmethod
    def open_blueprint(bp_file: str) -> ElementTree:
        """
        Open a blueprint

        :param bp_file: path to an xml blueprint file
        :return: ElementTree
        """
        try:  # TODO: probably needs to be expanded on
            tree = ElementTree.parse(bp_file)
            return tree
        except ElementTree.ParseError:
            my_log.error(f"Could not open BP due to ParseError: {bp_file}")
            return ElementTree

    @staticmethod
    def get_block_name(block: ElementTree) -> str:
        """
        Get the block name of a block

        :param block: an ElementTree of a single block
        :return: str
        """
        block_name = block.find("SubtypeName").text

        # it's possible there is no sub type name so make one up instead
        if block_name is None:
            print(block.attrib)
            for k, v in block.attrib.items():
                block_name = v.split("_")[1]
            my_log.info(f"Trying block_name: {block_name}")

        return block_name
