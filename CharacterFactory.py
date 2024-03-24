import copy

risk_levels = {
    "high": "is a high risk attack",
    "medium": "is a medium risk attack",
    "low": "is a low risk attack",
    "none": "is a no risk attack",
}


class CharacterFactory:
    class_types = {
        "blank": {
            "health": 100,
            "magic": 0,
            "mechanical": 0,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "warrior": {
            "health": 100,
            "magic": 0,
            "mechanical": 15,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "mage": {
            "health": 100,
            "magic": 15,
            "mechanical": 0,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "thief": {
            "health": 100,
            "magic": 0,
            "mechanical": 10,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
    }

    @staticmethod
    def createCharacter(name, classType):
        if classType not in CharacterFactory.class_types:
            raise ValueError("Invalid class type")

        data = CharacterFactory.class_types[classType]
        character = Character()

        character.name = name
        character.classType = classType
        character.health = data["health"]
        character.magic = data["magic"]
        character.mechanical = data["mechanical"]
        character.defense = data["defense"]
        character.magicDefense = data["magicDefense"]
        character.level = data["level"]
        character.loot = data["loot"]
        character.food = data["food"]

        return character


class Character:
    def __init__(self):
        # Meta data
        self.level = 0
        self.name = None
        self.classType = None

        # Meters
        self.health = 0
        self.magic = 0
        self.mechanical = 0
        self.defense = 0
        self.magicDefense = 0

        # Inventory
        self.loot = []
        self.food = []

    def PlotRisk(self, attacks):
        """
        Goes through enemeis potential attacks and damage according to our defense profile
        """
        for attack in attacks:
            name, mech, magic, health = attack
            print(f"{name} ", end="")
            if self.mechanical <= mech:
                # attack stuns opponent ?
                print(risk_levels["high"])
                continue

            total_damage = max(0, magic - self.magicDefense) + max(
                0, health - self.defense
            )
            if total_damage >= self.health:
                print(risk_levels["high"])
            elif total_damage > self.health / 2:
                print(risk_levels["medium"])
            elif total_damage > self.health / 4:
                print(risk_levels["low"])
            else:
                print(risk_levels["none"])
