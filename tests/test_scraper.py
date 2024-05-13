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
        config = {"some-key": "some-value"}

        scraper = Scraper(config)

        assert scraper.all_blocks == {}
        assert scraper.config == config

    def test_load_blocks_from_directory(self):
        """
        Load blocks from an xml file in a directory
        """
        type_id = "my-type-id"
        sub_type_id = "my-subtype-id"
        display_name = "my-display-name"

        block_element = ElementTree.Element("Definition")
        block_id_element = ElementTree.SubElement(block_element, "Id")
        ElementTree.SubElement(block_id_element, "TypeId").text = type_id
        ElementTree.SubElement(block_id_element, "SubtypeId").text = sub_type_id
        ElementTree.SubElement(block_element, "DisplayName").text = display_name

        with TemporaryDirectory() as test_dir:
            scraper = Scraper({"se_path": test_dir})

            xml_path = os.path.join(test_dir, "my_xml_file.xml")
            element_tree = ElementTree.ElementTree(block_element)
            element_tree.write(xml_path)

            scraper.load_blocks()

            assert len(scraper.all_blocks) == 1
            assert scraper.all_blocks[type_id] == {
                "type_id": type_id,
                "sub_type_id": sub_type_id,
                "display_name": display_name
            }

    def test_load_blocks_from_directory_non_xml_file(self):
        """
        Load blocks from a non xml file in a directory
        """
        with TemporaryDirectory() as test_dir:
            scraper = Scraper({"se_path": test_dir})

            xml_path = os.path.join(test_dir, "my_xml_file.xml")
            with open(xml_path, "w") as xml_file:
                xml_file.write("My non-XML content")

            scraper.load_blocks()

            assert len(scraper.all_blocks) == 0
            assert scraper.all_blocks == {}

    def test_load_blocks_from_directory_no_typeid_file(self):
        """
        Load blocks from an xml file without a TypeId in a directory
        """
        sub_type_id = "my-subtype-id"
        display_name = "my-display-name"

        block_element = ElementTree.Element("Definition")
        block_id_element = ElementTree.SubElement(block_element, "Id")
        ElementTree.SubElement(block_id_element, "TypeId")
        ElementTree.SubElement(block_id_element, "SubtypeId").text = sub_type_id
        ElementTree.SubElement(block_element, "DisplayName").text = display_name

        with TemporaryDirectory() as test_dir:
            scraper = Scraper({"se_path": test_dir})

            xml_path = os.path.join(test_dir, "my_xml_file.xml")
            element_tree = ElementTree.ElementTree(block_element)
            element_tree.write(xml_path)

            scraper.load_blocks()

            assert len(scraper.all_blocks) == 0
            assert scraper.all_blocks == {}
