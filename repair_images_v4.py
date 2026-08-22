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

# Highlight images requested by user
lion = "https://lh3.googleusercontent.com/aida/ADBb0ui962ZNifjFkcUZStfzEN5z-uWjPoLrGTjK8-VF_fopnxv4O5VVedPLXCpUUkI3fcasHTfXXwZi0dpah8BXlnOOqDzSdGv6c_P_40R7hm01mbfDDTm38EXUEUClAJLdDM16kZML7HKO7p7RorNvYXtzFaLelj-a5If0orYsNZN1di22VSZkcyImxorco3qho3eF5RkbGOncWRV5Ia7rTd6hflZQ12UK48kRFfdr2qMw1ACZQYR0d8O7F5Ku"
eye = "https://lh3.googleusercontent.com/aida/ADBb0ujX5zR7cDR5ICLMAURVNMcCVq1By24AFEkZUtyzaamYVTDDfWk1LZoVrntJLAnBSaEAxt45dPqBUV7MOxcUwud4_v8Cb0iaYlldZtihJCFZ3licYiYJ93-DBfA_9ilA4ayXbrsYHnlcVozhJfthaMWA_DTQMEqZi4ee6ZJg4q4Rufq8ttcBBAxFM_OEtiYaW04A6YgDpKAoQTfK_3Pqe3iEayd3WIgXNHl3qz7dNJE7V0Fq7mIR1phDzL4"
statue = "https://lh3.googleusercontent.com/aida/ADBb0uiYzEt9H0_X-3jbs6h7P3-JUZr1PABlIoJMmKghxpRg1xDvNCD8Bub0qFUzSKu9yMXo8wgHTJnqwwJiJm_q7LEnak1gP_MDgyb5YfTHS6_vqWiZkiNo6n6MmIy3RCsqhSSjbNw4U18e7DhXEI8BYTOoFAlKpO0opBOOd7qWqJpdZXh5qkvXsJhVLPPXVoRmZd48Q53L8Q8asedcUiaHmZKOJN2NDCLggOENGzLpfxvr9LwdjVcIpnUxFJZe"

def multiple_replace(text, adict):
    if not adict: return text
    sorted_keys = sorted(adict.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(k) for k in sorted_keys))
    return pattern.sub(lambda m: adict[m.group(0)], text)

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    url_pattern = re.compile(r'https://lh3\.googleusercontent\.com/[^"\')\s<>]+')
    matches = url_pattern.findall(content)
    unique_matches = []
    seen = set()
    for m in matches:
        if m not in seen:
            unique_matches.append(m)
            seen.add(m)

    if not unique_matches:
        return

    random.seed(filepath)
    is_piercing = any(x in filepath.lower() for x in ["piercing", "katelyn", "jewelry"])
    pool = piercings if is_piercing else tattoos

    # Shuffle pool for variety
    available_pool = pool[:]
    random.shuffle(available_pool)

    mapping = {}

    # Page-specific priority injections
    prio = []
    if "home" in filepath.lower():
        prio = [lion, eye, statue]
    elif "joshua" in filepath.lower():
        prio = [portraits["Joshua Cole"], statue, lion]
    elif "jay_jay" in filepath.lower():
        prio = [eye, lion, statue]
    elif "katelyn" in filepath.lower():
        prio = [portraits["Katelyn Cole"]]

    for i, old_url in enumerate(unique_matches):
        if i < len(prio):
            mapping[old_url] = prio[i]
        else:
            # Shift index to avoid using same first images if pool is small
            mapping[old_url] = available_pool[(i + 7) % len(available_pool)]

    new_content = multiple_replace(content, mapping)
    with open(filepath, 'w') as f:
        f.write(new_content)

files_to_update = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') or file.endswith('.svelte'):
            files_to_update.append(os.path.join(root, file))

for filepath in files_to_update:
    print(f"Refining {filepath}...")
    process_file(filepath)

print("Final Polish Done.")
