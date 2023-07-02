import monsters
import things
import characters


class Locations:
    name: str = 'name'
    description: str = 'description'
    actions: dict = dict()
    location_monsters: tuple = tuple()
    items: list = list()
    rare_items = list()
    is_explored = False
    is_open = True

    def __str__(self):
        return f'{self.name}'

    def print_location_info(self):
        print(f'Вы находитесь в локации {self}. '
              f'{self.description}\n'
              f'Далее вы можете:')
        print('------------------------------------------------------')
        for action, value in self.actions.items():
            if isinstance(value, Locations):
                if value.is_open:
                    print(f'+ Перейти в {action}')
            else:
                print(f'+ Поговорить с {action}')
        print('------------------------------------------------------')
        print(f'Введите название места куда бы вы хотели отправиться или имя персонажа для разговора')

    def add_action(self, action, reference):
        self.actions[action] = reference

    def add_items(self, items):
        for item in items:
            self.items.append(item)


class TumanskCity(Locations):
    name: str = 'Туманск'
    description: str = 'Расположенный в низине портовый город, куда стекаются торговцы, чтобы выгодно ' \
                       'продать свои товары заморским купцам.'
    actions: dict = dict()
    location_monsters: tuple = (monsters.Red, monsters.Bandit)
    items: list = [things.Knife, things.BlackCat, things.ShadowWolfBook]
    rare_items = [things.CharmedSword]
    is_explored = False
    is_open = True


class TavernDawnGlow(Locations):
    name: str = 'Зарево Рассвета'
    description: str = 'Здание из старого кирпича, со спальнями на втором этаже, которые располагаются над уютным' \
                       ' залом с камином. В зале царят приглушенные разговоры.'
    actions: dict = dict()
    location_monsters: tuple = tuple()
    items: list = [things.Soup]
    rare_items = list()
    is_explored = False
    is_open = True

    def __str__(self):
        return f'таверна {self.name}'


class Forest(Locations):
    name: str = 'Лес'
    description: str = 'Кроны деревьев скрывают свет. В этом полумраке живут различные создания.'
    actions: dict = dict()
    location_monsters: tuple = (monsters.Wolf, monsters.Bear)
    items: list = [things.Knife, things.Berries]
    rare_items = list()
    is_explored = False
    is_open = True


class Field(Locations):
    name: str = 'Поле'
    description: str = 'Его просторы поражают.'
    actions: dict = dict()
    location_monsters: tuple = (monsters.Red,)
    items: list = [things.HealingHerbs, things.Berries]
    rare_items = list()
    is_explored = False
    is_open = True


field = Field()
city_tumansk = TumanskCity()
tavern_dawn_glow = TavernDawnGlow()
forest = Forest()

field.add_action(f'{city_tumansk.name}', city_tumansk)
field.add_action('Лес', forest)
city_tumansk.add_action('Поле', field)
city_tumansk.add_action(f'{tavern_dawn_glow.name}', tavern_dawn_glow)
forest.add_action('Поле', field)

tavern_dawn_glow.add_action(f'{city_tumansk.name}', city_tumansk)
tavern_dawn_glow.add_action('Усталый путник', characters.weary_traveler)
