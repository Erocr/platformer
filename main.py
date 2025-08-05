from Inputs import *
from View import *
from Model import *


def main():
    view = View()
    inputs = Inputs()
    model = Model()

    while not inputs.quit:
        inputs.update()

        view.flip()


if __name__ == "__main__":
    main()
