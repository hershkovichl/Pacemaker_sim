import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.widgets import RadioButtons
import heart_activity

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-1, 2))
ax.set_ylabel('mv')
fig.subplots_adjust(left=0.3)
line, = ax.plot([], [], lw=2)
ax2 = fig.add_axes([0.05, 0.4, 0.15, 0.30])
ax2.set_title('Choose Mode')
radio = RadioButtons(ax2, ['NSR', 'AFib'], active=0, activecolor='r')
fig.set_size_inches(10,4)

def init():
    line.set_data([], [])
    return line,

Afib_mode = False

heart = heart_activity.heart()

length = 200
y = np.zeros(length)
def animate(i):
    global y
    x = np.linspace(0, 2, length)
    y = np.roll(y, -1)
    if Afib_mode:
        y[-1] = 0.03* np.random.randn()
    else:
        y[-1] = 0.01 * np.random.randn() + next(heart.rhythm)
    line.set_data(x, y)
    return line,

def setAfib_mode(label):
    global Afib_mode
    if label == 'AFib':
        Afib_mode = True
    else:
        Afib_mode = False


radio.on_clicked(setAfib_mode)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                                interval=10, blit=True)

plt.show()