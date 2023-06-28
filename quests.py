class Quest:
    name: str = 'Quest'
    steps_description: dict = {}
    current_step = 1
    objectives = {}
    experience: int = 10
    completed: bool = False

    def __str__(self):
        return self.name

    def print_quest_info(self):
        print(f'{self.name}\n...\nОписание: ', end='')
        for i in range(self.current_step):
            if self.steps_description[i + 1]:
                print(self.steps_description[i + 1], '\n')
        print(f'Цель: {self.objectives[self.current_step]}')

    def check_quest_completion(self):
        counter = 0
        for objective in self.objectives.values():
            if objective.completed:
                counter += 1

        return counter == len(self.objectives)

    def congratulations(self):
        print(f'Поздравляю! Квест {self} успешно завершен!')


class Objective:
    def __init__(self, description, target):
        self.target = target
        self.description: str = description
        self.completed = False

    def __str__(self):
        return self.description

    def objective_completed(self):
        self.completed = True
        print(f'Задача выполнена: '
              f'{self}')


class HelloQuestObjective(Objective):
    def __init__(self, description, target, counter):
        super().__init__(description, target)
        self.counter = counter

    def __str__(self):
        if self.completed:
            self.counter += 1
        return f'{self.description}: {self.counter}/2'


class HelloQuest(Quest):
    name: str = 'Уничтожение вредителей'
    steps_description: dict = {1: 'Уничтожить 2 крысы',
                               2: '',
                               3: 'Я выполнил задачу, теперь мне нужно поговорить с Усталым Путником. '
                                  'Он находится таверне "Коготь ворожеи"'}
    current_step = 1
    objectives = {1: HelloQuestObjective(f'Уничтожить крыс', 'Крыса', 0),
                  2: HelloQuestObjective('Уничтожить крыс', 'Крыса', 1),
                  3: Objective('Поговорить с Усталый путник', 'Усталый Путник')}
    experience: int = 50
    completed: bool = False


hello_quest = HelloQuest()
