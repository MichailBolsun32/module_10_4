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
                        table.guest = guest.name
                        guest.start()
                        #guest.join()
                        print(f'{guest.name} сел(-а) за стол номер {table.number}')
                        col_tables -= 1
                        break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

        for i in range(len(self.tables)):
            guests[i].join()

#Метод discuss_guests(self): Этот метод имитирует процесс обслуживания гостей.
#    Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
#    Если за столом есть гость(поток) и гость(поток) закончил приём пищи
#   (поток завершил работу - метод is_alive),
#    то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен".
#    Так же текущий стол освобождается (table.guest = None).
#    Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None),
#    то текущему столу присваивается гость взятый из очереди (queue.get()).
#    Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
#    Далее запустить поток этого гостя (start)

    def discuss_guests(self): # обслужить гостей
        pass

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

#Примечания:
    # Для проверки значения на None используйте оператор is (table.guest is None).
    # Для добавления в очередь используйте метод put, для взятия - get.
    # Для проверки пустоты очереди используйте метод empty.
    # Для проверки выполнения потока в текущий момент используйте метод is_alive.