import random

# --- NAME POOL & DATA ---
NAME_POOL = [
    "Atlas", "Cleo", "Orion", "Zelda", "Blaze", "Echo", "Zeus", "Athena", 
    "Kona", "Milo", "Scout", "Shadow", "Copper", "Duchess", "Rex", "Luna", 
    "Bandit", "Nova", "Ghost", "Titan", "Freya", "Fenrir", "Apollo", "Ruby", 
    "Socks", "Jasper", "Sage", "Diesel", "Hazel", "Cobra", "Bane", "Pixel"
]

BREEDS = {
    "Chihuahua": {"group": "Toy", "min": 1, "max": 3},
    "Golden Retriever": {"group": "Sporting", "min": 6, "max": 10},
    "German Shepherd": {"group": "Herding", "min": 5, "max": 9},
    "Cwn Annwn (Mythic)": {"group": "Mythic", "min": 2, "max": 5},
    "Kitsune Spirit Fox-Dog": {"group": "Mythic", "min": 1, "max": 4}
}

class Dog:
    def __init__(self, name, sex, breed):
        self.name = name
        self.sex = sex
        self.breed = breed if breed in BREEDS else "Mutt"
        self.age = random.randint(1, 3)
        self.health = 100
        self.fertility = random.randint(60, 95)
        self.affection = random.randint(30, 70)
        self.is_in_heat = True if sex == "Female" else False
        self.is_pregnant = False
        self.pregnancy_days = 0
        self.stats = {
            "Agility": random.randint(8, 15),
            "Strength": random.randint(8, 15),
            "Perception": random.randint(8, 15)
        }

    def display_info(self):
        print(f"\n--- {self.name} ({self.sex} - {self.breed}) ---")
        print(f"Age: {self.age} | Health: {self.health}% | Fertility: {self.fertility}%")
        print(f"Stats -> Agility: {self.stats['Agility']} | Strength: {self.stats['Strength']} | Perception: {self.stats['Perception']}")
        if self.sex == "Female":
            print(f"In Heat: {'Yes 🔥' if self.is_in_heat else 'No'}")
            if self.is_pregnant:
                print(f"Status: Pregnant ({self.pregnancy_days} days left)")

def get_unique_name():
    if NAME_POOL:
        return NAME_POOL.pop(0)
    return f"Dog_{random.randint(100, 999)}"

def main():
    print("🐾 Welcome to Canine Genetics & Mythic Lineage Tracker 🐾")
    
    money = 1200
    day = 1
    actions = 3
    kennel = {}

    # Initialize a couple of starting dogs
    starter_male = Dog(get_unique_name(), "Male", random.choice(list(BREEDS.keys())))
    starter_female = Dog(get_unique_name(), "Female", random.choice(list(BREEDS.keys())))
    kennel[starter_male.name] = starter_male
    kennel[starter_female.name] = starter_female

    while True:
        print(f"\n================ DAY {day} ================")
        print(f"Bank Vault: ${money} | Actions Left: {actions}/3")
        print("1. View Kennel Registry")
        print("2. Train a Dog")
        print("3. Breeding Center")
        print("4. Explore Zones")
        print("5. End Day / Pass Time")
        print("6. Quit Game")
        
        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            if not kennel:
                print("Your kennel is empty.")
            for dog in kennel.values():
                dog.display_info()

        elif choice == "2":
            if actions <= 0:
                print("⚠️ You have no actions left today! End the day to reset.")
                continue
            
            adults = list(kennel.keys())
            print("\nAvailable Dogs to Train:")
            for idx, name in enumerate(adults, 1):
                print(f"{idx}. {name}")
            
            try:
                sel = int(input("Choose dog number: ")) - 1
                dog_name = adults[sel]
                dog = kennel[dog_name]
                
                stat_choice = input("Train which stat? (Agility / Strength / Perception): ").capitalize()
                if stat_choice in dog.stats:
                    dog.stats[stat_choice] += 3
                    actions -= 1
                    print(f"✅ Training successful! {dog.name} gained +3 {stat_choice}.")
                else:
                    print("❌ Invalid stat choice.")
            except (ValueError, IndexError):
                print("❌ Invalid selection.")

        elif choice == "3":
            females = [name for name, d in kennel.items() if d.sex == "Female" and not d.is_pregnant and d.is_in_heat]
            males = [name for name, d in kennel.items() if d.sex == "Male"]

            if not females or not males:
                print("⚠️ You need at least one active Male and one Female in Heat to breed.")
                continue

            print("\nAvailable Females in Heat:")
            for idx, f in enumerate(females, 1): print(f"{idx}. {f}")
            f_sel = int(input("Select Mother number: ")) - 1

            print("\nAvailable Males:")
            for idx, m in enumerate(males, 1): print(f"{idx}. {m}")
            m_sel = int(input("Select Father number: ")) - 1

            mom = kennel[females[f_sel]]
            mom.is_pregnant = True
            mom.pregnancy_days = 2
            mom.is_in_heat = False
            print(f"❤️ Success! {mom.name} is now pregnant. Litter expected in 2 days.")

        elif choice == "4":
            if actions <= 0:
                print("⚠️ You have no actions left today!")
                continue
            
            print("\nExpedition Zones: 1. Scottish Highlands | 2. Mythic Forest")
            zone_choice = input("Choose zone (1 or 2): ").strip()
            if zone_choice in ["1", "2"]:
                actions -= 1
                new_dog = Dog(get_unique_name(), random.choice(["Male", "Female"]), random.choice(list(BREEDS.keys())))
                kennel[new_dog.name] = new_dog
                print(f"🎉 Expedition successful! Rescued a wild {new_dog.breed} named {new_dog.name}!")

        elif choice == "5":
            day += 1
            actions = 3
            print(f"\n🌙 Advancing to Day {day}...")
            for dog in kennel.values():
                if dog.sex == "Female":
                    dog.is_in_heat = not dog.is_in_heat # Toggle heat cycle
                    if dog.is_pregnant:
                        dog.pregnancy_days -= 1
                        if dog.pregnancy_days <= 0:
                            pup = Dog(get_unique_name(), random.choice(["Male", "Female"]), dog.breed)
                            kennel[pup.name] = pup
                            dog.is_pregnant = False
                            print(f"🐶 A new puppy was born in your kennel: {pup.name}!")

        elif choice == "6":
            print("Thanks for playing!")
            break
        else:
            print("❌ Invalid command, please select a number from 1 to 6.")

if __name__ == "__main__":
    main()
