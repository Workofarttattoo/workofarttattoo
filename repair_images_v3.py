import os
import json
import re
import random

# Load mapped categories
with open('image_categories.json', 'r') as f:
    categories = json.load(f)

tattoos = categories['tattoos']
piercings = categories['piercings']
portraits = categories['portraits']

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find all unique googleusercontent URLs
    pattern = re.compile(r'https://lh3\.googleusercontent\.com/[^"\')\s<>]+')
    matches = pattern.findall(content)
    unique_matches = []
    seen = set()
    for m in matches:
        if m not in seen:
            unique_matches.append(m)
            seen.add(m)

    if not unique_matches:
        return

    # Use a seed for deterministic but varied results per file
    random.seed(filepath)

    # Decide pool based on file content/name
    pool = tattoos
    is_piercing = "piercing" in filepath.lower() or "katelyn" in filepath.lower()
    if is_piercing:
        pool = piercings

    # Special pool for portraits if we are at the beginning of an artist page
    available_pool = pool[:]
    random.shuffle(available_pool)

    # Construct a mapping for this file
    mapping = {}
    for i, old_url in enumerate(unique_matches):
        new_url = None
        # Logic to pick the right image
        if "joshua" in filepath.lower() and i == 0:
             new_url = portraits["Joshua Cole"]
        elif "katelyn" in filepath.lower() and i == 0:
             new_url = portraits["Katelyn Cole"]
        else:
             # Pick from pool, ensure we don't just use the first one if we can help it
             # and avoid using portraits in general grids
             new_url = available_pool[i % len(available_pool)]

        mapping[old_url] = new_url

    # Perform replacement
    # Use a more careful approach to avoid partial replacements or re-replacing
    # We'll use a temporary placeholder or a single pass regex replacement
    def multiple_replace(text, adict):
        # Sort keys by length long to short to avoid partial matches
        sorted_keys = sorted(adict.keys(), key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(k) for k in sorted_keys))
        return pattern.sub(lambda m: adict[m.group(0)], text)

    new_content = multiple_replace(content, mapping)

    with open(filepath, 'w') as f:
        f.write(new_content)

# Targeted files
files_to_update = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') or file.endswith('.svelte'):
            files_to_update.append(os.path.join(root, file))

for filepath in files_to_update:
    print(f"Updating {filepath}...")
    replace_in_file(filepath)

print("Done.")
