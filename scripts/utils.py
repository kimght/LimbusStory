import copy
import json
import pathlib
import re

from .models import StoryLineDTO, TellerDTO, TitleDTO


def get_reference_chapters() -> dict[str, pathlib.Path]:
    path = pathlib.Path(__file__).parents[1] / "reference"

    if not path.exists():
        raise FileNotFoundError(f"Reference directory not found: {path}")

    return {file.stem: file for file in path.glob("*.json") if file.is_file()}


def load_story_lines(filename: str | pathlib.Path) -> list[StoryLineDTO]:
    with open(filename, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if "dataList" not in data:
        raise ValueError(f"Invalid file format: {filename}")

    return [StoryLineDTO.from_dict(line) for line in data["dataList"]]


def load_tellers() -> list[TellerDTO]:
    tellers_extra = pathlib.Path(__file__).parents[1] / "extra" / "tellers.json"

    if tellers_extra.exists():
        with tellers_extra.open("r", encoding="utf-8-sig") as f:
            tellers = json.load(f)
    else:
        tellers = []

    return [TellerDTO(**teller) for teller in tellers]


def load_titles() -> list[TitleDTO]:
    titles_extra = pathlib.Path(__file__).parents[1] / "extra" / "titles.json"

    if titles_extra.exists():
        with titles_extra.open("r", encoding="utf-8-sig") as f:
            titles = json.load(f)
    else:
        titles = []

    return [TitleDTO(**title) for title in titles]


def load_places() -> dict[str, str]:
    places_extra = pathlib.Path(__file__).parents[1] / "extra" / "places.json"

    if places_extra.exists():
        with places_extra.open("r", encoding="utf-8-sig") as f:
            places = json.load(f)
    else:
        places = {}

    return places


def save_tellers(tellers: list[TellerDTO]) -> None:
    tellers_extra = pathlib.Path(__file__).parents[1] / "extra" / "tellers.json"

    with tellers_extra.open("w", encoding="utf-8-sig") as f:
        json.dump(
            [teller.export() for teller in tellers], f, ensure_ascii=False, indent=2
        )


def save_titles(titles: list[TitleDTO]) -> None:
    titles_extra = pathlib.Path(__file__).parents[1] / "extra" / "titles.json"

    with titles_extra.open("w", encoding="utf-8-sig") as f:
        json.dump([title.export() for title in titles], f, ensure_ascii=False, indent=2)


def load_translations(filename: str | pathlib.Path) -> list[str]:
    with open(filename, "r", encoding="utf-8-sig") as f:
        content = f.read().strip()

    clean_lines = []
    for line in content.split("\n"):
        if line.strip().startswith("#"):
            continue
        clean_lines.append(line.strip())

    split_re = re.compile(r"\n{2,}", re.MULTILINE)
    result = []
    for line in split_re.split("\n".join(clean_lines)):
        if ":" not in line:
            raise ValueError(f"Invalid line format: {line}")
        line = line.split(":", 1)[1].strip()
        line = line.replace("\n[KEEP_LINE]\n", "\n\n")
        result.append(line)

    return result


def apply_translations(
    lines: list[StoryLineDTO], translations: list[str]
) -> list[StoryLineDTO]:
    result = copy.deepcopy(lines)
    current_id = 0
    for line in result:
        if not line.content or (line.id is not None and line.id < 0):
            continue
        if current_id >= len(translations):
            raise ValueError("Not enough translations")
        line.content = translations[current_id]
        current_id += 1
    if current_id != len(translations):
        raise ValueError("Too many translations")
    return result


def apply_tellers(
    lines: list[StoryLineDTO], tellers: list[TellerDTO]
) -> list[StoryLineDTO]:
    result = copy.deepcopy(lines)
    for line in result:
        if not line.teller:
            continue
        for teller in tellers:
            if teller.original == line.teller and teller.model == line.model:
                line.teller = teller.translation
                break
        else:
            print("Warning: teller not found", line.teller, line.model)
            continue
    return result


def apply_titles(
    lines: list[StoryLineDTO], titles: list[TitleDTO]
) -> list[StoryLineDTO]:
    result = copy.deepcopy(lines)
    for line in result:
        if not line.title:
            continue
        for title in titles:
            if title.original == line.title and title.model == line.model:
                line.title = title.translation
                break
        else:
            print("Warning: title not found", line.title, line.model)
            continue
    return result


def apply_places(
    lines: list[StoryLineDTO], places: dict[str, str]
) -> list[StoryLineDTO]:
    result = copy.deepcopy(lines)
    for line in result:
        if not line.place:
            continue
        if line.place in places:
            line.place = places[line.place]
        else:
            print("Warning: place not found", line.place)
            continue
    return result
