from datetime import datetime
from matplotlib import pyplot
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from random import randrange


class ChartWindowAnimation:
    def __init__(self) -> None:
        self.x_data, self.y_data = [], []
        self.figure = pyplot.figure()
        self.line, = pyplot.plot_date(self.x_data, self.y_data, '-')

    def update(self, frame):
        self.x_data.append(datetime.now())
        self.y_data.append(randrange(0, 100))
        self.line.set_data(self.x_data, self.y_data)
        self.figure.gca().relim()
        self.figure.gca().autoscale_view()
        return self.line,


if __name__ == "__main__":
    cwa = ChartWindowAnimation()
    animation = FuncAnimation(cwa.figure, cwa.update, interval=2000)
    pyplot.show()
