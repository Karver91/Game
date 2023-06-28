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

    def print_location_info(self):
        print(f'Вы находитесь в локации {self.name}. '
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


class City(Locations):
    name: str = 'Город'
    description: str = 'Тут кипит шумная жизнь, люди постоянно снуют туда сюда.'
    actions: dict = dict()
    location_monsters: tuple = (monsters.Red, monsters.Bandit)
    items: list = [things.Knife, things.BlackCat, things.ShadowWolfBook]
    rare_items = [things.CharmedSword]
    is_explored = False
    is_open = True


class Tavern(City):
    name: str = 'Таверна'
    description: str = 'Здесь люди могут отдохнуть от странствий'
    actions: dict = dict()
    location_monsters: tuple = tuple()
    items: list = [things.Soup]
    rare_items = list()
    is_explored = False
    is_open = True


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
city = City()
tavern = Tavern()
forest = Forest()

field.add_action('Город', city)
field.add_action('Лес', forest)
city.add_action('Поле', field)
city.add_action('Таверна', tavern)
forest.add_action('Поле', field)

tavern.add_action('Город', city)
tavern.add_action('Усталый путник', characters.weary_traveler)
