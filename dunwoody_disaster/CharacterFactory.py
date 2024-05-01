from dunwoody_disaster.views.meter import Meter

import dunwoody_disaster as DD
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QLabel
from dunwoody_disaster import Item


class Character:
    def __init__(self):
        # Meta data
        self.level = 0
        self.name = ""
        self.classType = ""
        self.strength = 0
        self.intelligence = 0
        self.image_path = DD.ASSETS["no_texture"]

        # Meteres
        self.curHealth = 0
        self.maxHealth = 0
        self.curMagic = 0
        self.maxMagic = 0
        self.curStamina = 0
        self.maxStamina = 0

        self.inventory_capacity = 100

        self.health_lbl = QLabel(f"Health: {self.curHealth}")
        self.health_lbl.setStyleSheet("color: white; font-size: 24px;")
        self.magic_lbl = QLabel(f"Magic: {self.curMagic}")
        self.magic_lbl.setStyleSheet("color: white; font-size: 24px;")
        self.stamina_lbl = QLabel(f"Stamina: {self.curStamina}")
        self.stamina_lbl.setStyleSheet("color: white; font-size: 24px;")
        self.health_meter = Meter(QColor(255, 0, 0), 100)
        self.magic_meter = Meter(QColor(200, 0, 200), 100)
        self.stamina_meter = Meter(QColor(50, 50, 50), 100)

        # What are these? --Cooper
        self.defense = 0
        self.magicDefense = 0

        # Inventory
        self.loot = []
        self.food = []
        self.weapons = []
        self.defenses = []

    def serialize(self) -> dict:
        return {
            "level": self.level,
            "name": self.name,
            "asset": DD.asset(self.image_path),
            "class": self.classType,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "health": self.maxHealth,
            "magic": self.maxMagic,
            "stamina": self.maxStamina,
            "defense": self.defense,
            "magicDefense": self.magicDefense,
            "inventory": {
                "weapons": [i.to_dict() for i in self.weapons],
                "armor": [i.to_dict() for i in self.defenses],
            },
        }

    def image(self) -> QPixmap:
        return QPixmap(self.image_path)

    def set_health(self, health: int):
        self.curHealth = min(self.maxHealth, max(0, health))
        if self.maxHealth == 0:
            percentage = 0
        else:
            percentage = (health / self.maxHealth) * 100
        self.health_lbl.setText(f"Health: {self.curHealth}")
        self.health_meter.setPercentage(percentage)

    def set_magic(self, magic: int):
        self.curMagic = min(self.maxMagic, max(0, magic))
        if self.maxMagic == 0:
            percentage = 0
        else:
            percentage = (magic / self.maxMagic) * 100
        self.magic_lbl.setText(f"Magic: {self.curMagic}")
        self.magic_meter.setPercentage(percentage)

    def set_stamina(self, stamina: int):
        self.curStamina = min(self.maxStamina, max(0, stamina))
        if self.maxStamina == 0:
            percentage = 0
        else:
            percentage = (stamina / self.maxStamina) * 100
        self.stamina_lbl.setText(f"Stamina: {self.curStamina}")
        self.stamina_meter.setPercentage(percentage)

    def add_item(self, item: Item.Item):
        kind = type(item)
        if kind is Item.Weapon:
            self.weapons.append(item)
        elif kind is Item.Armor:
            self.defenses.append(item)
        else:
            raise ValueError("Unknown item type")

    def get_items(self) -> list[Item.Item]:
        return self.weapons + self.defenses

    def clear_items(self):
        self.weapons = []
        self.defenses = []

    def PlotRisk(self, attacks: list) -> None:
        """
        Goes through enemeis potential attacks and damage according to our defense profile
        Prints how risk each attack could be
        :param attacks: List containing attack data [name, stamina cost, magic damage, health damage]
        """
        risk_levels = {
            "high": "is a high risk attack",
            "medium": "is a medium risk attack",
            "low": "is a low risk attack",
            "none": "is a no risk attack",
        }

        for attack in attacks:
            name, mech, magic, health = attack
            print(f"{name} ", end="")
            if self.curStamina <= mech:
                # attack stuns opponent ?
                print(risk_levels["high"])
                continue

            total_damage = max(0, magic - self.magicDefense) + max(
                0, health - self.defense
            )
            if total_damage >= self.curHealth:
                print(risk_levels["high"])
            elif total_damage > self.curHealth / 2:
                print(risk_levels["medium"])
            elif total_damage > self.curHealth / 4:
                print(risk_levels["low"])
            else:
                print(risk_levels["none"])


