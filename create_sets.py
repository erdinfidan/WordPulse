import json
import os
from datetime import datetime

# Configuration
REPO_URL_BASE = "https://raw.githubusercontent.com/erdinfidan/WordPulse/main/sets"
CATEGORY_MAPPING = {
    "conjunctions": "YÖKDİL-YDS BAĞLAÇLAR",
    "verbs": "AKADEMİK KELİMELER",
    "nouns": "AKADEMİK KELİMELER",
    "phrasal_verbs": "AKADEMİK KELİMELER",
}


def get_file_size_str(filepath):
    """Returns file size in KB as a string (e.g. '1.2 KB')"""
    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes / 1024
    return f"{size_kb:.1f} KB"


def main():
    # Read the original words.json
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: words.json not found.")
        return

    # Create sets directory if it doesn't exist
    os.makedirs("sets", exist_ok=True)

    sets_metadata_list = []

    print("Starting set generation...")

    # Create individual set files
    for set_data in data["sets"]:
        set_id = set_data["id"]
        words = set_data["words"]

        # 1. Create individual set file content
        # We only keep essential data for the individual file to keep it light if needed,
        # or we can keep it as is. The previous script kept 'setId', 'version', 'words'.
        set_file_content = {
            "setId": set_id,
            "version": "1.0.0",  # Could be dynamic if we tracked versions
            "words": words,
        }

        # Write to file
        filename = f"sets/{set_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(set_file_content, f, ensure_ascii=False, indent=2)

        # 2. Collect Metadata for sets.json
        file_size = get_file_size_str(filename)
        word_count = len(words)

        # Map category key to display name
        raw_category = set_data.get("category", "Uncategorized")
        display_category = CATEGORY_MAPPING.get(raw_category, raw_category.upper())

        # Build metadata object
        metadata = {
            "id": set_id,
            "name": set_data["name"],
            "description": set_data["description"],
            "icon": set_data.get("icon", "📝"),  # Default icon if missing
            "category": display_category,
            "wordCount": word_count,
            "fileUrl": f"{REPO_URL_BASE}/{set_id}.json",
            "size": file_size,
            "difficulty": set_data.get(
                "difficulty", "intermediate"
            ),  # Default to intermediate
            "version": "1.0.0",
        }

        sets_metadata_list.append(metadata)
        print(f"Generated {filename} ({word_count} words, {file_size})")

    # 3. Generate sets.json
    sets_manifest = {
        "version": "1.0.0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "sets": sets_metadata_list,
    }

    with open("sets.json", "w", encoding="utf-8") as f:
        json.dump(sets_manifest, f, ensure_ascii=False, indent=4)

    print(f"\nsets.json updated successfully with {len(sets_metadata_list)} sets!")


if __name__ == "__main__":
    main()
