from threading import Thread
from random import randint
from time import sleep
import queue # класс данных очередь
# Класс Table:
#  Объекты этого класса должны создаваться следующим способом - Table(1)
#  Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

#Класс Guest:
# Должен наследоваться от класса Thread (быть потоком).
# Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
# Обладать атрибутом name - имя гостя.
# Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(a=3, b=10))

# Класс Cafe:
# Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
# Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
# Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).

class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = queue.Queue()

#Метод guest_arrival(self, *guests):
#  Должен принимать неограниченное кол-во гостей (объектов класса Guest).
#  Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest),
#  запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
#  Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue
#  и выводить сообщение "<имя гостя> в очереди".

    def guest_arrival(self, *guests):   # прибытие гостей
        col_tables = len(self.tables) # number of tables in the cafe
        for guest in guests: # iteration by guests
            if col_tables > 0:
                for table in self.tables: # iteration by tables
                    if table.guest is None:
                        table.guest = guest
                        table.guest.start()
                        print(f'{table.guest.name} сел(-а) за стол номер {table.number}')
                        col_tables -= 1
                        break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

        for i in range(len(self.tables)):
            #print(i)
            self.tables[i].guest.join()

#Метод discuss_guests(self): Этот метод имитирует процесс обслуживания гостей.
#    1. Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
#    2. Если за столом есть гость(поток) и гость(поток) закончил приём пищи
#   (поток завершил работу - метод is_alive),
#    то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен".
#    Так же текущий стол освобождается (table.guest = None).
#    3. Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None),
#    то текущему столу присваивается гость взятый из очереди (queue.get()).
#    Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
#    4. Далее запустить поток этого гостя (start)

    def discuss_guests(self): # обслужить гостей
        # проверка на занятость стола
        def table_free(table):
            if table.guest is None:
                return False
            else:
                return True

        while True:
            # пока очередь не пустая (метод empty) или хотя бы один стол занят
            if self.queue.empty() and sum(map(table_free, self.tables)) == 0:
               return
            else:
                for table in self.tables:
                    # Если за столом есть гость(поток) и гость(поток) закончил приём пищи
                    # (поток завершил работу - метод is_alive),
                    if (table.guest is not None) and table.guest.is_alive() == False:
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None
                    #Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None)
                    if (self.queue.empty() == False) and table.guest is None:
                        table.guest = self.queue.get()
                        print(f"{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        table.guest.start()
                        table.guest.join()

# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()
