from osbot_utils.helpers.html.Tag__Base import Tag__Base


class Tag__Link(Tag__Base):
    end_tag  : bool = False
    tag_name : str  = 'link'
    href     : str
    rel      : str
    integrity: str
