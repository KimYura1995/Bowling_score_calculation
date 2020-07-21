# -*- coding: utf-8 -*-

import argparse

from bowling import ForeignRule, GamePointProcessing, HomeRule


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Counting points in a bowling game")
    parser.add_argument("--result", dest="game_result", required=True, help="Game result line")
    parser.add_argument("--rule", dest="rule", required=True, help="'HomeRule' or 'ForeignRule'")
    args = parser.parse_args()
    if args.rule == 'HomeRule':
        rule = HomeRule()
    else:
        rule = ForeignRule()
    point_processing = GamePointProcessing(rule=rule)
    score = point_processing.get_score(args.game_result)
    print(f"{args.game_result} - {score}")