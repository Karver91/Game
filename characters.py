from time import sleep


class Characters:
    name: str = 'Character'
    dialogs = []

    def start_dialog(self):
        if self.dialogs:
            print(f'{self.name}: Здравствуй')
            sleep(1)
            print('...')
        else:
            print(f'{self.name}: У меня сейчас нет времени для разговоров')
            sleep(1)
            print('...')
            sleep(1)


class WearyTraveler(Characters):
    name: str = 'Усталый путник'
    dialogs = []


weary_traveler = WearyTraveler()
