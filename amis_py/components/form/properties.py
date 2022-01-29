from amis_py.components.base import Prop, Properties


class FormItemProperties(Properties):
    def __init__(self):
        super().__init__()
        self.defaults = [
            Prop("name", str, ""),
            Prop("label", str, ""),
            Prop("description", str, ""),
            Prop("inline", bool, None),
            Prop("disable", bool, None),
            Prop("visible", bool, None),
            Prop("required", bool, None),
            Prop("validations", str, ""),
            Prop("value", str, None)
        ]
