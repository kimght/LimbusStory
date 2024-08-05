import pathlib

from .models import StoryLineDTO
from .utils import load_story_lines, load_translations, get_reference_chapters


def main():
    references = get_reference_chapters()
    chapters_path = pathlib.Path(__file__).parents[1] / "chapters"

    invalid_chapters = []
    for chapter_file in chapters_path.glob("*.txt"):
        chapter_id = chapter_file.stem
        if chapter_id not in references:
            continue

        try:
            translations = load_translations(chapter_file)
        except ValueError:
            invalid_chapters.append(chapter_id)
            print(f"Chapter {chapter_id} has invalid translations")
            continue

        story = load_story_lines(references[chapter_id])
        count_lines = 0
        for line in story:
            if line.id is not None and line.id < 0:
                continue
            if line.content:
                count_lines += 1

        if count_lines != len(translations):
            invalid_chapters.append(chapter_id)
            print(f"Chapter {chapter_id} has {count_lines} lines but {len(translations)} translations")

    if invalid_chapters:
        raise ValueError(f"Invalid chapters: {', '.join(invalid_chapters)}")

    print("All chapters are valid!")


if __name__ == '__main__':
    main()
