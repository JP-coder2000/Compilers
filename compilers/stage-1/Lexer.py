from enum import IntEnum

class Tag(IntEnum):
    EOF = 65535
    ERROR = 65534
    ## Operators ##
    GEQ = 258
    LEQ = 259
    NEQ = 260
    ASSIGN = 261
    ## REGULAR EXPRESSIONS ##
    ID = 358
    NUMBER = 359
    STRING = 360
    TRUE = 361
    FALSE = 362
    ## ADD THE MISSING RESERVED WORDS, JUST FOLLOW THE NUMBER SEQUENCE ##
    VAR = 457
    FORWARD = 458
    BACKWARD = 459
    RIGHT = 460
    LEFT = 461
    SETX = 462
    SETY = 463
    SETXY = 464
    HOME = 465
    CLEAR = 466
    CIRCLE = 467
    ARC = 468
    PENUP = 469
    PENDOWN = 470
    COLOR = 471
    PENWIDTH = 472
    PRINT = 473
    WHILE = 474
    IF = 475
    IFELSE = 476
    AND = 477
    OR = 478
    MOD = 479
    
class Token:
    tag = Tag.EOF
    value = None
    
    def __init__(self, tagId, val = None):
        self.tag = tagId
        self.value = val
        
    def __str__(self):
        if self.tag == Tag.GEQ:
            return "'>='"
        elif self.tag == Tag.LEQ:
            return "'<='"
        elif self.tag == Tag.NEQ:
            return "'<>'"
        elif self.tag == Tag.ASSIGN:
            return "':='"
        elif self.tag == Tag.TRUE:
            return "'#T'"
        elif self.tag == Tag.FALSE:
            return "'#F'"
        elif self.tag == Tag.NUMBER:
            return str(self.value)
        elif self.tag == Tag.ID:
            return "ID = '" + str(self.value) + "'"
        elif self.tag >= Tag.VAR and self.tag <= Tag.MOD:
            return "'" +  str(self.value) + "'"
        elif self.tag == Tag.STRING:
            return str(self.value)
        else:
            return "'" + chr(self.tag) + "'" 
            
