# ТУТ РАСПОЛАГАЮТСЯ КЛАССЫ ОПИСАНИЯ ПРЕДМЕТОВ
class Weapon:
    """Класс для описания оружия и его свойств"""
    name: str = 'Кулаки'
    damage_description: str = '1-2'
    damage: tuple = (1, 2)
    weight: int = 0
    is_consumable = False
    is_equipped = False
    is_equipped_description: str = '(Экип.)'

    def __str__(self):
        if self.is_equipped:
            return f'{self.name}  —|—  Урон: {self.damage_description}  —|—  Вес: {self.weight}' \
                   f' {self.is_equipped_description}'
        else:
            return f'{self.name}  —|—  Урон: {self.damage_description}  —|—  Вес: {self.weight}'


class Knife(Weapon):
    name: str = 'Нож'
    damage_description: str = '2–5'
    damage: tuple = (2, 5)
    weight: int = 2
    is_equipped = False


class Sword(Weapon):
    name: str = 'Меч'
    damage_description: str = '5-10'
    damage: tuple = (5, 10)
    weight: int = 5
    is_consumable = False
    is_equipped = False
    is_equipped_description: str = '(Экип.)'


class MagicWeapon(Weapon):
    name: str = 'MagicWeapon'
    damage_description: str = '1-2'
    damage: tuple = (1, 2)
    weight: int = 0
    is_consumable = False
    is_equipped = False
    is_equipped_description: str = '(Экип.)'

    def __str__(self):
        if self.is_equipped:
            return f'{self.name}  —|—  Урон: {self.damage_description} (Маг.)  —|—  Вес: {self.weight}' \
                   f' {self.is_equipped_description}'
        else:
            return f'{self.name}  —|—  Урон: {self.damage_description} (Маг.)  —|—  Вес: {self.weight}'


class CharmedSword(MagicWeapon):
    name: str = 'Зачарованный Меч'
    damage_description: str = '7-10'
    damage: tuple = (7, 10)
    weight: int = 4
    is_consumable = False
    is_equipped = False
    is_equipped_description: str = '(Экип.)'


class MedicalThings:
    """Класс для описания предметов лечения и их свойств"""
    name: str = 'MedicalThings'
    treatment_points: int = 0
    weight: int = 0
    is_consumable = True

    def __str__(self):
        return f'{self.name}  —|—  Восстанавливает: {self.treatment_points}ХП  —|—  Вес: {self.weight}'


class FirstAidKit(MedicalThings):
    name: str = 'Аптечка первой помощи'
    treatment_points: int = 50
    weight: int = 2


class HealingHerbs(MedicalThings):
    name: str = 'Целебные травы'
    treatment_points: int = 15
    weight: int = 1


class Berries(MedicalThings):
    name: str = 'Ягоды'
    treatment_points: int = 10
    weight: int = 1


class Soup(MedicalThings):
    name: str = 'Похлебка'
    treatment_points: int = 10
    weight: int = 1


class Companion:
    name: str = 'Пусто'
    damage: int = (0, 0)
    weight: int = 0
    is_consumable = False
    is_equipped = False
    is_equipped_description: str = '(Экип.)'

    def __str__(self):
        if self.is_equipped:
            return f'Спутник {self.name}  —|—  Вес: {self.weight} {self.is_equipped_description}'
        return f'Спутник {self.name}  —|—  Вес: {self.weight}'


class BlackCat(Companion):
    name: str = 'Черная кошка'
    damage: int = (2, 5)
    weight: int = 2
    is_equipped = False


class SummoningBook:
    name: str = 'Пусто'
    creature_name: str = 'Summon'
    damage: int = (0, 0)
    weight: int = 0
    is_consumable = False
    is_equipped = False
    is_summoned = False
    is_equipped_description: str = '(Экип.)'

    def __str__(self):
        if self.is_equipped:
            return f'Книга Призыва {self.name}  —|—  Вес: {self.weight} {self.is_equipped_description}'
        return f'Книга Призыва {self.name}  —|—  Вес: {self.weight}'


class ShadowWolfBook(SummoningBook):
    name: str = 'Теневой Волк'
    creature_name: str = 'Теневой Волк'
    damage: int = (3, 5)
    weight: int = 1
