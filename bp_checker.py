import xml.etree.ElementTree as ElementTree

from logbook import Logger


my_log = Logger(__name__)


class BluePrintChecker:
    """
    Checks blueprint details
    """
    def __init__(self, blocks: dict, components: dict) -> None:
        """
        Create a BluePrintChecker class

        :param blocks: a dict with all the blocks in
        :return: None
        """
        self.blocks = blocks  # for calculating component costs later
        self.components = components  # for calculating materials estimate later

    def check_blueprint(self, bp_file: str) -> dict:
        """
        Check a blueprint

        :param bp_file: path to an xml blueprint file
        :return: dict
        """
        blueprint = self.open_blueprint(bp_file)
        blocks = self.check_blocks(blueprint)
        components = self.check_components(blocks)
        materials = self.check_mats(components["components"])

        return {"blocks": blocks,
                "components": components["components"],
                "unknown_blocks": components["unknown_blocks"],
                "materials_estimate": materials["materials"]}

    def check_blocks(self, blueprint: ElementTree) -> dict:
        """
        Checks the blocks in a blueprint

        :param blueprint: the blueprint as an element
        :return: dict
        """
        used_blocks = {}
        for block in blueprint.getroot().findall(".//MyObjectBuilder_CubeBlock"):
            sub_type_name = self.get_block_name(block)

            if sub_type_name in used_blocks.keys():
                used_blocks[sub_type_name] += 1
            else:
                used_blocks[sub_type_name] = 1

        return used_blocks

    def check_components(self, blocks: dict) -> dict:
        """
        Checks the components required for blocks

        :param blocks: a dict of the blocks
        :return: dict
        """
        used_components = {}
        unknown_blocks = []
        for block, b_quantity in blocks.items():
            if block not in self.blocks.keys():
                # don't know what this block is
                my_log.warn(f"Unknown block type: {block}")
                unknown_blocks.append(block)
                continue

            for component, c_quantity in self.blocks[block]["components"].items():
                if component in used_components.keys():
                    used_components[component] += c_quantity * b_quantity
                else:
                    used_components[component] = c_quantity * b_quantity

        return {"components": used_components,
                "unknown_blocks": unknown_blocks}

    # TODO: I'm sure this name won't become confusing at all
    def check_mats(self, components: dict) -> dict:
        """
        Estimates the materials required to build the components

        :param components: a dict of the components
        :return: dict
        """
        used_materials = {}
        unknown_components = []
        for component, c_quantity in components.items():
            if component not in self.components.keys():
                # unknown component type
                my_log.warn(f"Unknown component type: {component}")
                unknown_components.append(component)
                continue

            for material, m_quantity in self.components[component]["materials"].items():
                if material in used_materials.keys():
                    used_materials[material] += m_quantity * c_quantity
                else:
                    used_materials[material] = m_quantity * c_quantity

        return {"materials": used_materials,
                "unknown_components": unknown_components}

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
            for k, v in block.attrib.items():
                block_name = v.split("_")[1]
            my_log.info(f"Trying block_name: {block_name}")

        return block_name
