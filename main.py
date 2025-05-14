import argparse
from scanner import Scanner,tokens
from parser import Parser

if __name__ == "__main__":

    # this is the command line parser, not the C-simple parser
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--symbol_table', '-s', action='store_true')
    args = parser.parse_args()

    with open(args.file_name) as f:
        source_code = f.read()

    s = Scanner(tokens)
    s.input_string(source_code)

    p = Parser(s, args.symbol_table)
    try:
        p.parse(source_code)
    except Exception as e:
        print(e)
