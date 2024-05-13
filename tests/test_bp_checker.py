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
          'CubeBlock': {
            'type_id': 'CubeBlock',
            'sub_type_id': 'SmallWindowRoundInwardsCornerInv',
            'display_name': 'DisplayName_Block_WindowRoundInwardsCornerInv'
          }
        }

        bpc = BluePrintChecker(blocks)

        assert bpc.blocks == blocks

    def test_open_bp(self):
        """
        Open a blueprint file
        """
        blocks = {
          'CubeBlock': {
            'type_id': 'CubeBlock',
            'sub_type_id': 'SmallWindowRoundInwardsCornerInv',
            'display_name': 'DisplayName_Block_WindowRoundInwardsCornerInv'
          }
        }

        bpc = BluePrintChecker(blocks)
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
        bpc = BluePrintChecker({})

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
        bpc = BluePrintChecker({})
        sub_type_name = "FancyBlockName"

        block_element = ElementTree.Element("xyz_SomeBlock", attrib={"xsi:type": "xyz_SomeBlock"})
        ElementTree.SubElement(block_element, "SubtypeName").text = sub_type_name

        name = bpc.get_block_name(block_element)

        assert name == sub_type_name

    def test_get_block_name_no_subtypename(self):
        """
        Get a block name without SubtypeName
        """
        bpc = BluePrintChecker({})
        sub_name = "FancyBlockName"

        block_element = ElementTree.Element(f"xyz_{sub_name}", attrib={"xsi:type": f"xyz_{sub_name}"})
        ElementTree.SubElement(block_element, "SubtypeName")

        name = bpc.get_block_name(block_element)

        assert name == sub_name
