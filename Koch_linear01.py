import turtle

tur_joe = turtle.Turtle()

def KOCH_FUNCTION(lenth, t = tur_joe):
    t.speed(10000)
    t.ht()
    if lenth > 6:
        lenth_d_3 = lenth // 3
        KOCH_FUNCTION(lenth_d_3, t)
        t.left(60)
        KOCH_FUNCTION(lenth_d_3, t)
        t.right(120)
        KOCH_FUNCTION(lenth_d_3, t)
        t.left(60)
        KOCH_FUNCTION(lenth_d_3, t)
    else:
        t.forward(lenth)
        t.left(60)
        t.fd(lenth)
        t.right(120)
        t.fd(lenth)
        t.left(60)
        t.fd(lenth)
    turtle.done()


def FRACTAL_GENERATE(numbers_of_iteration, lenth, t = tur_joe, spin_of_iteration = 'right'):
    if spin_of_iteration == 'right':
        for i in range(numbers_of_iteration):
            KOCH_FUNCTION(lenth, t)
            t.right(120)
    elif spin_of_iteration == 'left':
        for i in range(numbers_of_iteration):
            KOCH_FUNCTION(lenth, t)
            t.left(120)
    else:
        print("You can not use this value for spin_of_iteration parameter. Allowed values:'right' or 'left' ")
    turtle.done()


if __name__ == "__main__":
    KOCH_FUNCTION(150)
    turtle.done()
