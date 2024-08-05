from .models import TitleDTO
from .utils import get_reference_chapters, load_story_lines, load_titles, save_titles


def main() -> None:
    titles = load_titles()

    reference_chapters = get_reference_chapters()
    for i, (chapter_name, chapter_path) in enumerate(reference_chapters.items(), start=1):
        print(f"Processing {chapter_name} [{i}/{len(reference_chapters)}]...")

        story_lines = load_story_lines(chapter_path)
        for line in story_lines:
            if line.title is None:
                continue

            if any(title.model == line.model and title.original == line.title for title in title):
                continue

            print("New title found:", line.title, "for", line.model)
            translation = input("Enter translation: ")
            titles.append(
                TitleDTO(original=line.title, translation=translation, model=line.model)
            )

    save_titles(titles)
    print("Done!")


if __name__ == "__main__":
    main()
