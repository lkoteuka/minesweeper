def bomb():
    print("YOU ARE DEAD!!!")


def none():
    print("Nothing")


def number(num):
    def print_number():
        print("Number ", num)

    return print_number
