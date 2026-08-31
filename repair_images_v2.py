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

def get_random_images(source_list, count):
    if len(source_list) >= count:
        return random.sample(source_list, count)
    else:
        # If not enough, repeat but shuffle
        res = source_list[:]
        while len(res) < count:
            res.extend(random.sample(source_list, len(source_list)))
        return res[:count]

def replace_in_file(filepath, mapping):
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to replace existing https://lh3.googleusercontent.com/aida/ADBb... URLs
    # OR the old aida-public ones if any remain.
    # Actually, let's just find all image URLs in <img> src and style background-image

    def replacer(match):
        url = match.group(0)
        # Only replace if it looks like a googleusercontent URL we've been messing with
        if "lh3.googleusercontent.com" in url:
            # Check context or just rotate?
            # Better to use a specific mapping per file type
            return mapping.get(url, url)
        return url

    # Pattern for URLs in double/single quotes
    pattern = re.compile(r'https://lh3\.googleusercontent\.com/[^"\')\s<>]+')

    # Actually, it's easier to just find all matches and replace them one by one with a rotation
    matches = pattern.findall(content)
    new_content = content

    # Use a seed for deterministic but varied results per file
    random.seed(filepath)

    # Decide which pool to use based on file content/name
    pool = tattoos
    if "piercing" in filepath.lower() or "katelyn" in filepath.lower():
        pool = piercings

    available_pool = pool[:]
    random.shuffle(available_pool)

    unique_matches = list(dict.fromkeys(matches))
    for i, old_url in enumerate(unique_matches):
        # Specific overrides
        new_url = None
        if "joshua" in filepath.lower() and i == 0: # Likely first image is portrait
             new_url = portraits["Joshua Cole"]
        elif "katelyn" in filepath.lower() and i == 0:
             new_url = portraits["Katelyn Cole"]
        else:
             new_url = available_pool[i % len(available_pool)]

        new_content = new_content.replace(old_url, new_url)

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
    replace_in_file(filepath, {})

print("Done.")
