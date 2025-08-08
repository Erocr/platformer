from Inputs import *
from View.View import *
from Model import *
import time


def main():
    view = View()
    inputs = Inputs()
    model = Model()

    while not inputs.quit:
        inputs.update()

        model.update(inputs)

        view.draw(model)

        view.flip()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
