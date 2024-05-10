import xml.etree.ElementTree as ElementTree


class Block:
    """
    Contains block details
    """
    def __init__(self, element: ElementTree):
        """
        Create a block class

        :param element: an XML element to create a block from
        """
        self.type_id = None
        self.sub_type_id = None
        self.display_name = None

        self.from_element(element)

    def from_element(self, element: ElementTree) -> None:
        """
        Populate a block from an element

        :param element: an XML element to create a block from
        :return: None
        """
        this_id = element.find("Id")

        self.type_id = this_id.find("TypeId").text
        self.sub_type_id = this_id.find("SubtypeId").text
        self.display_name = element.find("DisplayName").text

        # weird case where sometimes SubTypeId is empty ??
        if self.sub_type_id is None:
            self.sub_type_id = self.type_id

    def as_dict(self) -> dict:
        """
        Output a block as a dict

        :return: dict
        """
        return {"type_id": self.type_id,
                "sub_type_id": self.sub_type_id,
                "display_name": self.display_name}
