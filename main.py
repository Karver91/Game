from random import randint, choice, random
from time import sleep

import locations
import things
import characters
import quests


class Game:
    def __init__(self):
        self.player = Player()
        self.current_location = None
        self.current_location_monster: locations = locations.Monsters

        self.flight_states = ('Вы бежите изо всех сил', 'Быстрее, быстрее!!!', 'Сердце бешено колотится',
                              'Страх и адреналин смешиваются в крови',
                              'Вы спотыкаетесь, но встаете. Надо бежать дальше!',
                              'Спастись, только спастись!', 'Дыхание прерывистое и частое',
                              'Ноги тяжелеют, но надо бежать')

        self.command = {'1': self.search_location,
                        '2': self.player.print_player_info,
                        '3': self.player.use_inventory,
                        '4': self.player.quest_journal.print_journal,
                        '5': self.print_help_info}

        self.battle_command = {'1': self.player_attack,
                               '2': self.player_defend,
                               '3': self.summon_creature,
                               '4': self.escape_attempt}

    def main(self):
        """Стартует игру, отвечает за цикл вывода локаций"""
        self.start_game()
        while True:
            if self.player.current_health > 0:
                self.current_location.print_location_info()
                self.get_player_choice()
            else:
                self.end_game()
                break

    @staticmethod
    def start_game():
        """Выводит предысторию при старте игры"""
        backstory = []
        for row in backstory:
            print(row)
            sleep(1)

    def print_help_info(self):
        """Выводит подсказки на экран"""
        print(f'В поле ввода вы можете ввести название локации, для перехода в нее. Пример: город\n'
              f'Так же вы можете использовать команды для доступа к различным элементам игры:\n'
              f'1 - Исследовать локацию\n'
              f'2 - Для доступа к характеристикам персонажа\n'
              f'3 - Для доступа к инвентарю персонажа\n'
              f'4 - Для доступа к журналу заданий\n'
              f'5 - для доступа к подсказке по управлению')
        self.enter_1_to_continue()

    def search_location(self):
        """Вызывается при обыске локации"""
        if self.current_location.is_explored:
            print('Вы уже обыскивали эту локацию')
            self.enter_1_to_continue()
        else:
            print('Ведется поиск: ')
            for _ in range(3):
                print('...')
                sleep(1)

            self.check_search_event_probability()

    def check_search_event_probability(self):
        """Генерирует событие, которое происходит в ответ на обыск локации"""
        random_digit = random()
        thing = None
        if random_digit <= 0.1:
            if self.current_location.rare_items:
                thing = choice(self.current_location.rare_items)()
        elif 0.1 < random_digit <= 0.4:
            if self.current_location.location_monsters:
                self.get_monster()
                self.battle()
        elif 0.4 < random_digit <= 0.75:
            if self.current_location.items:
                thing = choice(self.current_location.items)()

        if thing:
            self.offer_item_pickup(thing)
        else:
            print('К сожалению, вы ничего не нашли')
            self.enter_1_to_continue()

        self.current_location.is_explored = True

    def offer_item_pickup(self, thing):
        """Предлагает забрать или оставить предмет из локации"""
        print('Вы нашли предмет:')
        while True:
            print(f'{thing}\n'
                  f'1 - Взять /// 2 - Оставить /// 3 - Открыть инвентарь')
            player_choice: str = input()
            if player_choice not in ('1', '2', '3'):
                print('Введена неверная команда попробуйте еще раз')
            elif player_choice == '1':
                if self.player.inventory.add_thing_to_inventory(thing):
                    print(f'Вы забрали {thing.name}')
                    break
            elif player_choice == '2':
                break
            else:
                self.command[player_choice]()

    def get_player_choice(self):
        """Отвечает за выбор действий игрока в меню локации"""
        while True:
            player_choice = input().capitalize()
            if player_choice in self.current_location.actions:
                action_choice = self.current_location.actions[player_choice]
                flag = self.check_action_type(action_choice)
            elif player_choice in self.command:
                self.command[player_choice]()
                break
            else:
                flag = False

            if flag is True:
                self.check_quest_progress(player_choice)
                break
            else:
                print('Введено некорректное имя. Попробуйте еще раз')

    def check_action_type(self, player_choice) -> bool:
        """Проверяет к какому действию относится выбор игрока"""
        flag = False
        if isinstance(player_choice, locations.Locations):
            flag = self.enter_location(player_choice)
        elif isinstance(player_choice, characters.Characters):
            print('...')
            sleep(1)
            player_choice.start_dialog()
            flag = True
        return flag

    def enter_location(self, player_choice) -> bool:
        """Запускает переход в новую локацию, если она открыта"""
        flag = False
        if player_choice.is_open is True:
            self.current_location.is_explored = False
            self.current_location = player_choice
            for i in ['...', 'Вы находитесь в пути', '...']:
                print(i)
                sleep(1)

            self.encounter_monsters()
            flag = True
        return flag

    def encounter_monsters(self):
        """Отвечает за встречу с монстром при переходе между локациями"""
        if self.current_location.location_monsters:
            if randint(1, 1) == 1:
                self.get_monster()
                self.battle()
        else:
            print('Вы безопасно перешли в текущую локацию')

    def get_monster(self):
        self.current_location_monster = choice(self.current_location.location_monsters)()

    def battle(self):
        """Управляет боем игрока с монстром"""
        print(f'Вы встретили противника {self.current_location_monster.name}')

        while True:
            # Ход игрока
            if self.player_turn():
                break

            # Ход монстра
            self.monster_turn()
            if self.player.current_health == 0:
                break

        self.player.book_slot.is_summoned = False
        if self.player.current_health > 0 and self.current_location_monster.health > 0:
            print('Вы успешно сбежали от монстра')
        elif self.player.current_health > 0:
            print(f'Вы победили монстра {self.current_location_monster.name}\n')
            self.player.gain_experience(self.current_location_monster.experience)
            self.check_quest_progress(self.current_location_monster.name)
        else:
            print('Вы были повержены в бою')

    def player_turn(self):
        while True:
            print(f'Ваше здоровье: {self.player.current_health}\n'
                  f'Здоровье противника {self.current_location_monster.health}\n'
                  f'1 - Атаковать\n'
                  f'2 - Обороняться\n'
                  f'3 - Призвать создание\n'
                  f'4 - Попытаться сбежать')

            player_choice = input()
            if player_choice not in self.battle_command:
                print('Введена неверная команда, попробуйте еще раз: ')
                continue
            else:
                print('...')
                sleep(1)
                return self.battle_command[player_choice]()

    def monster_turn(self):
        damage = randint(*self.current_location_monster.damage)
        if self.player.is_defense:
            damage = damage // 2
            self.player.is_defense = False

        self.player.current_health -= damage
        print(f'{self.current_location_monster.name} нанес вам {damage} урона')
        sleep(1)
        print('...')
        sleep(1)
        if self.player.current_health < 0:
            self.player.current_health = 0

    def player_attack(self):
        damage = self.get_player_damage()
        self.current_location_monster.health -= damage
        print(f'Вы нанесли {damage} урона противнику {self.current_location_monster.name}')
        sleep(1)
        if self.is_monster_alive():
            return True
        print(f'Здоровье противника: {self.current_location_monster.health}')
        sleep(1)
        print('...')

        if self.are_creatures_on_battlefield():
            return True

    def get_player_damage(self) -> int:
        damage = randint(*self.player.weapon.damage)
        if isinstance(self.player.weapon, things.MagicWeapon):
            damage = damage + (damage * self.player.magic_power // 2)
        return damage

    def player_defend(self):
        print('Вы ушли в глухую оборону')
        sleep(1)
        print('...')
        self.player.is_defense = True
        sleep(1)
        self.are_creatures_on_battlefield()

    def are_creatures_on_battlefield(self):
        """Проверяет наличие спутника и книги призыва в слотах игрока"""
        if self.player.companion.name != 'Пусто':
            if self.companion_attack():
                return True

        if self.player.book_slot.is_summoned:
            if self.summoned_creature_attack():
                return True

    def companion_attack(self):
        damage = randint(*self.player.companion.damage)
        self.current_location_monster.health -= damage
        print(f'{self.player.companion.name} нанес {damage} урона противнику {self.current_location_monster.name}')
        sleep(1)
        if self.is_monster_alive():
            return True
        print(f'Здоровье противника: {self.current_location_monster.health}')
        sleep(1)
        print('...')

    def summoned_creature_attack(self):
        damage = randint(*self.player.book_slot.damage)
        self.current_location_monster.health -= damage
        print(f'{self.player.book_slot.creature_name} нанес {damage} урона противнику'
              f' {self.current_location_monster.name}')
        sleep(1)
        if self.is_monster_alive():
            return True
        print(f'Здоровье противника: {self.current_location_monster.health}')
        sleep(1)
        print('...')

    def is_monster_alive(self) -> bool:
        """Проверяет текущее хп противника"""
        if self.current_location_monster.health <= 0:
            self.current_location_monster.health = 0
            print(f'Здоровье противника: {self.current_location_monster.health}')
        return self.current_location_monster.health == 0

    def summon_creature(self):
        """Отвечает за вызов существа игроком на поле боя"""
        if self.player.book_slot.name != 'Пусто':
            self.player.book_slot.is_summoned = True
            print(f'{self.player.book_slot.creature_name} успешно призван!')
            sleep(1)
            print('...')
            sleep(1)
            self.are_creatures_on_battlefield()
        else:
            print('Вы не имеете книги призыва')
            sleep(1)
            print('...')

    def escape_attempt(self) -> bool:
        """Отвечает за попытку бегства игроком"""
        print('Вы пытаетесь сбежать от противника:')
        for _ in range(2):
            sleep(1)
            print('...')
            sleep(1)
            print(choice(self.flight_states))
        sleep(1)
        print('...')
        sleep(1)
        if randint(1, 4) == 1:
            return True
        else:
            print('Противник догнал вас\n'
                  'Попытка бегства провалилась\n...')

    def check_quest_progress(self, value):
        """Проверяет выполнение целей в квестах журнала"""
        journal = self.player.quest_journal.quests
        if journal:
            for quest in journal:
                objective = quest.objectives[quest.current_step]
                if objective.target.lower() == value.lower():
                    objective.objective_completed()  # вызываем метод, который ставит текущей задачи True,
                    # Выводит сообщение на экран об успешном прохождении этапа задания.
                    self.enter_1_to_continue()
                    if quest.check_quest_completion():  # Вызывает проверку все ли задачи в квесте True.
                        quest.congratulations()
                        self.player.gain_experience(quest.experience)
                        self.player.quest_journal.remove_quest(quest)
                    else:
                        quest.current_step += 1

    @staticmethod
    def enter_1_to_continue():
        while True:
            if input('...\n1 - Продолжить: ') == '1':
                break
        print('...')

    @staticmethod
    def end_game():
        print('Игра окончена')


class Player:
    """Класс для описания игрока"""
    name: str = 'Player'
    level: int = 1
    current_health: int = 100
    maximum_health: int = 100
    magic_power: int = 1
    weapon: things.Weapon = things.Weapon()
    companion: things.Companion = things.Companion()
    book_slot: things.SummoningBook = things.SummoningBook()
    experience: int = 0
    experience_to_next_level: int = 50
    quest_journal = None
    inventory = None
    is_defense = False

    def __init__(self):
        self.inventory: Inventory = Inventory('Сумка', list(), 10, 0)
        self.inventory_command: dict = {'1': self.use_item, '2': self.inventory.remove_thing_from_inventory}
        self.quest_journal = QuestJournal()

    def print_player_info(self):
        """Выводит статы игрока на экран"""
        print(f'Имя: {self.name}\n'
              f'Уровень: {self.level}\n'
              f'Здоровье: {self.current_health}/{self.maximum_health}\n'
              f'Магическая мощь: {self.magic_power}\n'
              f'Оружие: {self.weapon.name}\n'
              f'Спутник: {self.companion.name}\n'
              f'Книга: {self.book_slot.name}\n'
              f'Опыт: {self.experience}\n'
              f'След. уровень: {self.experience_to_next_level}\n'
              f'Инвентарь: {self.inventory.name}')
        game.enter_1_to_continue()

    def use_inventory(self):
        if self.inventory.things_list:
            self.inventory.print_inventory()
            self.inventory_command_choice()
        else:
            print('...\nИнвентарь пуст')
            game.enter_1_to_continue()

    def inventory_command_choice(self):
        """Проверяет команды управления инвентарем"""
        print('\n1 - Использовать предмет /// 2 - Выкинуть предмет /// 0 - Отмена')
        while True:
            player_choice: str = input()
            if player_choice not in ('1', '2', '0'):
                print('Введена неверная команда попробуйте еще раз')
            elif player_choice == '0':
                break
            else:
                self.inventory_command[player_choice]()
                break

    def use_item(self):
        print('Введите номер предмета, которы хотите использовать или 0 для отмены')
        for index in self.inventory.choice_item_from_inventory():
            thing: object = self.inventory.things_list[index]
            for key in self.inventory.equipment:
                if isinstance(thing, key):
                    self.inventory.equipment[key](self, thing)
                    if thing.is_consumable is True:
                        self.inventory.remove_thing(index)
                        self.inventory.print_inventory()
                    break

    def equip_weapon(self, weapon):
        if weapon.is_equipped:
            print(f'Вы сняли {self.weapon.name}')
            self.weapon.is_equipped = False
            self.weapon = Player.weapon
            self.weapon.is_equipped = True
        else:
            self.weapon.is_equipped = False
            self.weapon = weapon
            self.weapon.is_equipped = True
            print(f'Вы экипировали {self.weapon.name}')

    def equip_companion(self, companion):
        if companion.is_equipped:
            print(f'Вы не используете {self.companion.name}')
            self.companion.is_equipped = False
            self.companion = Player.companion
            self.companion.is_equipped = True
        else:
            self.companion.is_equipped = False
            self.companion = companion
            self.companion.is_equipped = True
            print(f'К вам присоединился {self.companion.name}')

    def equip_summon_book(self, book):
        if book.is_equipped:
            print(f'Вы убрали книгу {self.book_slot.name}')
            self.book_slot.is_equipped = False
            self.book_slot = Player.book_slot
            self.book_slot.is_equipped = True
        else:
            self.book_slot.is_equipped = False
            self.book_slot = book
            self.book_slot.is_equipped = True
            print(f'Вы экипировали книгу {self.book_slot.name}')

    def use_medical(self, thing):
        print('Вы восполнили здоровье\n')
        if self.current_health + thing.treatment_points > self.maximum_health:
            self.current_health = self.maximum_health
        else:
            self.current_health = self.current_health + thing.treatment_points

    def gain_experience(self, experience):
        """Будет вызываться каждый раз при получении опыта игроком"""
        self.experience += experience
        print(f'Опыт: {experience}\n')
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        """Метод повышающий уровень"""
        self.level += 1
        self.maximum_health += 10
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5 + self.experience_to_next_level)
        print('Поздравляю вы получили новый уровень!')
        game.enter_1_to_continue()


