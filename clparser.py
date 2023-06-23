import re
from typing import Tuple, List, Optional
from log import logger


class Token:

    def __init__(self, type_: str, value: object):
        self.type = type_
        self.value = value

    def __str__(self):
        if not isinstance(self.value, tuple):
            return f'Token(type: {self.type}, value: {self.value})'
        value = []
        for v in self.value:
            value.append(v.__str__())
        return f'Token(type: {self.type}, value: {tuple(value)})'


class Parser:
    number = re.compile(r'(-?\d+(\.\d+)?)')
    string = re.compile(r'"(\w*)"')
    null = re.compile(r'\s')
    func = re.compile(r'(\w+) (\w+),\s*(.+)')

    def __init__(self, line: str = None):
        self._code = line

    def set_line(self, line: str):
        self._code = line

    def get_token(self, txt: str) -> Optional[Token]:
        t = None
        n = self.number.match(txt)
        #  print(txt, n, n.groups())
        if n:
            return Token("Number", float(n.group(1)))
        n = self.string.match(txt)
        if n:
            return Token("String", n.group(1))

        return t

    def get_tokens(self) -> Tuple[Token]:
        tokens: List[Token] = []
        line = self._code

        while line:
            # print(line)
            n = self.null.match(line)
            if n:
                line = line[len(n.group(0)):]
            func = self.func.match(line)
            if func:
                # print(func.groups(), "g")
                tokens.append(Token("call", (func.group(1), func.group(2), self.get_token(func.group(3)))))
                line = line[len(func.group(0)):]
            else:
                logger.warning(f'have problems in token parser, not detect function, info: '
                               f'{(line, tuple(t.__str__() for t in tokens))}')
                break

        return tuple(tokens)


if __name__ == '__main__':
    pars = Parser('set gravity, 0')
    print(pars.get_tokens()[0].__str__())
    pars = Parser('set gravity, 1.5')
    print(pars.get_tokens()[0].__str__())