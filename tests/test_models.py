import xml.etree.ElementTree as ElementTree

from models import Block, Recipe


class TestBlock:
    """
    A test block class for Block class tests
    """
    def test_new_block(self):
        """
        Make a new empty block
        """
        block = Block()

        assert block.type_id is None
        assert block.sub_type_id is None
        assert block.display_name is None
        assert block.components == {}

    def test_new_block_from_element(self):
        """
        Make a new block from an element
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

        block = Block()
        block.from_element(block_element)

        assert block.type_id == type_id
        assert block.sub_type_id == sub_type_id
        assert block.display_name == display_name
        assert block.components == {components["sub_type"]: int(components["count"])}

    def test_new_block_from_element_no_subtype(self):
        """
        Make a new block from an element but SubtypeId is empty
        """
        type_id = "my-type-id"
        display_name = "my-display-name"
        components = {"sub_type": "Steel Plate", "count": "10"}

        block_element = ElementTree.Element("Definition")
        block_id_element = ElementTree.SubElement(block_element, "Id")
        ElementTree.SubElement(block_id_element, "TypeId").text = type_id
        ElementTree.SubElement(block_id_element, "SubtypeId")
        ElementTree.SubElement(block_element, "DisplayName").text = display_name
        component_element = ElementTree.SubElement(block_element, "Components")
        ElementTree.SubElement(component_element, "Component",
                               attrib={"Subtype": components["sub_type"],
                                       "Count": components["count"]})

        block = Block()
        block.from_element(block_element)

        assert block.type_id == type_id
        assert block.sub_type_id == type_id
        assert block.display_name == display_name

    def test_return_block_as_dict(self):
        """
        Return a block as a dict
        """
        type_id = "my-type-id"
        sub_type_id = "my-subtype-id"
        display_name = "my-display-name"
        components = {"Steel Plate": 10}

        block = Block()
        block.type_id = type_id
        block.sub_type_id = sub_type_id
        block.display_name = display_name
        block.components = components

        assert block.as_dict() == {
            "type_id": type_id,
            "sub_type_id": sub_type_id,
            "display_name": display_name,
            "components": components
        }


class TestRecipe:
    """
    A test recipe class for Recipe class tests
    """
    def test_new_recipe(self):
        """
        Make a new empty recipe
        """
        recipe = Recipe()

        assert recipe.materials == {}
        assert recipe.output_type_id is None
        assert recipe.output_quantity is None

    def test_new_recipe_from_element(self):
        """
        Make a new recipe from an element
        """
        type_id = "Component"
        amount = 1
        sub_type_id = "some-subtype-id"
        materials = {
            "mat-1": 20,
            "mat-2": 10
        }

        recipe_element = ElementTree.Element("Blueprint")
        ElementTree.SubElement(recipe_element, "Result",
                               attrib={"SubtypeId": sub_type_id,
                                       "Amount": amount,
                                       "TypeId": type_id})
        prerequisites_element = ElementTree.SubElement(recipe_element, "Prerequisites")
        for material, m_quantity in materials.items():
            ElementTree.SubElement(prerequisites_element, "Item",
                                   attrib={"SubtypeId": material,
                                           "Amount": m_quantity})

        recipe = Recipe()
        recipe.from_element(recipe_element)

        assert recipe.materials == materials
        assert recipe.output_quantity == amount
        assert recipe.output_type_id == sub_type_id

    def test_new_recipe_from_element_no_result(self):
        """
        Make a new recipe from an element but there is no Result element
        """
        recipe_element = ElementTree.Element("Blueprint")

        recipe = Recipe()
        recipe.from_element(recipe_element)

        assert recipe.materials == {}
        assert recipe.output_quantity is None
        assert recipe.output_type_id is None

    def test_new_recipe_from_element_not_component(self):
        """
        Make a new recipe from an element that is not a component
        """
        type_id = "Ingot"
        amount = 1
        sub_type_id = "some-subtype-id"
        materials = {
            "mat-1": 20,
            "mat-2": 10
        }

        recipe_element = ElementTree.Element("Blueprint")
        ElementTree.SubElement(recipe_element, "Result",
                               attrib={"SubtypeId": sub_type_id,
                                       "Amount": amount,
                                       "TypeId": type_id})

        recipe = Recipe()
        recipe.from_element(recipe_element)

        assert recipe.materials == {}
        assert recipe.output_quantity is None
        assert recipe.output_type_id is None

    def test_return_recipe_as_dict(self):
        """
        Return a recipe as a dictionary
        """
        amount = 1
        sub_type_id = "some-subtype-id"
        materials = {
            "mat-1": 20,
            "mat-2": 10
        }

        recipe = Recipe()
        recipe.materials = materials
        recipe.output_type_id = sub_type_id
        recipe.output_quantity = amount

        assert recipe.as_dict() == {
            "materials": materials,
            "output_type_id": sub_type_id,
            "output_quantity": amount
        }
