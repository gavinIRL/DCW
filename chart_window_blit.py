import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class ChartWindowBlit:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'ro')

    def start(self):
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-1, 1)
        return self.ln,

    def update(self, frame):
        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln,


if __name__ == "__main__":
    cwb = ChartWindowBlit()
    animation = FuncAnimation(cwb.fig, cwb.update, frames=np.linspace(0, 2*np.pi, 128),
                              init_func=cwb.start, blit=True)
    plt.show()
