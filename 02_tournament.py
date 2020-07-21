# -*- coding: utf-8 -*-

# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

import argparse

from processing_result import ResultProcessing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Outputting the results of a bowling game to a file and to the console"
    )
    parser.add_argument("--input", dest="input_file_name", required=True, help="Path and input file name")
    parser.add_argument("--output", dest="output_file_name", help="Path and output file name")
    parser.add_argument("--rule", dest="rule", required=True, help="'HomeRule' or 'ForeignRule'")
    args = parser.parse_args()
    processing = ResultProcessing(args.input_file_name, args.rule, args.output_file_name)
    processing.open_files()
    processing.print_console()