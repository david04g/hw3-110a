import argparse
from scanner import Scanner, tokens
from parser import Parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--symbol_table', '-s', action='store_true')
    parser.add_argument('--scan_only', action='store_true')
    args = parser.parse_args()

    with open(args.file_name, 'r') as f:
        f_contents = f.read()

    s = Scanner(tokens)
    s.input_string(f_contents)

    if args.scan_only:
        while True:
            tok = s.token()
            if tok is None:
                break
            print(tok)
    else:
        p = Parser(s, args.symbol_table)
        p.parse(f_contents)

