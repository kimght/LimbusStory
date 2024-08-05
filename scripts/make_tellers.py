from .models import TellerDTO
from .utils import get_reference_chapters, load_story_lines, load_tellers, save_tellers


def main() -> None:
    tellers = load_tellers()

    reference_chapters = get_reference_chapters()
    for i, (chapter_name, chapter_path) in enumerate(reference_chapters.items(), start=1):
        print(f"Processing {chapter_name} [{i}/{len(reference_chapters)}]...")

        story_lines = load_story_lines(chapter_path)
        for line in story_lines:
            if line.teller is None:
                continue

            if any(teller.model == line.model and teller.original == line.teller for teller in tellers):
                continue

            print("New teller found:", line.teller, "for", line.model)
            translation = input("Enter translation: ")
            tellers.append(
                TellerDTO(original=line.teller, translation=translation, model=line.model)
            )

    save_tellers(tellers)
    print("Done!")


if __name__ == "__main__":
    main()
