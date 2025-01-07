import sys

from app.patterns.parser import Parser
from app.patterns.scanner import Scanner


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize" or command != "parse":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

        if file_contents:
            if command == "tokenize":
                scanner = Scanner(file_contents)
                for token in scanner.scan_tokens():
                    print(token)
                if scanner.had_error:
                    sys.exit(65)
            else:
                scanner = Scanner(file_contents)
                parser = Parser(scanner.scan_tokens())
                print(parser.parse())
        else:
            print(
                "EOF  null"
            )  # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
