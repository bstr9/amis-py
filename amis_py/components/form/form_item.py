from ..base import BaseComponent
from .properties import FormItemProperties


class FormItem(BaseComponent):
    def __init__(
        self,
        props: FormItemProperties
    ):
        super().__init__()
        self._type = "form-item"
        self._view = {
            "type": self._type,
            "name": "",
            "label": props.get("label"),
        }
