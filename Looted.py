import os
import re
import time
import requests
from random import choice
import json
from code_map import data, create_code_mapping, notfound_map, notfound, regular_colors
from datetime import datetime

code_mapping = create_code_mapping(data)
discColor = ['1752220', '1146986', '3066993', '2067276', '3447003', '2123412', '10181046', '7419530', '15277667', '11342935', '15844367', '12745742', '15105570', '11027200', '15158332', '10038562', '9807270', '9936031', '8359053', '12370112', '3426654', '2899536', '16776960']
script_dir = os.path.dirname(os.path.realpath(__file__))
assets_dir = os.path.join(script_dir, "assets")
config_file_path = 'config.json'
def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print("The config file was not found.")
        return None
    except json.JSONDecodeError:
        print("There was an error decoding the config file.")
        return None

config = load_config(config_file_path)
if config:
    discord_webhook = config['discord_webhook']
    root_path = config['root_path'] 
    rune_color = config['rune_color']
    runeword_color = config['runeword_color']
    unique_color = config['unique_color']
    sleep_seconds = config['sleep_seconds']
    clear_logs = config['clear_logs']
    loot_path = os.path.join(root_path, 'Looted')
    logs_path = os.path.join(root_path, 'Logs')
    print(f"Discord Webhook URL: {discord_webhook}")
    print(f"Root Path: {root_path}")

    if clear_logs:
        if os.path.exists(loot_path):
            # Iterate through files in the Looted path and remove them
            for filename in os.listdir(loot_path):
                file_path = os.path.join(loot_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")
        else:
            print(f"Looted path {loot_path} does not exist.")
        if os.path.exists(logs_path):
            # Iterate through files in the Logs path and remove them
            for filename in os.listdir(logs_path):
                file_path = os.path.join(logs_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")
        else:
            print(f"Logs path {logs_path} does not exist.")
else:
    print("Failed to load config.")

def get_itemcount(path):
    try:
        with open(path, 'r', encoding='oem') as file:
            content = file.read()
        matches = re.findall(r'(?m)(?<=^)([\s\S]+?)(?=[0-9- :]{20}|\Z)', content)
        return len(matches)
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return 0

def get_regexitem(path, index, name):
    try:
        with open(path, 'r', encoding='oem') as file:
            content = file.read()
        matches = re.findall(r'(?m)(?<=^)([\s\S]+?)(?=[0-9- :]{20}|\Z)', content)
        if index < len(matches):
            buffer = matches[index].split('\n')
            return {
                'foundby': name,
                'Timestamp': buffer[0].strip().rstrip('.'),
                'Name': buffer[1].strip(),
                'Type': buffer[2].strip(),
                'Stats': '\n'.join(buffer[3:])
            }
        return None
    except Exception as e:
        print(f"Error processing file {path}: {e}")
        return None

def monitor_folder(root_path):
    print("Searching for Looted.log files")
    log_files = []
    for subdir, dirs, files in os.walk(root_path):
        for file in files:
            if file == 'Looted.log':
                log_files.append(os.path.join(subdir, file))
    print(f"Found {len(log_files)} files.")
    file_sizes = {log_file: os.path.getsize(log_file) for log_file in log_files}
    item_counts = {log_file: get_itemcount(log_file) for log_file in log_files}
    while True:
        time.sleep(sleep_seconds)
        for log_file in log_files:
            new_size = os.path.getsize(log_file)
            if new_size != file_sizes[log_file]:
                new_item_count = get_itemcount(log_file)
                if new_item_count > item_counts[log_file]:
                    subfolder_name = os.path.basename(os.path.dirname(log_file))
                    print(f"New item detected for {subfolder_name}.")
                    item = get_regexitem(log_file, new_item_count - 1, subfolder_name)
                    if item:
                        print(f"Finding image for: {item['Name']} from {subfolder_name}")
                        find_images(item, assets_dir)
                file_sizes[log_file] = new_size
                item_counts[log_file] = new_item_count

def extract_base_item_type(full_item_name):
    parts = full_item_name.lower().split()
    full_item_name_lower = ' '.join(parts)
    base_item_types = [item[1].lower() for item in notfound]
    for base_type in base_item_types:
        if base_type in full_item_name_lower:
            return base_type
    return None

def find_images(item, assets_dir):
    code = None
    image_found = False
    colortype = int(choice(discColor))
    runeword_found = False
    def search_for_item_by_type(item_type, assets_directory):
        print(f"Searching for  {item_type}")
        for file_name in os.listdir(assets_directory):
            if file_name.endswith(".json"):
                json_file_path = os.path.join(assets_directory, file_name)
                try:
                    with open(json_file_path, 'r') as file:
                        data = json.load(file)
                        for item_data in data.values():
                            if 'type' in item_data and item_data['name'].lower() == item_type.lower():
                                return item_data.get('code')
                except Exception as e:
                    print(f"Error processing {json_file_path}: {e}")
        return None

    for file_name in os.listdir(assets_dir):
        if file_name.endswith(".json"):
            json_file_path = os.path.join(assets_dir, file_name)
            try:
                with open(json_file_path, 'r') as file:
                    uniques_data = json.load(file)
                    for item_data in uniques_data.values():
                        if item_data.get('name', '').lower() == item['Name'].lower():
                            code = item_data.get('code')
                            image_found = True
                            if code.startswith('Runeword'):
                                runeword_found = True
                                for color_code, color_name in regular_colors.items():
                                    if color_name == runeword_color:
                                        colortype = color_code
                                        break
                            break
            except Exception as e:
                print(f"Error processing {json_file_path}: {e}")
    if runeword_found:
        runeword_code = search_for_item_by_type(item['Type'], assets_dir)
        if runeword_code:
            code = runeword_code
        else:
            print("No valid code found for Runeword by type. Lets try checking the upgraded bases map.")
            if code in code_mapping:
                code = code_mapping[code]
                print(f"Mapped code: {code}")
                image_found = True
            else:
                print("Code not found in the mapping.")
            return
    elif not code:
        type_code = search_for_item_by_type(item['Type'], assets_dir)
        if type_code:
            code = type_code
        else:
            item_name = item['Name'] 
            base_item_type = extract_base_item_type(item_name)  # extract the base item type

            if base_item_type:
                code = notfound_map.get(base_item_type)
                if code:
                    print(f"Code found in notfound map for base item type {base_item_type}: {code}")
                else:
                    print(f"No valid code found for the base item type {base_item_type}.")
            else:
                print("No base item type extracted from item name.")
    if image_found and code:
        action = "sending to Discord"
        print(f"Image found, {action}: {code}")
    else:
        print("No matching item found or code not provided try mapping?")
    post_disc(item, code, colortype)

def post_disc(item, code, colortype):
    webHookUrl = discord_webhook
    img_url = f"https://raw.githubusercontent.com/blizzhackers/ItemScreenshot/master/assets/gfx/{code}/0.png"
    response = requests.head(img_url)
    if response.status_code == 200:
        print(f"Image found on GitHub for code: {code}")
    else:
        print(f"Image not found on GitHub for code: {code}. Trying mapping...")
        if code in code_mapping:
            code = code_mapping[code]  # Update code if mapping found
            img_url = f"https://raw.githubusercontent.com/blizzhackers/ItemScreenshot/master/assets/gfx/{code}/0.png"
            print(f"New code after mapping: {code}")
        else:
            print("Code not found in the mapping.")
    timestamp_str = item['Timestamp'].strip(':')  # Remove the trailing colon if present
    format_str = "%d-%m-%Y %H:%M:%S"
    timestamp_dt = datetime.strptime(timestamp_str, format_str)
    timestamp_12hr = timestamp_dt.strftime("%I:%M:%S %p")  # e.g., "11:22:28 PM"
    embedObject = {
        "color": colortype,
        "title": item['Name'],
        "description": f"{item['Type']}\n\n{item['Stats']}\n*Found by: {item['foundby']}\nTimestamp: {timestamp_12hr}*",
        "thumbnail": {"url": img_url}  # Use thumbnail for image on the right
    }
    payload = {"embeds": [embedObject]}
    response = requests.post(webHookUrl, json=payload, headers={"Content-Type": "application/json"})
    if response.status_code != 204:
        print(f"Error posting to Discord: {response.status_code}, {response.text}")


monitor_folder(loot_path)