class CharacterFactory:
    """
    A class for creating characters
    """

    class_types = {
        "blank": {
            "health": 100,
            "magic": 100,
            "stamina": 100,
            "strength": 10,
            "intelligence": 10,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        }
    }

    @staticmethod
    def createCharacter() -> Character:
        """
        Creates a character based on the given class type
        :param name: The name of the character
        :param classType: The type of the character
        :return: The created character object
        :raises:
            ValueError: If the provided classType is not a member of CharacterFactory.class_types
        """
        
        character = Character()

        # character.name = character.name
        
        # character.maxHealth = character["health"]
        # character.maxMagic = character["magic"]
        # character.maxStamina = character["stamina"]

        # character.strength = character["strength"]
        # character.intelligence = character["intelligence"]

        # character.defense = character["defense"]
        # character.magicDefense = character["magicDefense"]

        # character.level = character["level"]
        # character.loot = character["loot"]
        # character.food = character["food"]

        # character.set_health(character["health"])
        # character.set_magic(character["magic"])
        # character.set_stamina(character["stamina"])

        for weapon in Item.weapons:
            character.add_item(weapon)
        for armor in Item.armors:
            character.add_item(armor)

        return character

    @staticmethod
    def createTestChar() -> Character:
        """
        Creates a default character we can use for testing
        """
        character = CharacterFactory.createCharacter()
        return character

    @staticmethod
    def createFromJson(json: dict) -> Character:
        char = Character()
        char.name = json["name"]
        char.image_path = DD.ASSETS[json["asset"]]
        char.level = json["level"]
        char.classType = json["class"]
        char.strength = json["strength"]
        char.intelligence = json["intelligence"]
        char.maxHealth = json["health"]
        char.maxMagic = json["magic"]
        char.maxStamina = json["stamina"]
        char.defense = json["defense"]
        char.magicDefense = json["magicDefense"]

        char.set_health(json["health"])
        char.set_magic(json["magic"])
        char.set_stamina(json["stamina"])

        for item in json["inventory"]["weapons"]:
            char.add_item(Item.Weapon.from_json(item))
        for item in json["inventory"]["defenses"]:
            char.add_item(Item.Armor.from_json(item))

        return char

    @staticmethod
    def Cooper() -> Character:
        """"""
        char = CharacterFactory.createCharacter()
        char.name = "Cooper"
        char.maxHealth = 100
        char.maxMagic = 100
        char.maxStamina = 100
        char.strength = 1
        char.intelligence = 1
        char.defense = 1
        char.magicDefense = 1

        char.weapons = [Item.weapons]
        char.defenses = [Item.armors]
        char.loot = []
        char.food = []
        return char
    
    @staticmethod
    def John() -> Character:
        """"""
        char = CharacterFactory.createTestChar()
        char.name = "John"
        char.maxHealth = 100
        char.maxMagic = 100
        char.maxStamina = 100
        char.strength = 1
        char.intelligence = 1
        char.defense = 1
        char.magicDefense = 1
        return char
    
    @staticmethod
    def Noah() -> Character:
        """"""
        char = CharacterFactory.createTestChar()
        char.name = "Noah"
        char.maxHealth = 100
        char.maxMagic = 100
        char.maxStamina = 100
        char.strength = 1
        char.intelligence = 1
        char.defense = 1
        char.magicDefense = 1
        return char
    
    @staticmethod
    def Mitch() -> Character:
        """Mitch is more strength and defense oriented. Weak to magic"""
        char = CharacterFactory.createTestChar()
        char.name = "Mitch"
        char.maxHealth = 120
        char.maxMagic = 40
        char.maxStamina = 80
        char.strength = 30
        char.intelligence = 5
        char.defense = 30
        char.magicDefense = 5
        return char
    
    @staticmethod
    def LeAnnSimonson() -> Character:
        """LeAnn is built as a magic character, but weaker than Matthew."""
        char = CharacterFactory.createCharacter()
        char.name = "LeAnn Simonson"
        char.maxHealth = 70
        char.maxMagic = 110
        char.maxStamina = 65
        char.strength = 1
        char.intelligence = 25
        char.defense = 0
        char.magicDefense = 15
        char.level = 1

        char.weapons = []
        char.defenses = []
        char.loot = []
        char.food = []
        return char
    
    @staticmethod
    def AmalanPulendran() -> Character:
        """Amalan is currently an all-around character."""
        char = CharacterFactory.createCharacter()
        char.name = "Amalan Pulendran"
        char.maxHealth = 100
        char.maxMagic = 70
        char.maxStamina = 60
        char.strength = 15
        char.intelligence = 15
        char.defense = 15
        char.magicDefense = 15
        char.level = 2

        char.loot = []
        char.food = []
        return char

    @staticmethod
    def RyanRengo() -> Character:
        """Ryan is a bit of a glass cannon. Strong attacks, but weaker durability.
        I'm not sure if we want to keep it this way due to real-life situations..."""
        char = CharacterFactory.createCharacter()
        char.name = "Ryan Rengo"
        char.maxHealth = 70
        char.maxMagic = 70
        char.maxStamina = 40
        char.strength = 25
        char.intelligence = 25
        char.defense = 5
        char.magicDefense = 5
        char.level = 3

        char.loot = []
        char.food = []
        return char

    @staticmethod
    def NoureenSajid() -> Character:
        """Noureen is currently built as a stronger character, similar to Joe."""
        char = CharacterFactory.createCharacter()
        char.name = "Noureen Sajid"
        char.maxHealth = 110
        char.maxMagic = 50
        char.maxStamina = 65
        char.strength = 15
        char.intelligence = 20
        char.defense = 0
        char.magicDefense = 15
        char.level = 4

        char.loot = []
        char.food = []
        return char

    @staticmethod
    def JoeAxberg() -> Character:
        """Joe is currently built as a strong, brute character."""
        char = CharacterFactory.createCharacter()
        char.name = "Joe Axberg"
        char.maxHealth = 130
        char.maxMagic = 40
        char.maxStamina = 50
        char.strength = 20
        char.intelligence = 5
        char.defense = 15
        char.magicDefense = 0
        char.level = 5

        char.weapons = []
        char.defenses = []
        char.loot = []
        char.food = []
        return char


    @staticmethod
    def MatthewBeckler() -> Character:
        """Matthew is currently the strongest magic caster."""
        char = CharacterFactory.createCharacter()
        char.name = "Matthew Beckler"
        char.maxHealth = 80
        char.maxMagic = 120
        char.maxStamina = 60
        char.strength = 5
        char.intelligence = 30
        char.defense = 0
        char.magicDefense = 20
        char.level = 6

        char.loot = []
        char.food = []
        return char
    
    @staticmethod
    def BillHudson() -> Character:
        """Bill is meant as a stronger version of Amalan. Strongest all-around stats."""
        char = CharacterFactory.createCharacter()
        char.name = "Bill Hudson"
        char.maxHealth = 120
        char.maxMagic = 100
        char.maxStamina = 75
        char.strength = 20
        char.intelligence = 20
        char.defense = 20
        char.magicDefense = 20
        char.level = 7

        char.loot = []
        char.food = []
        return char
