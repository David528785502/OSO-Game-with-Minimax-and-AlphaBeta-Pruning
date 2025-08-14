import json, os
from screens.screen_manager import ScreenManager

BASE_DIR = os.path.dirname(__file__)
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        raise FileNotFoundError(f"Not Found: {SETTINGS_PATH}")
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings_data):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings_data, f, indent=4, ensure_ascii=False)

def ensure_max_resolution():
    settings = load_settings()
    
    if "max_scaled_resolution" in settings:
        return

    max_res = ScreenManager.get_display_resolution()
    max_res = [int(round(max_res[0])), int(round(max_res[1]))]

    scaled_res = [int(round(max_res[0] * 0.8)), int(round(max_res[1] * 0.8))]

    settings["max_scaled_resolution"] = scaled_res

    if scaled_res not in settings["resolutions"]:
        settings["resolutions"].append(scaled_res)

    save_settings(settings)

# Getters
def get_current_resolution():
    return load_settings()["current_resolution"]

def get_current_opponent():
    return load_settings()["current_opponent"]

def get_current_language():
    return load_settings()["current_language"]

def get_current_board_size():
    return load_settings()["current_board_size"]

def get_resolutions():
    return load_settings()["resolutions"]

def get_opponents():
    return load_settings()["opponents"]

def get_board_sizes():
    return load_settings()["board_sizes"]

def get_languages():
    return load_settings()["languages"]