import json
import pathlib

from .utils import (
    apply_places,
    apply_tellers,
    apply_titles,
    apply_translations,
    get_reference_chapters,
    load_places,
    load_story_lines,
    load_tellers,
    load_titles,
    load_translations,
)


def main():
    chapters_path = pathlib.Path(__file__).parents[1] / "chapters"
    dist_path = pathlib.Path(__file__).parents[1] / "dist"

    if not dist_path.exists():
        dist_path.mkdir()

    tellers = load_tellers()
    titles = load_titles()
    places = load_places()
    reference_chapters = get_reference_chapters()

    for chapter in chapters_path.glob("*.txt"):
        chapter_id = chapter.stem
        if chapter_id not in reference_chapters:
            continue

        try:
            story_lines = load_story_lines(reference_chapters[chapter_id])
            translations = load_translations(chapter)

            result = apply_translations(story_lines, translations)
            result = apply_titles(result, titles)
            result = apply_tellers(result, tellers)
            result = apply_places(result, places)
        except Exception as e:
            print(f"Error processing chapter {chapter_id}: {e}")
            raise e

        with open(dist_path / f"{chapter_id}.json", "w", encoding="utf-8-sig") as f:
            json.dump(
                {"dataList": [line.export() for line in result]},
                f,
                ensure_ascii=False,
                indent=2,
            )

    print("Done!")


if __name__ == "__main__":
    main()
