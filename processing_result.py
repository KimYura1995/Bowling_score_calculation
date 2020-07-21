#!/usr/bin/env python3

from collections import defaultdict
from bowling import ForeignRule, GamePointProcessing, HomeRule


class ResultProcessing:
    """"
    Обработка файла с результатами игры в боулинг
    """
    def __init__(self, input_file_name, rule, output_file_name=None):
        self.num_matches_played = defaultdict(int)
        self.num_mathces_won = defaultdict(int)
        self.input_file_name = input_file_name
        self.output_name_file = (output_file_name if output_file_name else "tournament_result.txt")
        self.name_winner = None
        self.winner_score = 0
        if rule == "HomeRule":
            self.current_rule = HomeRule()
        else:
            self.current_rule = ForeignRule()
        self.point_processing = GamePointProcessing(rule=self.current_rule)


    def processing_result(self, line):
        """
        Обработка строки
        :param line: входная строка из файла
        :return: обработанная строка для записи в файл
        """
        if ("Tour" in line) or (line == "\n"):
            self.name_winner = None
            self.winner_score = 0
            return line
        elif "winner" in line:
            self.num_mathces_won[self.name_winner] += 1
            return f"winner is {self.name_winner}\n"
        else:
            current_name, game_result = line.split()
            try:
                current_score = self.point_processing.get_score(game_result=game_result)
                if current_score > self.winner_score:
                    self.name_winner = current_name
                    self.winner_score = current_score
                    self.num_matches_played[current_name] += 1
                return f"{current_name}\t{game_result:<24} {current_score}\n"
            except Exception as err:
                self.num_matches_played[current_name] += 1
                return f"{current_name}\t{game_result:<24} {err}\n"

    def open_files(self):
        """
        Открытие файлов. чтение и запись
        :return: None
        """
        with open(self.input_file_name, mode="r", encoding="UTF-8") as input_file, \
                open(self.output_name_file, mode="a", encoding="UTF-8") as output_file:
            for line in input_file.readlines():
                processed_line = self.processing_result(line=line)
                output_file.write(processed_line)

    def print_console(self):
        """
        Вывод на консоль обработанных результатов
        :return: None
        """
        sorted_list = sorted(self.num_matches_played.items(), key=lambda x: x[1], reverse=True)
        print(f"+{'-' * 10}+{'-' * 18}+{'-' * 14}+")
        print(f"|{'Игрок':^10}|{'сыграно матчей':^18}|{'всего побед':^14}|")
        print(f"+{'-' * 10}+{'-' * 18}+{'-' * 14}+")
        for name, all_games in sorted_list:
            won_games = str(self.num_mathces_won[name])
            print(f"|{name:^10}|{all_games:^18}|{won_games:^14}|")
        print(f"+{'-' * 10}+{'-' * 18}+{'-' * 14}+")


if __name__ == '__main__':
    processed = ResultProcessing("tournament.txt", "ForeignRule")
    processed.open_files()
    processed.print_console()



