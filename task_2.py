"""
Простий інтерпретатор арифметичних виразів.

Цей модуль реалізує інтерпретатор, який може обчислювати прості арифметичні вирази,
що містять цілі числа, операції додавання, віднімання, множення, ділення та дужки.
"""


class LexicalError(Exception):
    """Виняток при помилках лексичного аналізу."""


class ParsingError(Exception):
    """Виняток при помилках синтаксичного аналізу."""


class TokenType:
    """
    Клас, що визначає типи токенів для лексичного аналізу.

    Атрибути:
        INTEGER: Цілі числа
        PLUS: Оператор додавання
        MINUS: Оператор віднімання
        MUL: Оператор множення
        DIV: Оператор ділення
        LPAREN: Ліва дужка
        RPAREN: Права дужка
        EOF: Кінець вхідного рядка
    """
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"  # Означає кінець вхідного рядка


class Token:
    """
    Клас для представлення токенів.

    Атрибути:
        type: Тип токена
        value: Значення токена
    """
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self):
        return f"Token({self.token_type}, {repr(self.token_value)})"


class Lexer:
    """
    Лексичний аналізатор.
    
    Розбиває вхідний текст на послідовність токенів.
    
    Атрибути:
        text: Вхідний текст для аналізу
        pos: Поточна позиція у тексті
        current_char: Поточний символ
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None

    def advance(self):
        """Переміщуємо 'вказівник' на наступний символ вхідного рядка"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Означає кінець введення
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Пропускаємо пробільні символи."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Повертаємо ціле число, зібране з послідовності цифр."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """
        Отримує наступний токен з вхідного тексту.
        
        Returns:
            Token: Наступний токен
            
        Raises:
            LexicalError: Якщо знайдено невідомий символ
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError("Помилка лексичного аналізу")

        return Token(TokenType.EOF, None)


class AST:
    """Базовий клас для всіх вузлів 
    абстрактного синтаксичного дерева."""


class BinOp(AST):
    """
    Вузол бінарної операції в AST.
    
    Атрибути:
        left: Лівий операнд
        op: Оператор
        right: Правий операнд
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    """
   Вузол для представлення числових значень в AST.
   
   Зберігає числове значення та його токен для подальшої обробки 
   в інтерпретаторі арифметичних виразів.

   Attributes:
       token: Token об'єкт, що містить тип та значення числа
       value: Числове значення, витягнуте з токена
   """
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    """
    Синтаксичний аналізатор.
    
    Будує абстрактне синтаксичне дерево з послідовності токенів.
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        """
        Обробляє синтаксичні помилки.
       
        Raises:
           ParsingError: Викидає виняток з повідомленням про помилку синтаксичного аналізу.
        """
        raise ParsingError("Помилка синтаксичного аналізу")

    def eat(self, token_type):
        """
        Перевіряє та 'поглинає' поточний токен.
        
        Перевіряє, чи відповідає поточний токен очікуваному типу.
        Якщо відповідає - переходить до наступного токена, 
        якщо ні - викликає помилку.
        
        Args:
            token_type: Очікуваний тип токена
            
        Raises:
            ParsingError: Якщо тип поточного токена не відповідає очікуваному
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        Обробляє множники (числа та вирази в дужках).
        
        Returns:
            AST: Вузол дерева розбору
            
        Raises:
            ParsingError: При синтаксичній помилці
        """
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        self.error()

    def term(self):
        """
        Обробляє терми (множення та ділення).
        
        Returns:
            AST: Вузол дерева розбору
        """
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        Обробляє вирази (додавання та віднімання).
        
        Returns:
            AST: Корінь дерева розбору
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


def print_ast(node, level=0):
    """
    Виводить AST у читабельному форматі.
    
    Args:
        node: Корінь дерева або піддерева
        level: Рівень відступу для форматування
    """
    indent = "  " * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  left: ")
        print_ast(node.left, level + 2)
        print(f"{indent}  op: {node.op.type}")
        print(f"{indent}  right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")


class Interpreter:
    """
    Інтерпретатор арифметичних виразів.
    
    Обходить AST та обчислює результат виразу.
    """
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        """
        Відвідує та обчислює значення вузла бінарної операції.
        
        Args:
            node: Вузол бінарної операції (BinOp)
            
        Returns:
            float: Результат обчислення бінарної операції
        """
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        """
        Відвідує та повертає значення числового вузла.
        
        Args:
            node: Числовий вузол (Num)
            
        Returns:
            int: Числове значення вузла
        """
        return node.value

    def interpret(self):
        """
        Інтерпретує вхідний вираз.
        
        Returns:
            float: Результат обчислення виразу
        """
        tree = self.parser.expr()
        return self.visit(tree)

    def visit(self, node):
        """
        Відвідує вузол AST, викликаючи відповідний метод відвідування.
        
        Args:
            node: Вузол AST для відвідування
            
        Returns:
            Результат обчислення відповідного методу відвідування
            
        Raises:
            Exception: Якщо для даного типу вузла немає відповідного методу відвідування
        """
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Обробляє випадок, коли немає специфічного методу для відвідування вузла.
        
        Args:
            node: Вузол AST, для якого не знайдено специфічного методу відвідування
            
        Raises:
            Exception: Завжди викидає виняток з повідомленням про відсутність 
                        відповідного методу відвідування
        """
        raise Exception(f"Немає методу visit_{type(node).__name__}")


def main():
    """
    Головна функція програми.
    
    Забезпечує інтерактивний режим роботи з користувачем,
    дозволяючи вводити вирази та отримувати результати обчислень.
    """
    while True:
        try:
            text = input('Введіть вираз (або "exit" для виходу): ')
            if text.lower() == "exit":
                print("Вихід із програми.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
