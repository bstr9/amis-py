from amis_py.components.base import Prop, Properties, BaseComponent


class PageProperties(Properties):
    # do not support remark, aside, toolbar and initApi now
    def __init__(self, *args, **kwargs):
        super().__init__()
        defaults = [
            Prop("title", str, ""),
            Prop("sub_title", str, ""),
            Prop("class_name", str, "", "className"),
        ]
        self.update_defaults(defaults)
        self.update_properties(**kwargs)


class Page(BaseComponent):
    pass
