import json
import os

# Read the original words.json
with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create sets directory if it doesn't exist
os.makedirs('sets', exist_ok=True)

# Create individual set files
for set_data in data['sets']:
    set_id = set_data['id']
    
    # Create individual set file
    set_file = {
        "setId": set_id,
        "version": "1.0.0",
        "words": set_data['words']
    }
    
    # Write to file
    filename = f'sets/{set_id}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(set_file, f, ensure_ascii=False, indent=2)
    
    print(f'✅ Created {filename} with {len(set_data["words"])} words')

print('\n🎉 All set files created successfully!')