class Lexer:
    file_path = None
    position = 0
    buffer_size = 0
    current_buffer = None
    next_buffer = None
    words = {}
    line = 0

    def __init__(self, file_path, buffer_size = 1014):
        self.file_path = file_path
        self.buffer_size = buffer_size
        self.position = 0
        self.current_buffer = ""
        self.next_buffer = ""
        self.line = 1

        with open(self.file_path, 'r') as file:
            file.seek(self.position)
            self.current_buffer = file.read(self.buffer_size)
            self.next_buffer = file.read(self.buffer_size)
            self.position += self.buffer_size

        self.words["VAR"] = Token(Tag.VAR, "VAR")
        self.words["FORWARD"] = Token(Tag.FORWARD, "FORWARD")
        self.words["FD"] = Token(Tag.FORWARD, "FORWARD")
        self.words["BACKWARD"] = Token(Tag.BACKWARD, "BACKWARD")
        self.words["BK"] = Token(Tag.BACKWARD, "BACKWARD")
        self.words["RIGHT"] = Token(Tag.RIGHT, "RIGHT")
        self.words["RT"] = Token(Tag.RIGHT, "RIGHT")
        self.words["LEFT"] = Token(Tag.LEFT, "LEFT")
        self.words["LT"] = Token(Tag.LEFT, "LEFT")
        self.words["SETX"] = Token(Tag.SETX, "SETX")
        self.words["SETY"] = Token(Tag.SETY, "SETY")
        self.words["SETXY"] = Token(Tag.SETXY, "SETXY")
        self.words["HOME"] = Token(Tag.HOME, "HOME")
        self.words["CLEAR"] = Token(Tag.CLEAR, "CLEAR")
        self.words["CLS"] = Token(Tag.CLEAR, "CLEAR")
        self.words["CIRCLE"] = Token(Tag.CIRCLE, "CIRCLE")
        self.words["ARC"] = Token(Tag.ARC, "ARC")
        self.words["PENUP"] = Token(Tag.PENUP, "PENUP")
        self.words["PU"] = Token(Tag.PENUP, "PENUP")
        self.words["PENDOWN"] = Token(Tag.PENDOWN, "PENDOWN")
        self.words["PD"] = Token(Tag.PENDOWN, "PENDOWN")
        self.words["COLOR"] = Token(Tag.COLOR, "COLOR")
        self.words["PENWIDTH"] = Token(Tag.PENWIDTH, "PENWIDTH")
        self.words["PRINT"] = Token(Tag.PRINT, "PRINT")
        self.words["WHILE"] = Token(Tag.WHILE, "WHILE")
        self.words["IF"] = Token(Tag.IF, "IF")
        self.words["IFELSE"] = Token(Tag.IFELSE, "IFELSE")
        self.words["AND"] = Token(Tag.AND, "AND")
        self.words["OR"] = Token(Tag.OR, "OR")
        self.words["MOD"] = Token(Tag.MOD, "MOD")

    def get_next_character(self):
        if len(self.current_buffer) == 0 and len(self.next_buffer) > 0:
            self.current_buffer = self.next_buffer
            with open(self.file_path, 'r') as file:
                file.seek(self.position)
                self.next_buffer = file.read(self.buffer_size)
                self.position += self.buffer_size

        if len(self.current_buffer) > 0:
            character = self.current_buffer[0]
            self.current_buffer = self.current_buffer[1:]

            if character == '\n':
                self.line += 1
            return character
        
        return None
    
    def push_back(self, character):
        if character == '\n':
            self.line -= 1
        self.current_buffer = character + self.current_buffer

    def scan(self):
        while True:
            character = self.get_next_character()

            if character is None:
                return Token(Tag.EOF)
            
            if character.isspace():
                continue

            ## ADD CODE TO SKIP COMMENTS HERE ##
            if character == '%':
                while True:
                    character = self.get_next_character()
                    if character is None or character == '\n':
                        break
                continue

            if character == '<':
                character = self.get_next_character()
                if character in ['=', '>']:
                    if character == '=':
                        return Token(Tag.LEQ, "<=")
                    else:
                        return Token(Tag.NEQ, "<>")
                else:
                    self.push_back(character)
                    return Token(ord('<'))
                
            if character == '>':
                character = self.get_next_character()
                if character == '=':
                    return Token(Tag.GEQ, ">=")
                else:
                    self.push_back(character)
                    return Token(ord('>'))
                
            if character == '#':
                character = self.get_next_character().upper()
                if character in ['T', 'F']:
                    if character == 'T':
                        return Token(Tag.TRUE, "#T")    
                    else:
                        return Token(Tag.FALSE, "#F")    
                else:
                    self.push_back(character)
                    return Token(ord('#'))
                
            if character == ':':
                character = self.get_next_character()
                if character == '=':
                    return Token(Tag.ASSIGN, ":=")
                else:
                    self.push_back(character)
                    return Token(ord(':'))
                
            if character == '"':
                text = ""
                while True:
                    text += character
                    character = self.get_next_character()
                    if character == '"':
                        break
                text += character
                return Token(Tag.STRING, text)
            
            if character.isdigit():
                value = 0.0
                while True:
                    value = (value * 10) + int(character)
                    character = self.get_next_character()
                    if not character.isdigit():
                        break
                
                ## ADD CODE TO PROCESS DECIMAL PART HERE ##
                if character == '.':
                    decimal_factor = 0.1
                    character = self.get_next_character()
                    if character.isdigit():
                        while character.isdigit():
                            value = value + (int(character) * decimal_factor)
                            decimal_factor *= 0.1
                            character = self.get_next_character()
                    else:
                        # No digits after the decimal point is an error
                        self.push_back(character)
                        self.push_back('.')
                        return Token(Tag.NUMBER, value)
                
                self.push_back(character)
                return Token(Tag.NUMBER, value)
            
            if character.isalpha():
                lexem = ""
                while True:
                    lexem += character.upper()
                    character = self.get_next_character()
                    if not character.isalnum():
                        break
                self.push_back(character)

                if lexem in self.words:
                    return self.words[lexem]
                
                token = Token(Tag.ID, lexem)
                self.words[lexem] = token
                return token
            
            return Token(ord(character))