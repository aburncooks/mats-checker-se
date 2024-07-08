import os.path
import xml.etree.ElementTree as ElementTree
from tempfile import TemporaryDirectory

from scraper import Scraper


class TestScraper:
    """
    A test scraper class for Scraper class tests
    """
    def test_new_scraper(self):
        """
        Make a new Scraper class
        """
        scraper = Scraper()

        assert scraper.all_blocks == {}
        assert scraper.all_recipes == {}

    def test_load_blocks_from_directory(self):
        """
        Load blocks from an xml file in a directory
        """
        type_id = "my-type-id"
        sub_type_id = "my-subtype-id"
        display_name = "my-display-name"
        components = {"sub_type": "Steel Plate", "count": "10"}

        block_element = ElementTree.Element("Definition")
        block_id_element = ElementTree.SubElement(block_element, "Id")
        ElementTree.SubElement(block_id_element, "TypeId").text = type_id
        ElementTree.SubElement(block_id_element, "SubtypeId").text = sub_type_id
        ElementTree.SubElement(block_element, "DisplayName").text = display_name
        component_element = ElementTree.SubElement(block_element, "Components")
        ElementTree.SubElement(component_element, "Component",
                               attrib={"Subtype": components["sub_type"],
                                       "Count": components["count"]})

        with TemporaryDirectory() as test_dir:
            scraper = Scraper()

            xml_path = os.path.join(test_dir, "my_xml_file.sbc")
            element_tree = ElementTree.ElementTree(block_element)
            element_tree.write(xml_path)

            scraper.load_blocks(test_dir)

            assert len(scraper.all_blocks) == 1
            assert scraper.all_blocks[sub_type_id] == {
                "type_id": type_id,
                "sub_type_id": sub_type_id,
                "display_name": display_name,
                "components": {components["sub_type"]: int(components["count"])}
            }

    def test_load_blocks_from_directory_non_xml_sbc_file(self):
        """
        Load blocks from a non xml file in a directory
        """
        with TemporaryDirectory() as test_dir:
            scraper = Scraper()

            xml_path = os.path.join(test_dir, "my_xml_file.sbc")
            with open(xml_path, "w") as xml_file:
                xml_file.write("My non-XML content")

            scraper.load_blocks(test_dir)

            assert len(scraper.all_blocks) == 0
            assert scraper.all_blocks == {}

    def test_load_blocks_from_directory_non_sbc_file(self):
        """
        Load blocks from a non xml file in a directory
        """
        with TemporaryDirectory() as test_dir:
            scraper = Scraper()

            xml_path = os.path.join(test_dir, "my_xml_file.xml")
            with open(xml_path, "w") as xml_file:
                xml_file.write("My non-XML content")

            scraper.load_blocks(test_dir)

            assert len(scraper.all_blocks) == 0
            assert scraper.all_blocks == {}

    def test_load_blocks_from_directory_no_typeid_file(self):
        """
        Load blocks from an xml file without a TypeId in a directory
        """
        sub_type_id = "my-subtype-id"
        display_name = "my-display-name"
        components = {"sub_type": "Steel Plate", "count": "10"}

        block_element = ElementTree.Element("Definition")
        block_id_element = ElementTree.SubElement(block_element, "Id")
        ElementTree.SubElement(block_id_element, "TypeId")
        ElementTree.SubElement(block_id_element, "SubtypeId").text = sub_type_id
        ElementTree.SubElement(block_element, "DisplayName").text = display_name
        component_element = ElementTree.SubElement(block_element, "Components")
        ElementTree.SubElement(component_element, "Component",
                               attrib={"Subtype": components["sub_type"],
                                       "Count": components["count"]})

        with TemporaryDirectory() as test_dir:
            scraper = Scraper()

            xml_path = os.path.join(test_dir, "my_xml_file.sbc")
            element_tree = ElementTree.ElementTree(block_element)
            element_tree.write(xml_path)

            scraper.load_blocks(test_dir)

            assert len(scraper.all_blocks) == 0
            assert scraper.all_blocks == {}

    def test_load_blocks_from_missing_directory(self):
        """
        Load blocks from a directory that does not exist
        """
        scraper = Scraper()
        scraper.load_blocks("missing/path")

        assert len(scraper.all_blocks) == 0
        assert scraper.all_blocks == {}

    def test_load_blocks_from_file(self):
        """
        Load blocks from a file instead of directory
        """
        with TemporaryDirectory() as test_dir:
            scraper = Scraper()

            xml_path = os.path.join(test_dir, "my_xml_file.sbc")
            block_element = ElementTree.Element("Definition")
            element_tree = ElementTree.ElementTree(block_element)
            element_tree.write(xml_path)

            scraper.load_blocks(xml_path)

        assert len(scraper.all_blocks) == 0
        assert scraper.all_blocks == {}

    def test_load_recipes_from_directory(self):
        """
        Load recipes from an xml file in a directory
        """
        type_id = "Component"
        amount = "1"
        sub_type_id = "some-subtype-id"
        materials = {"sub_type": "mat-1", "count": "10"}

        recipe_element = ElementTree.Element("Blueprint")
        ElementTree.SubElement(recipe_element, "Result",
                               attrib={"SubtypeId": sub_type_id,
                                       "Amount": amount,
                                       "TypeId": type_id})
        prerequisites_element = ElementTree.SubElement(recipe_element, "Prerequisites")
        ElementTree.SubElement(prerequisites_element, "Item",
                               attrib={"SubtypeId": materials["sub_type"],
                                       "Amount": materials["count"]})

        with TemporaryDirectory() as test_dir:
            scraper = Scraper()

            xml_path = os.path.join(test_dir, "my_xml_file.sbc")
            element_tree = ElementTree.ElementTree(recipe_element)
            element_tree.write(xml_path)

            scraper.load_recipes(xml_path)

            assert len(scraper.all_recipes) == 1
            assert scraper.all_recipes[sub_type_id] == {
                "output_type_id": sub_type_id,
                "output_quantity": int(amount),
                "materials": {materials["sub_type"]: float(materials["count"])}
            }

    def test_load_recipes_from_missing_file(self):
        """
        Load recipes from a file that does not exist
        """
        scraper = Scraper()
        scraper.load_recipes("missing/path")

        assert len(scraper.all_recipes) == 0
        assert scraper.all_recipes == {}
