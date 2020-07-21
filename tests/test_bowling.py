#!/usr/bin/env python3

import lesson_014.bowling as bw
from unittest import TestCase


class TestBowlingHomeRule(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rule = bw.HomeRule()
        self.point_processing = bw.GamePointProcessing(rule=self.rule)

    def test_get_score(self):
        """
        Тест функции get_score
        """
        test_result_game = "4/X34-44/X34-44/X"
        correct_test_result = 127
        check_test_result = self.point_processing.get_score(game_result=test_result_game)
        self.assertEqual(check_test_result, correct_test_result, "Не правильно считает очки")

    def test_raise_max_symbols(self):
        """
        Тест на максимально допустимое количество символов в строке.
        В данном случае при игре из 10 фреймов и 2 бросках в каждрм фрейме,
        максимальное количество символов 10*2
        """
        test_result_game = ""
        with self.assertRaises(ValueError):
            self.point_processing.get_score(game_result=test_result_game)

    def test_raise_min_symbols(self):
        """
        Тест на минимально допустимое количество символов в строке.
        В данном случае при игре из 10 фреймов и 2 бросках в каждрм фрейме,
        минималбное количество символов 10
        """
        test_result_game = "XXXXXXX"
        with self.assertRaises(ValueError):
            self.point_processing.get_score(game_result=test_result_game)

    def test_raise_incorrect_symb(self):
        """
        Тест на некорректный символ в строке
        """
        test_result_game = "a4X34-44/X34-44/X"
        with self.assertRaises(ValueError):
            self.point_processing.get_score(game_result=test_result_game)

    def test_raise_num_frames(self):
        """
        Тест на кол-во фреймов в строке
        """
        test_result_game = "XXXXXXXXXXX"
        with self.assertRaises(bw.NumFrameError):
            self.point_processing.get_score(game_result=test_result_game)

    def test_raise_num_score_in_frame(self):
        """
        Тест на максимальное кол-во очков в одном фрейме
        """
        test_result_game = "4/X34-44/X34-44/99"
        with self.assertRaises(bw.NumScoreFrameError):
            self.point_processing.get_score(game_result=test_result_game)


class TestBowlingForeignRule(TestBowlingHomeRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rule = bw.ForeignRule()
        self.point_processing = bw.GamePointProcessing(rule=self.rule)

    def test_get_score(self):
        """
        Тест функции get_score
        """
        test_result_game = "3532X332/3/62--62X"
        correct_test_result = 90
        check_test_result = self.point_processing.get_score(game_result=test_result_game)
        self.assertEqual(check_test_result, correct_test_result, "Не правильно считает очки")




