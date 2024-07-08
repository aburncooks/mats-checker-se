import os.path
import xml.etree.ElementTree as ElementTree
from tempfile import TemporaryDirectory

from bp_checker import BluePrintChecker


class TestBluePrintChecker:
    """
    A test blue print checker class for BluePrintChecker class tests
    """
    def test_new_bpc(self):
        blocks = {
          "CubeBlock": {
            "type_id": "CubeBlock",
            "sub_type_id": "SmallWindowRoundInwardsCornerInv",
            "display_name": "DisplayName_Block_WindowRoundInwardsCornerInv",
            "components": {
              "SteelPlate": 10
            }
          }
        }

        recipes = {
            "SteelPlate": {
                "materials": {
                    "Iron": 21.0
                },
                "output_type_id": "SteelPlate",
                "output_quantity": 1.0
            }
        }

        bpc = BluePrintChecker(blocks, recipes)

        assert bpc.blocks == blocks
        assert bpc.components == recipes

    def test_open_bp(self):
        """
        Open a blueprint file
        """
        blocks = {
          "CubeBlock": {
            "type_id": "CubeBlock",
            "sub_type_id": "SmallWindowRoundInwardsCornerInv",
            "display_name": "DisplayName_Block_WindowRoundInwardsCornerInv",
            "components": {
              "SteelPlate": 10
            }
          }
        }

        recipes = {
            "SteelPlate": {
                "materials": {
                    "Iron": 21.0
                },
                "output_type_id": "SteelPlate",
                "output_quantity": 1.0
            }
        }

        bpc = BluePrintChecker(blocks, recipes)
        element = ElementTree.Element("MyKey")

        with TemporaryDirectory() as test_dir:
            xml_path = os.path.join(test_dir, "my_bp_file.xml")
            element_tree = ElementTree.ElementTree(element)
            element_tree.write(xml_path)

            my_bp = bpc.open_blueprint(xml_path)

            assert ElementTree.dump(my_bp) == ElementTree.dump(element)  # this feels cursed

    def test_open_non_xml_bp(self):
        """
        Open a blueprint file that isn't XML
        """
        bpc = BluePrintChecker({}, {})

        with TemporaryDirectory() as test_dir:
            xml_path = os.path.join(test_dir, "my_bp_file.xml")
            with open(xml_path, "w") as xml_file:
                xml_file.write("Some non-XML text")

            my_bp = bpc.open_blueprint(xml_path)

            assert my_bp == ElementTree  # this also feels cursed

    def test_get_block_name(self):
        """
        Get a block name from SubtypeName
        """
        bpc = BluePrintChecker({}, {})
        sub_type_name = "FancyBlockName"

        block_element = ElementTree.Element("xyz_SomeBlock", attrib={"xsi:type": "xyz_SomeBlock"})
        ElementTree.SubElement(block_element, "SubtypeName").text = sub_type_name

        name = bpc.get_block_name(block_element)

        assert name == sub_type_name

    def test_get_block_name_no_subtypename(self):
        """
        Get a block name without SubtypeName
        """
        bpc = BluePrintChecker({}, {})
        sub_name = "FancyBlockName"

        block_element = ElementTree.Element(f"xyz_{sub_name}", attrib={"xsi:type": f"xyz_{sub_name}"})
        ElementTree.SubElement(block_element, "SubtypeName")

        name = bpc.get_block_name(block_element)

        assert name == sub_name

    def test_check_blocks(self):
        """
        Check the blocks quantity from a tree
        """
        sub_type_name = "MyBlock"
        another_name = "MyOtherBlock"

        grid_element = ElementTree.Element("CubeGrid")
        blocks_element = ElementTree.SubElement(grid_element, "CubeBlocks")
        block_element = ElementTree.SubElement(blocks_element, "MyObjectBuilder_CubeBlock")
        ElementTree.SubElement(block_element, "SubtypeName").text = sub_type_name
        block_element = ElementTree.SubElement(blocks_element, "MyObjectBuilder_CubeBlock")
        ElementTree.SubElement(block_element, "SubtypeName").text = sub_type_name
        block_element = ElementTree.SubElement(blocks_element, "MyObjectBuilder_CubeBlock")
        ElementTree.SubElement(block_element, "SubtypeName").text = another_name

        tree = ElementTree.ElementTree(grid_element)
        used_blocks = {
            sub_type_name: 2,
            another_name: 1
        }

        bpc = BluePrintChecker({}, {})
        blocks = bpc.check_blocks(tree)

        assert used_blocks == blocks

    def test_check_components(self):
        """
        Check the components quantity for some blocks
        """
        all_blocks = {
          "LargeRailStraight": {
            "type_id": "CubeBlock",
            "sub_type_id": "LargeRailStraight",
            "display_name": "LargeRailStraight",
            "components": {
              "SteelPlate": 12,
              "Construction": 8
            }
          }
        }

        used_blocks = {
            "LargeRailStraight": 2,
            "AnotherBlock": 5
        }

        bpc = BluePrintChecker(all_blocks, {})
        components = bpc.check_components(used_blocks)

        assert components["components"] == {"SteelPlate": 24, "Construction": 16}
        assert components["unknown_blocks"] == ["AnotherBlock"]

    def test_check_mats(self):
        all_recipes = {
            "SteelPlate": {
                "materials": {
                    "Iron": 21.0
                },
                "output_type_id": "SteelPlate",
                "output_quantity": 1.0
            }
        }

        used_components = {
            "SteelPlate": 10,
            "AnotherComponent": 11
        }

        bpc = BluePrintChecker({}, all_recipes)
        mats = bpc.check_mats(used_components)

        assert mats["materials"] == {"Iron": 210.0}
        assert mats["unknown_components"] == ["AnotherComponent"]
