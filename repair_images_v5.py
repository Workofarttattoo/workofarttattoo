import os
import json
import re
import random

# Load mapped categories
with open('image_categories.json', 'r') as f:
    categories = json.load(f)

tattoos = list(dict.fromkeys(categories['tattoos']))
piercings = list(dict.fromkeys(categories['piercings']))
portraits = categories['portraits']

# Requested hero images
lion = "https://lh3.googleusercontent.com/aida/ADBb0ui962ZNifjFkcUZStfzEN5z-uWjPoLrGTjK8-VF_fopnxv4O5VVedPLXCpUUkI3fcasHTfXXwZi0dpah8BXlnOOqDzSdGv6c_P_40R7hm01mbfDDTm38EXUEUClAJLdDM16kZML7HKO7p7RorNvYXtzFaLelj-a5If0orYsNZN1di22VSZkcyImxorco3qho3eF5RkbGOncWRV5Ia7rTd6hflZQ12UK48kRFfdr2qMw1ACZQYR0d8O7F5Ku"
eye = "https://lh3.googleusercontent.com/aida/ADBb0ujX5zR7cDR5ICLMAURVNMcCVq1By24AFEkZUtyzaamYVTDDfWk1LZoVrntJLAnBSaEAxt45dPqBUV7MOxcUwud4_v8Cb0iaYlldZtihJCFZ3licYiYJ93-DBfA_9ilA4ayXbrsYHnlcVozhJfthaMWA_DTQMEqZi4ee6ZJg4q4Rufq8ttcBBAxFM_OEtiYaW04A6YgDpKAoQTfK_3Pqe3iEayd3WIgXNHl3qz7dNJE7V0Fq7mIR1phDzL4"
statue = "https://lh3.googleusercontent.com/aida/ADBb0uiYzEt9H0_X-3jbs6h7P3-JUZr1PABlIoJMmKghxpRg1xDvNCD8Bub0qFUzSKu9yMXo8wgHTJnqwwJiJm_q7LEnak1gP_MDgyb5YfTHS6_vqWiZkiNo6n6MmIy3RCsqhSSjbNw4U18e7DhXEI8BYTOoFAlKpO0opBOOd7qWqJpdZXh5qkvXsJhVLPPXVoRmZd48Q53L8Q8asedcUiaHmZKOJN2NDCLggOENGzLpfxvr9LwdjVcIpnUxFJZe"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find all occurrences of image URLs (not just unique ones)
    url_pattern = re.compile(r'https://lh3\.googleusercontent\.com/[^"\')\s<>]+')
    matches = url_pattern.finditer(content)

    # We will build a new content string by replacing each match with a unique selection from pool
    random.seed(filepath)
    is_piercing = any(x in filepath.lower() for x in ["piercing", "katelyn", "jewelry"])
    pool = piercings if is_piercing else tattoos

    # Prepare pool with variety
    shuffled_pool = pool[:]
    random.shuffle(shuffled_pool)

    # Hero logic
    prio = []
    if "home" in filepath.lower(): prio = [lion, eye, statue]
    elif "joshua" in filepath.lower(): prio = [portraits["Joshua Cole"], statue, lion]
    elif "jay_jay" in filepath.lower(): prio = [eye, lion, statue]
    elif "katelyn" in filepath.lower(): prio = [portraits["Katelyn Cole"]]

    new_content = []
    last_idx = 0
    match_count = 0

    for m in matches:
        new_content.append(content[last_idx:m.start()])

        replacement = ""
        if match_count < len(prio):
            replacement = prio[match_count]
        else:
            # Pick from pool, rotating with a high enough offset to ensure variety
            # Use match_count to keep it different for every single slot
            idx = (match_count + 5) % len(shuffled_pool)
            replacement = shuffled_pool[idx]

        new_content.append(replacement)
        last_idx = m.end()
        match_count += 1

    new_content.append(content[last_idx:])

    if match_count > 0:
        with open(filepath, 'w') as f:
            f.write("".join(new_content))
        return True
    return False

files_to_update = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') or file.endswith('.svelte'):
            files_to_update.append(os.path.join(root, file))

updated = 0
for filepath in files_to_update:
    if process_file(filepath):
        updated += 1

print(f"Variety-enriched update complete for {updated} files.")
