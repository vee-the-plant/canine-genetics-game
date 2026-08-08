import random
from pyscript import document

# --- DATA POOLS ---
NAME_POOL = [
    "Atlas", "Cleo", "Orion", "Zelda", "Blaze", "Echo", "Zeus", "Athena", 
    "Kona", "Milo", "Scout", "Shadow", "Copper", "Duchess", "Rex", "Luna"
]

BREEDS = {
    "Chihuahua": {"group": "Toy"},
    "Golden Retriever": {"group": "Sporting"},
    "German Shepherd": {"group": "Herding"},
    "Cwn Annwn (Mythic)": {"group": "Mythic"},
    "Kitsune Spirit Fox-Dog": {"group": "Mythic"}
}

# Game State
game_state = {
    "money": 1200,
    "day": 1,
    "actions": 3,
    "kennel": {}
}

def get_unique_name():
    if NAME_POOL:
        return NAME_POOL.pop(0)
    return f"Dog_{random.randint(100, 999)}"

def create_dog(name, sex, breed):
    return {
        "name": name, "sex": sex, "breed": breed,
        "age": random.randint(1, 3), "health": 100,
        "fertility": random.randint(60, 95),
        "stats": {"Agility": random.randint(8, 15), "Strength": random.randint(8, 15), "Perception": random.randint(8, 15)}
    }

# Initialize starting dogs
starter_m = create_dog(get_unique_name(), "Male", random.choice(list(BREEDS.keys())))
starter_f = create_dog(get_unique_name(), "Female", random.choice(list(BREEDS.keys())))
game_state["kennel"][starter_m["name"]] = starter_m
game_state["kennel"][starter_f["name"]] = starter_f

def render_ui(text, buttons_dict):
    output_div = document.querySelector("#output")
    controls_div = document.querySelector("#controls")
    
    header = f"=== DAY {game_state['day']} ===\nBank Vault: ${game_state['money']} | Actions Left: {game_state['actions']}/3\n\n"
    output_div.innerHTML = f"<pre>{header}{text}</pre>"
    
    controls_div.innerHTML = ""
    for label, callback in buttons_dict.items():
        btn = document.createElement("button")
        btn.innerText = label
        btn.onclick = callback
        controls_div.appendChild(btn)

def show_main_menu(e=None):
    text = "Choose an action for your kennel:"
    buttons = {
        "View Kennel": view_kennel,
        "Train Dog (-1 Action)": train_menu,
        "Explore Zones (-1 Action)": explore_zone,
        "End Day": end_day
    }
    render_ui(text, buttons)

def view_kennel(e):
    if not game_state["kennel"]:
        text = "Your kennel is empty."
    else:
        text = "🐾 KENNEL REGISTRY:\n"
        for dog in game_state["kennel"].values():
            text += f"\n• {dog['name']} ({dog['sex']} - {dog['breed']})\n  Age: {dog['age']} | Health: {dog['health']}% | Fertility: {dog['fertility']}%\n  Stats -> Agility: {dog['stats']['Agility']} | Strength: {dog['stats']['Strength']} | Perception: {dog['stats']['Perception']}\n"
    render_ui(text, {"Back to Menu": show_main_menu})

def train_menu(e):
    if game_state["actions"] <= 0:
        render_ui("⚠️ You have no actions left today! End the day to reset.", {"Back to Menu": show_main_menu})
        return
    
    buttons = {}
    for name in game_state["kennel"].keys():
        buttons[f"Train {name}"] = lambda event, n=name: perform_training(n)
    buttons["Back to Menu"] = show_main_menu
    render_ui("Select a dog to train (+3 Agility):", buttons)

def perform_training(dog_name):
    if game_state["actions"] > 0:
        game_state["actions"] -= 1
        game_state["kennel"][dog_name]["stats"]["Agility"] += 3
        render_ui(f"✅ Training successful! {dog_name} gained +3 Agility.", {"Back to Menu": show_main_menu})
    else:
        render_ui("⚠️ No actions left!", {"Back to Menu": show_main_menu})

def explore_zone(e):
    if game_state["actions"] <= 0:
        render_ui("⚠️ No actions left today!", {"Back to Menu": show_main_menu})
        return
    
    game_state["actions"] -= 1
    new_dog = create_dog(get_unique_name(), random.choice(["Male", "Female"]), random.choice(list(BREEDS.keys())))
    game_state["kennel"][new_dog["name"]] = new_dog
    render_ui(f"🎉 Expedition successful! Rescued a wild {new_dog['breed']} named {new_dog['name']}!", {"Back to Menu": show_main_menu})

def end_day(e):
    game_state["day"] += 1
    game_state["actions"] = 3
    render_ui(f"🌙 Advanced to Day {game_state['day']}. Actions refreshed!", {"Back to Menu": show_main_menu})

# Launch initial view
show_main_menu()
