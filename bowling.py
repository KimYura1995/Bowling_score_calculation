#!/usr/bin/env python3

import re
from abc import ABC, abstractmethod


class NumFrameError(Exception):
    pass


class NumScoreFrameError(Exception):
    pass


class Rule(ABC):

    def __init__(self):
        self.future_characters = None
        self.combinations = {
            re.compile(r'[XХ]'): 1,
            re.compile(r'\-[1-9]'): 2,
            re.compile(r'[1-9]\-'): 2,
            re.compile(r'\-\-'): 2,
            re.compile(r'[1-9]\/'): 2,
            re.compile(r'[1-9][1-9]'): 2,
        }

    def get_max_score_in_frame(self):
        return 10

    def get_max_frame_in_game(self):
        return 10

    def processing(self, frame, future_characters=None):
        self.future_characters = future_characters
        if (frame == "X") or (frame == "Х"):
            return self.get_strike()
        elif frame[-1] == "/":
            return self.get_spare()
        else:
            return self.get_usual(frame)

    def get_usual(self, frame):
        frame_score = 0
        for throw in frame:
            if throw != "-":
                frame_score += int(throw)
        if frame_score < self.get_max_score_in_frame():
            return frame_score
        elif frame_score > self.get_max_score_in_frame():
            raise NumScoreFrameError(f"Превышено значение очков во фрейме - «{frame}»")
        else:
            raise SyntaxError(f"Недопустимая комбинация фрейма - «{frame}»")

    @abstractmethod
    def get_strike(self):
        pass

    @abstractmethod
    def get_spare(self):
        pass


class HomeRule(Rule):
    """
    Правила игры для внутреннего рынка
    """
    def get_strike(self):
        return 20

    def get_spare(self):
        return 15


class ForeignRule(Rule):
    """
    Правила игры для внешнего рынка
    """
    def get_strike(self):
        total_future = 0
        if self.future_characters:
            if self.future_characters[-1] == "/":
                return 20
            else:
                for symb in self.future_characters:
                    total_future += self.processing(frame=symb)
                return 10 + total_future
        else:
            return 10

    def get_spare(self):
        if self.future_characters:
            return 10 + self.processing(frame=self.future_characters[0])
        else:
            return 10


class GamePointProcessing:
    """
    Подсчет кол-ва очков для боулинга
    """

    def __init__(self, rule):
        self.rule = rule
        self.combinations = self.rule.combinations
        self.game_result = None

    def get_frame(self, game_result):
        """
        Генератор фреймов, вывод одного фреймы по очереди
        :param game_result: str результата игры
        :return: str фрейм, str 2 символа после фрейма
        """
        while game_result:
            for combination, max_throw in self.combinations.items():
                frame = combination.search(game_result)
                if frame and frame.span()[0] == 0:
                    break
            else:
                raise SyntaxError(f"Недопустимая комбинация фрейма в строке - «{game_result}»")

            frame = frame[0]
            game_result = game_result[max_throw:]
            future_characters = game_result[:2]
            yield frame, future_characters

    def get_score(self, game_result):
        """
        Подсчет кол-ва очков в игре по полученной строке
        :return; кол-во очков
        """
        self.game_result = str(game_result)
        total_score = 0
        count_frame = 0
        check_result = (True if re.match(r'[-1-9XХ/]{10,20}', self.game_result) else False)
        if check_result:
            frames = self.get_frame(game_result=self.game_result)
            for frame, future_characters in frames:
                count_frame += 1
                total_score += self.rule.processing(frame, future_characters)
            if count_frame == self.rule.get_max_frame_in_game():
                return total_score
            else:
                raise NumFrameError(f"Ошибка в количестве фреймов, кол-во фреймов - {count_frame}")
        else:
            raise ValueError("Недопустимые символы/кол-во символов")


if __name__ == '__main__':
    s = "2/25613542X2/322/--"
    print(12 + 7 + 7 + 8 + 6 + 20 + 13 + 5 + 10)
    rule = ForeignRule()
    point_processing = GamePointProcessing(rule=rule)
    score = point_processing.get_score(game_result=s)
    print(score)
