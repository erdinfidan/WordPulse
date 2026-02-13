import json
import argparse
import os


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def import_from_txt(txt_file, json_file="words.json"):
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    data = load_json(json_file)
    sets_dict = {s["id"]: s for s in data["sets"]}

    updated_count = 0
    added_count = 0
    skipped_count = 0

    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):  # Skip empty lines and comments
                    continue

                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 3:
                    print(
                        f"Skipping line {line_num}: Invalid format (expected set_id | text | meaning)"
                    )
                    skipped_count += 1
                    continue

                set_id, text, meaning = parts[0], parts[1], parts[2]

                if set_id not in sets_dict:
                    print(f"Skipping line {line_num}: Set ID '{set_id}' not found.")
                    skipped_count += 1
                    continue

                target_set = sets_dict[set_id]

                # Check if word exists in this set
                existing_word = next(
                    (
                        w
                        for w in target_set["words"]
                        if w["text"].lower() == text.lower()
                    ),
                    None,
                )

                if existing_word:
                    if existing_word["meaning"] != meaning:
                        existing_word["meaning"] = meaning
                        updated_count += 1
                    else:
                        # Identical text and meaning, no change needed
                        pass
                else:
                    target_set["words"].append({"text": text, "meaning": meaning})
                    added_count += 1

        if added_count > 0 or updated_count > 0:
            save_json(json_file, data)
            print(f"Successfully processed {txt_file}:")
            print(f" - {added_count} words added")
            print(f" - {updated_count} words updated")
            if skipped_count > 0:
                print(f" - {skipped_count} lines skipped")
        else:
            print(f"No changes made from {txt_file}.")

    except FileNotFoundError:
        print(f"Error: TXT file '{txt_file}' not found.")
    except Exception as e:
        print(f"Error reading TXT: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Import/Update words from TXT to words.json"
    )
    parser.add_argument(
        "file", help="Path to the TXT file (format: set_id | text | meaning)"
    )

    args = parser.parse_args()

    import_from_txt(args.file)
