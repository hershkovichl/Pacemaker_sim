import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.widgets import RadioButtons

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-1, 2))
fig.subplots_adjust(left=0.3)
line, = ax.plot([], [], lw=2)
ax2 = fig.add_axes([0.05, 0.4, 0.15, 0.30])
ax2.set_title('Choose Mode')
radio = RadioButtons(ax2, ['NSR', 'AFib'], active=0, activecolor='r')


# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

Afib_mode = False

# animation function.  This is called sequentially
length = 100
y = np.zeros(length)
def animate(i):
    global y
    x = np.linspace(0, 2, length)
    y = np.roll(y, -1)
    if Afib_mode:
        y[-1] = np.random.randn()
    else:
        y[-1] = 0.01 * np.random.randn()
    line.set_data(x, y)
    return line,

def setAfib_mode(label):
    global Afib_mode
    print(label)
    if label == 'AFib':
        Afib_mode = True
        print('setting Afib_mode to True')
    else:
        Afib_mode = False
        print('Resetting')

radio.on_clicked(setAfib_mode)


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                                interval=10, blit=True)

plt.show()