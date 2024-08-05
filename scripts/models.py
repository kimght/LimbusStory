import collections
import dataclasses

__all__ = ("StoryLineDTO", "TellerDTO", "TitleDTO")


@dataclasses.dataclass
class StoryLineDTO:
    id: int | None = None
    place: str | None = None
    model: str | None = None
    teller: str | None = None
    title: str | None = None
    content: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "StoryLineDTO":
        return cls(
            id=data.get("id"),
            place=data.get("place"),
            model=data.get("model"),
            teller=data.get("teller"),
            title=data.get("title"),
            content=data.get("content")
        )

    def export(self) -> dict:
        field_list = [
            ("id", self.id),
            ("place", self.place),
            ("model", self.model),
            ("teller", self.teller),
            ("title", self.title),
            ("content", self.content)
        ]

        return collections.OrderedDict(
            (key, value) for key, value in field_list
            if value is not None or key == "id"
        )


@dataclasses.dataclass
class ModelRelatedTranslationBase:
    original: str
    translation: str
    model: str | None = None

    def export(self) -> dict:
        field_list = [
            ("original", self.original),
            ("translation", self.translation),
            ("model", self.model)
        ]

        return collections.OrderedDict(
            (key, value) for key, value in field_list if value is not None
        )


@dataclasses.dataclass
class TellerDTO(ModelRelatedTranslationBase):
    pass


@dataclasses.dataclass
class TitleDTO(ModelRelatedTranslationBase):
    pass
