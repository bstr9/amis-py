from ..base import BaseComponent
from .properties import FormItemProperties


class FormItem(BaseComponent):
    __type = "form-item"

    def __init__(
        self,
        props: FormItemProperties
    ):
        self.__view = {
            "type": self.__type,
            "name": "",
            "label": props.get("label"),
        }
