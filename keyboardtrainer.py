import os
import sys
from os import system
from random import randint
from pprint import pprint
from time import perf_counter
import logging


def cfg():
    fmt = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename="my_program.log", filemode="w", format=fmt, level=logging.ERROR)


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


class App:
    def __init__(self):
        file_path = resource_path('examples.txt')
        with open(file_path, "r") as example:
            self.text = example.read()
        self.text = self.text.replace("?", "?.").replace("!", "!.").replace("\xa0", "").replace("…", "...").replace("—", '-')
        self.text = self.text.split(".")
        print("Тренажер для печати. Игнорируйте апострофы побокам, ре - для смены предложения.")
        print("")

        self.lst_sym = list()
        self.lst_errors = list()
        self.lst_err_percents = list()
        self.lst_time = list()
        self.lst_speed = list()

    def stats_leave(self):
        if input():
            self.main()
        else:
            print("Любой символ введите!")
            self.stats_leave()

    def stats(self):
        system("cls")
        print('Ваши результаты за сессию, для продолжение тренировки введите любой символ')
        print("")
        print(f"Всего введено символов:    {sum(self.lst_sym)} шт.")
        print(f"Всего ошибок:    {sum(self.lst_errors)} шт.")
        print(f"Общий процент ошибок:    {round(sum(self.lst_err_percents) / len(self.lst_err_percents),3)}%")
        print(f"Времени проведено:    {round(sum(self.lst_time), 3)} сек.")
        print(f"Средняя скорость:    {round(sum(self.lst_speed) / len(self.lst_speed), 3)} сим. в сек. ({round((sum(self.lst_speed) / len(self.lst_speed)), 3)*60} сим. в мин.)")
        self.stats_leave()

    def dec_main(self, func):
        def wrapper():

            func()
            system("cls")
            self.sym = len(self.usr_line)
            self.percent = round(float(self.errors) / float(len(self.line)) * 100)
            self.all_time = round(perf_counter() - self.t_start, 2)
            self.speed = round(len(self.line) / self.all_time)

            self.lst_sym.append(self.sym)
            self.lst_errors.append(self.errors)
            self.lst_err_percents.append(self.percent)
            self.lst_time.append(self.all_time)
            self.lst_speed.append(self.speed)

            print("-"*15)
            print(f"Ошибок:   {self.errors} шт.", f"    {self.percent} %", )
            print(f"Время:    {self.all_time} сек.")
            print(f"Скорость:   {self.speed} Сим. в сек.")
            print("-"*15)

        return wrapper()

    def inputtxt(self):
        self.line = self.text[randint(0, len(self.text)-1)].strip()
        if self.line == '':
            self.main()
        self.errors = 0

        pprint(self.line, width=100)
        print("")

        self.t_start = perf_counter()

        self.usr_line = input().ljust(len(self.line))
        if self.usr_line.strip() == "ре":
            self.main()
        elif self.usr_line.strip() == "рез":
            self.stats()

        for i in range(len(self.line)):
            if self.line[i] == self.usr_line[i]:
                pass
            else:
                if len(self.usr_line) > len(self.line):
                    self.usr_line = f"{self.usr_line[:i]}{self.usr_line[i + 1:]}"
                    i -= 1
                else:
                    self.usr_line = f"{self.usr_line[:i]}{self.line[i]}{self.usr_line[i + 1:]}"
                self.errors += 1

    def main(self):
        while True:
            self.dec_main(self.inputtxt)


if __name__ == '__main__':
    cfg()
    try:
        app = App()
        app.main()
    except Exception:
        logging.exception("ERROR")
