import re
import random

def cmd_turtle_fd(t, lenth, pencolor, *args):
    t.pencolor(pencolor)
    t.pensize(args[1])
    t.fd(lenth * args[0])


def cmd_turtle_left(t, *args):
    t.left(args[0])


def cmd_turtle_right(t, *args):
    t.right(args[0])


def cmd_turtle_leaf(t, lenth, *args):
    if random.random() > 0.9:
        return
    p = t.pensize
    t.pensize(5)
    p = random.randint(0, 2)
    if p == 0:
        t.pencolor('#009900')
    elif p == 1:
        t.pencolor('#667900')
    else:
        t.pencolor('#20BB00')

    t.fd(lenth // 2)
    t.pencolor('#000000')
    t.pensize(p)




# МЕТОД ГЕНЕРАЦИИ ФРАКТАЛОВ
class KOCH_FUNCTION:
    def __init__(self, t, screen, detal_number, axiom="F", width=2, lenth=50.0, angle=60.0, pencolor='#000000'):
        self.axiom = axiom
        self.state = axiom
        self.width = width
        self.lenth = lenth
        self.angle = angle
        self.t = t
        self.rules = {}                 # список правил
        self.t.pensize(self.width)
        self.rules_key = None
        self.key_re_list = []           # список шаблонов команд
        self.cmd_functions = {}         # словарь связей команд и функций
        self.pencolor = pencolor
        self.screen = screen
        self.turtles = {}
        self.num_turtle = []
        self.detal_number = detal_number

    def RULES_GENERATE(self, *rules):
        print("Генерация правил...")
        for r in rules:
            p = 1
            if len(r) == 3:
                key, value, p = r
            else:
                key, value = r

            key_re = key.replace("(", r"\(")
            key_re = key_re.replace(")", r"\)")
            key_re = key_re.replace("+", r"\+")
            key_re = key_re.replace("-", r"\-")

            if not isinstance(value, str):
                key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
                self.key_re_list.append(key_re)

            if not self.rules.get(key):
                self.rules[key] = [(value, key_re, p)]
            else:
                self.rules[key].append((value, key_re, p))

    def get_random_rule(self, rules):
        p = random.random()
        off = 0
        for v in rules:
            if p < (v[2] + off):
                print(v)
                return v
            off += v[2]
        print(rules[0])
        return rules[0]

    def update_param_cmd(self, m):
        if not self.rules_key:
            return ""

        rule = self.rules_key[0] if len(self.rules_key) == 1 else self.get_random_rule(self.rules_key)

        if isinstance(rule[0], str):
            return rule[0].lower()
        else:
            args = list(map(float, m.groups()))
            return rule[0](*args).lower()

    def RULES_IMPLEMENTATION(self):
        print("Применение правил...")
        for n in range(self.detal_number):
            for key, rules in self.rules.items():
                self.rules_key = rules
                self.state = re.sub(rules[0][1], self.update_param_cmd, self.state)
                self.rules_key = None

            self.state = self.state.upper()

    def set_turtle(self, my_tuple):
        self.t.up()
        self.t.goto(my_tuple[0], my_tuple[1])
        self.t.seth(my_tuple[2])
        self.t.down()

    def add_rules_move(self, *moves):
        for key, func in moves:
            self.cmd_functions[key] = func


    def FRACTAL_GENERATE(self, start_pos, start_angle):
        print("Генерация фрактала")
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        coordination_stack = []
        key_list_re = "|".join(self.key_re_list)
        for current_action in re.finditer(r"(" + key_list_re + r"|.)", self.state):
            cmd = current_action.group(0)
            args = [float(x) for x in current_action.groups()[1:] if x]

            if 'F' in cmd:
                if len(args) > 0 and self.cmd_functions.get('F'):
                    self.cmd_functions['F'](self.t, self.lenth, self.pencolor, *args)

                else:
                    self.t.forward(self.lenth)
            elif 'S' in cmd:
                if len(args) > 0 and self.cmd_functions.get('S'):
                    self.cmd_functions['S'](self.t, self.lenth, *args)
                else:
                    self.t.up()
                    self.t.forward(self.lenth)
                    self.t.down()
            elif '+' in cmd:
                if len(args) > 0 and self.cmd_functions.get('+'):
                    self.cmd_functions['+'](self.t, self.angle, *args)
                else:
                    self.t.left(self.angle)
            elif '-' in cmd:
                if len(args) > 0 and self.cmd_functions.get('-'):
                    self.cmd_functions['-'](self.t, self.angle, *args)
                else:
                    self.t.right(self.angle)
            elif 'A' in cmd:
                if self.cmd_functions.get('A'):
                    self.cmd_functions['A'](self.t, self.lenth, *args)
            elif "[" in cmd:
                coordination_stack.append((self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
            elif "]" in cmd:
                xcor, ycor, head, w = coordination_stack.pop()
                self.set_turtle((xcor, ycor, head))
                self.width = w
                self.t.pensize(self.width)

# ПАРАМЕТРЫ ГЕНЕРАЦИИ ФРАКТАЛОВ/УПРАВЛЯЮЩАЯ КОНСТРУКЦИЯ ДЛЯ ВЗАИМОДЕЙСТВИЯ С KOCH_FUNCTION