class Inventory:
    """Класс для описания инвентаря и взаимодействия с ним"""
    equipment = {things.Weapon: Player.equip_weapon,
                 things.Companion: Player.equip_companion,
                 things.MedicalThings: Player.use_medical,
                 things.SummoningBook: Player.equip_summon_book}

    def __init__(self, name: str, things_list: list, weight_limit: int, current_weight: int):
        self.name = name
        self.things_list = things_list
        self.weight_limit = weight_limit
        self.current_weight = current_weight

    def print_inventory(self):
        print(f'{self.name}\n'
              f'Ваш инвентарь содержит:')
        for index, thing in enumerate(self.things_list, start=1):
            print(f'{index}: {thing}')
        print(f'\nТекущий вес: {self.current_weight}/{self.weight_limit}')

    def add_thing_to_inventory(self, thing) -> bool:
        """Добавляет в инвентарь новый предмет"""
        flag = True
        if self.check_weight_limit(thing):
            self.things_list.append(thing)
            self.current_weight += thing.weight
            self.inventory_sort()
        else:
            print('...\nЭта вещь слишком тяжелая, у вас нет для нее места\n...')
            flag = False
        return flag

    def remove_thing_from_inventory(self):
        """Удаляет предмет из инвентаря"""
        print('Введите номер предмета, который хотите выкинуть или 0 для Отмены')
        for index in self.choice_item_from_inventory():
            thing = self.things_list[index]
            if not thing.is_consumable:
                if thing.is_equipped:
                    print('Экипированный предмет невозможно удалить')
                    continue

            thing = self.remove_thing(index)
            print(f'\nПредмет {thing.name} успешно удален\n')
            if self.things_list:
                self.print_inventory()
                print('Выкинуть еще предмет? 0 - Отмена')

    def choice_item_from_inventory(self):
        while len(self.things_list) > 0:
            index = input()
            if not index.isdigit() or not 0 <= int(index) <= len(self.things_list):
                print('Введено некорректное число')
            elif index == '0':
                break
            else:
                yield int(index) - 1

    def remove_thing(self, index: int):
        thing = self.things_list.pop(index)
        self.current_weight -= thing.weight
        return thing

    def check_weight_limit(self, thing):
        """Проверяет не превышен ли лимит веса"""
        return self.current_weight + thing.weight <= self.weight_limit

    def inventory_sort(self):
        self.things_list.sort(key=lambda x: x.__class__.__name__)


class QuestJournal:
    def __init__(self):
        self.quests = []

    def print_journal(self):
        if self.quests:
            print('...')
            for num, quest in enumerate(self.quests, start=1):
                print(f'{num}: {quest}')

            self.quest_choice()
        else:
            print('...\nВаш журнал пуст')
            game.enter_1_to_continue()

    def quest_choice(self):
        print('...\nВыберете номер квеста 0 - Отмена\n...')
        while True:
            player_choice = input()
            try:
                player_choice = int(player_choice)
                if 0 < player_choice <= len(self.quests):
                    self.quests[player_choice - 1].print_quest_info()
                    game.enter_1_to_continue()
                    break
                elif player_choice == 0:
                    break
                else:
                    raise ValueError

            except ValueError:
                print('...\nВведено некорректное число\n...')

    def add_quest(self, quest):
        self.quests.append(quest)

    def remove_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)


if __name__ == '__main__':
    game = Game()
    print('Добро пожаловать в игру!\n'
          'Элементом управления является набор простейших текстовых команд\n')
    game.print_help_info()
    game.player.name = input('Введите имя своего персонажа: ')
    game.current_location = locations.tavern_dawn_glow
    game.player.quest_journal.add_quest(quests.hello_quest)
    game.main()
