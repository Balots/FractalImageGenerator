import turtle

tur_joe = turtle.Turtle()
tur_joe.ht()


class DRAGON_FUNCTION:
    def __init__(self, axiom = "F", t = tur_joe, width = 2, lenth = 50, angle = 60):
        self.axiom = axiom
        self.state = axiom
        self.width = width
        self.lenth = lenth
        self.angle = angle
        self.t = t
        self.rules = {}
        self.t.pensize(self.width)


    def RULES_GENERATE(self, *rules):
        for key, value in rules:
            self.rules[key] = value


    def RULES_IMPLEMENTATION(self, detal_number):
        for n in range(detal_number):
            for key, value in self.rules.items():
                self.state = self.state.replace(key, value.lower())

            self.state = self.state.upper()

    def FRACTAL_GENERATE(self, start_pos, start_angle):
        turtle.tracer(1, 0)
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        for current_action in self.state:
            if current_action == 'F':
                self.t.forward(self.lenth)
            elif current_action == '+':
                self.t.left(self.angle)
            elif current_action == "S":
                self.t.up()
                self.t.forward(self.lenth)
                self.t.down()
            elif current_action == '-':
                self.t.right(self.angle)
        turtle.done()