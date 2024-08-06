import json
import pathlib

from .utils import get_reference_chapters, load_story_lines


def main() -> None:
    places_extra = pathlib.Path(__file__).parents[1] / "extra" / "places.json"

    if places_extra.exists():
        with places_extra.open("r", encoding="utf-8-sig") as f:
            places = json.load(f)
    else:
        places = {}

    reference_chapters = get_reference_chapters()
    for i, (chapter_name, chapter_path) in enumerate(
        reference_chapters.items(), start=1
    ):
        print(f"Processing {chapter_name} [{i}/{len(reference_chapters)}]...")

        story_lines = load_story_lines(chapter_path)
        for line in story_lines:
            if line.place is None:
                continue
            if line.place in places:
                continue

            print("New place found:", line.place)
            translation = input("Enter translation: ")
            places[line.place] = translation

    with places_extra.open("w", encoding="utf-8-sig") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)

    print("Done!")


if __name__ == "__main__":
    main()
