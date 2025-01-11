from enum import StrEnum

class Environment(StrEnum):
    LOCAL = "local", "local"
    DEVELOPMENT = "development", "dev"
    STAGING = "staging", "stg"
    PRODUCTION = "production", "prod"
    TESTING = "testing", "test"

    def __new__(cls, value, suffix):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._suffix = suffix
        return obj

    @property
    def suffix(self):
        return self._suffix

    def get_file_name(self):
        return f".env.{self.suffix}"

    @classmethod
    def _is_valid_value(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def _get_valid_values(cls):
        return [member.value for member in cls]

    @classmethod
    def check_value(cls, value: str):
        if not cls._is_valid_value(value):
            raise ValueError(
                f"{value} is not a valid Environment value. Valid values are: {', '.join(cls._get_valid_values())}"
            )