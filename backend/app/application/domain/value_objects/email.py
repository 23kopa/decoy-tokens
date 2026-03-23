import re


class Email:
    _pattern = re.compile(r".+@.+\..+")

    def __init__(self, value: str):
        if not self._pattern.match(value):
            raise ValueError("Invalid email")
        self.value = value

    def __str__(self) -> str:
        return self.value
