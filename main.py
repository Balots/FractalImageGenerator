import turtle
import tkinter
import re
import random
from PIL import ImageGrab
# ФУНКЦИИ ЧЕРЕПАХИ
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
    def __init__(self, t, screen, axiom="F", width=2, lenth=50.0, angle=60.0, pencolor='#000000'):
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

    def RULES_IMPLEMENTATION(self, detal_number):
        print("Применение правил...")
        for n in range(detal_number):
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
class cmd_for_generation(KOCH_FUNCTION):
    def Dragon_fractal(self, detal_number):
        Dragon_sys2 = KOCH_FUNCTION(self.t, self.screen, lenth=1, axiom="FXFY", angle=90)
        Dragon_sys2.RULES_GENERATE(
            ("FX", "FX+(a)FY+(a)", 0.5), ("FY", "-(a)FX-(a)FY", 0.5),
            ("+(a)", lambda a: f"+({a + random.triangular(-10, 10, random.gauss(0, 2))})"),
            ("-(a)", lambda a: f"-({a + random.triangular(-10, 10, random.gauss(0, 2))})"))
        Dragon_sys2.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right))
        Dragon_sys2.RULES_IMPLEMENTATION(detal_number)
        print(Dragon_sys2.state)
        Dragon_sys2.FRACTAL_GENERATE((0, 0), 0)

    def Koch_snowflake(self, detal_number):
        l_sys = KOCH_FUNCTION(self.t, self.screen, lenth=1, axiom="F-F-F")
        l_sys.RULES_GENERATE(("F", "F+F--F+F"))
        l_sys.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right))
        l_sys.RULES_IMPLEMENTATION(detal_number)
        print(l_sys.state)
        l_sys.FRACTAL_GENERATE((0, 0), 0)

    def Cover_Serpinsky(self, detal_number):
        Cover_sys2 = KOCH_FUNCTION(self.t, self.screen,  lenth=1, axiom="FXF--FF--FF", angle=90)
        Cover_sys2.RULES_GENERATE(("F", "FF"), ("X", "--FXF++FXF++FXF--"))
        Cover_sys2.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right))
        Cover_sys2.RULES_IMPLEMENTATION(detal_number)
        print(Cover_sys2.state)
        Cover_sys2.FRACTAL_GENERATE((0, 0), -180)

    def Wood_fractal_no_param(self, detal_number):
        WoodSys = KOCH_FUNCTION(self.t, self.screen, lenth=5, axiom="A", angle=33)
        WoodSys.RULES_GENERATE(("A", "F[+A][-A]"), ("F", "FF"))
        WoodSys.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right))
        WoodSys.RULES_IMPLEMENTATION(detal_number)
        WoodSys.FRACTAL_GENERATE((0, -200), 90)

    def Grass_fractal(self, detal_number):
        GrassSys = KOCH_FUNCTION(self.t, self.screen, lenth=1, axiom="F", angle=25.7)
        GrassSys.RULES_GENERATE(("F", "F[+F]F[-F]F"))
        GrassSys.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right))
        GrassSys.RULES_IMPLEMENTATION(detal_number)
        GrassSys.FRACTAL_GENERATE((0, -200), 90)

    def Little_Tree_fractal(self, detal_number):
        TreeSys = KOCH_FUNCTION(t=self.t, screen=self.screen, lenth=10, axiom="F", angle=22.5)
        TreeSys.RULES_GENERATE(("F", "FF-[-F+F+F]+[+F-F-F]"))
        TreeSys.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right))
        TreeSys.RULES_IMPLEMENTATION(detal_number)
        print(TreeSys.state)
        TreeSys.FRACTAL_GENERATE((0, -200), 90)

    def Tree_param_2(self, detal_number):
        TreeSys = KOCH_FUNCTION(self.t, self.screen, lenth=20, axiom="A", angle=20)
        TreeSys.RULES_GENERATE(
            ("A", f"F(1, 1)[+({TreeSys.angle})A][-({TreeSys.angle})A]", 0.9),
            ("A", f"F(1, 1)[-({TreeSys.angle})A]", 0.05),
            ("A", f"F(1, 1)[+({TreeSys.angle})A]", 0.05),

            ("F(x, y)", lambda x, y: f"F({(1.2 + random.triangular(-0.5, 0.5, random.gauss(0, 1))) * x}, {1.3 * y})"),
            ("+(x)", lambda x: f"+({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
            ("-(x)", lambda x: f"-({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
        )
        TreeSys.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right),
                               ("A", cmd_turtle_leaf))
        TreeSys.RULES_IMPLEMENTATION(detal_number)
        print(TreeSys.state)
        TreeSys.FRACTAL_GENERATE((0, -300), 90)

    def Tree_param_4(self, detal_number):
        TreeSys = KOCH_FUNCTION(self.t, self.screen, lenth=20, axiom="A", angle=20, pencolor='#30221A')
        TreeSys.RULES_GENERATE(
            ("A", f"F(1, 1)[+({TreeSys.angle})A][-({TreeSys.angle})A]", 0.5),
            (
                "A", f"F(1, 1)[++({TreeSys.angle})A][+({TreeSys.angle})A][-({TreeSys.angle})A][--({TreeSys.angle})A]",
                0.4),
            ("A", f"F(1, 1)[-({TreeSys.angle})A]", 0.05),
            ("A", f"F(1, 1)[+({TreeSys.angle})A]", 0.05),

            ("F(x, y)", lambda x, y: f"F({(1.2 + random.triangular(-0.5, 0.5, random.gauss(0, 1))) * x}, {1.3 * y})"),
            ("+(x)", lambda x: f"+({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
            ("-(x)", lambda x: f"-({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
        )
        TreeSys.add_rules_move(("F", cmd_turtle_fd),
                               ("+", cmd_turtle_left),
                               ("-", cmd_turtle_right),
                               ("A", cmd_turtle_leaf))
        TreeSys.RULES_IMPLEMENTATION(detal_number)
        print(TreeSys.state)
        TreeSys.FRACTAL_GENERATE((0, -200), 90)

# СОЗДАЁМ МЕТОД ДЛЯ ВСЕХ КНОПОК
class AppFun:
    def __init__(self, root, screen, canvas, tur_joe):
        self.root = root
        self.screen = screen
        self.canvas = canvas
        self.tur_joe = tur_joe
        # СОЗДАЁМ МЕТОД ДЛЯ ВЗАИМОДЕЙСТВИЯ С ГЕНЕРАТОРОМ
        self.MAINFun = cmd_for_generation(t=self.tur_joe, screen=self.screen)



    # ФУНКЦИИ КНОПОК
    def btn_tree_param_4(self, ImplementNumber):
        self.MAINFun.Tree_param_4(ImplementNumber)

    def btn_tree_param_2(self, ImplementNumber):
        self.MAINFun.Tree_param_2(ImplementNumber)

    def btn_koch_snowlake(self, ImplementNumber):
        self.MAINFun.Koch_snowflake(ImplementNumber)

    def btn_dragon_fractale(self, ImplementNumber):
        self.MAINFun.Dragon_fractal(ImplementNumber)
    def btn_cover_serp(self, ImplementNumber):
        self.MAINFun.Cover_Serpinsky(ImplementNumber)

    def btn_wood_no_param(self, ImplementNumber):
        self.MAINFun.Wood_fractal_no_param(ImplementNumber)

    def btn_grass(self, ImplementNumber):
        self.MAINFun.Grass_fractal(ImplementNumber)

    def btn_little_tree(self, ImplementNumber):
        self.MAINFun.Little_Tree_fractal(ImplementNumber)

    def btn_clear_canvas(self):
        self.canvas.delete("all")
    def btn_save_image(self):
        self.canvas = self.screen.getcanvas()
        self.canvas.postscript(file="image.ps")










 # ОСНОВНЫЕ НАСТРОЙКИ ПРИЛОЖЕНИЯ
root = tkinter.Tk()  # ЭКРАН ПРИЛОЖЕНИЯ
root2 = tkinter.Tk()  # ЭКРАН ЧЕРЕПАХИ
width = root2.winfo_screenwidth()
height = root2.winfo_screenheight()
canvas = tkinter.Canvas(root2)
canvas.pack()
canvas.config(width=width, height=height)
screen = turtle.TurtleScreen(canvas)
tur_joe = turtle.RawTurtle(screen)
tur_joe.ht()
screen.tracer(0, 0)
#btn_new_tur = tkinter.Button(root, text="Создать новую черепаху", command=ExFun1.Add_new_turtle)
ImplementNumber_value = 6

# СОЗДАЁМ МЕТОД ДЛЯ ВСЕХ КНОПКОК
ExFun = AppFun(root=root, screen=screen, canvas=canvas, tur_joe=tur_joe)




# ФУНКЦИОНАЛ КНОПОК
def change_implement_deep():
    return int(ImplementNumber.get())
def btn_tree_param_4():
    ExFun.btn_tree_param_4(change_implement_deep())

def btn_tree_param_2():
    ExFun.btn_tree_param_2(change_implement_deep())

def btn_koch_snowlake():
    ExFun.btn_koch_snowlake(change_implement_deep())

def btn_dragon_fractale():
    ExFun.btn_dragon_fractale(change_implement_deep())

def btn_cover_serp():
    ExFun.btn_cover_serp(change_implement_deep())

def btn_wood_no_param():
    ExFun.btn_wood_no_param(change_implement_deep())

def btn_grass():
    ExFun.btn_grass(change_implement_deep())

def btn_clear_canvas():
    ExFun.btn_clear_canvas()
def btn_little_tree():
    ExFun.btn_little_tree(change_implement_deep())

def btn_save():
    ExFun.btn_save_image()

# СОЗДАЁМ ОКНА ВВОДА
ImplementNumber = tkinter.Spinbox(from_=2, to=15, increment=1, command=change_implement_deep)

# СОЗДАЁМ КНОПКИ
btn_little_tree_f = tkinter.Button(root, text="Параметрическое дерево тип 0", command=btn_little_tree)
btn_tree_param_2_f = tkinter.Button(root, text="Параметрическое дерево тип 1", command=btn_tree_param_2)
btn_tree_param_4_f = tkinter.Button(root, text="Параметрическое дерево тип 2", command=btn_tree_param_4)
btn_koch_snowlake_f = tkinter.Button(root, text="Снежинка Коха", command=btn_koch_snowlake)
btn_dragon_fractale_f = tkinter.Button(root, text="Фрактал Дракона", command=btn_dragon_fractale)
btn_cover_serp_f = tkinter.Button(root, text="Ковёр Серпинского", command=btn_cover_serp)
btn_wood_no_param_f = tkinter.Button(root, text="Непараметрическое дерево", command=btn_wood_no_param)
btn_grass_f = tkinter.Button(root, text="Трава", command=btn_grass)
btn_clear_canvas_f = tkinter.Button(root, text="Очистить холст", command=btn_clear_canvas)
btn_save_f = tkinter.Button(root, text="Сохранить изображение", command=btn_save)






def main():
    # ПАКУЕМ ПРИЛОЖЕНИЕ
    btn_little_tree_f.grid(row=0, column=0)
    btn_tree_param_2_f.grid(row=1, column=0)
    btn_tree_param_4_f.grid(row=2, column=0)
    btn_koch_snowlake_f.grid(row=3, column=0)
    btn_dragon_fractale_f.grid(row=4, column=0)
    btn_cover_serp_f.grid(row=5, column=0)
    btn_wood_no_param_f.grid(row=6, column=0)
    btn_grass_f.grid(row=7, column=0)
    ImplementNumber.grid(row=0, column=1)
    btn_clear_canvas_f.grid(row=0, column=2)
    btn_save_f.grid(row=0, column=3)
    #btn_new_tur.pack(anchor="nw")
    root.mainloop()

if __name__ == "__main__":
    main()