class Monsters:
    name: str = 'Monster'
    health: int = 100
    damage: tuple = (1, 2)
    experience: int = 1


class Red(Monsters):
    name: str = 'Крыса'
    health: int = 10
    damage: tuple = (1, 2)
    experience: int = 10


class Wolf(Monsters):
    name: str = 'Волк'
    health: int = 50
    damage: tuple = (3, 5)
    experience: int = 25


class Bandit(Monsters):
    name: str = 'Бандит'
    health: int = 100
    damage: tuple = (5, 10)
    experience: int = 50


class Bear(Monsters):
    name: str = 'Медведь'
    health: int = 150
    damage: tuple = (10, 20)
    experience: int = 100
