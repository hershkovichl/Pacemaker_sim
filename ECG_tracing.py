import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.widgets import RadioButtons
import heart_activity
import Pacemaker

# Initialize the figure, axes, and buttons
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-1, 2))
ax.set_ylabel('mv')
fig.subplots_adjust(left=0.3)
line, = ax.plot([], [], lw=2)
ax2 = fig.add_axes([0.05, 0.5, 0.18, 0.30])
ax2.set_title('Choose Mode')
ax3 = fig.add_axes([0.05, 0.2, 0.18, 0.2])
ax3.set_title('Pacemaker')
radio = RadioButtons(ax2, ['NSR', 'AFib', 'AV Block', 'AFib + Block'], active=0, activecolor='r')
radio2 = RadioButtons(ax3, ['On', 'Off'], active = 1, activecolor='r')
fig.set_size_inches(10,4)
def init():
    line.set_data([], [])
    return line,

# Initialize heart object for electrophysiology simulation
heart = heart_activity.Heart()

# Animation function, gets called on each frame to update the "line"
length = 200
y = np.zeros(length)
def animate(i):
    global y
    x = np.linspace(0, 2, length)
    y = np.roll(y, -1)
    y[-1] = next(heart) # Notable: the line that gets the value from the heart
    line.set_data(x, y)
    return line,

# Function for how the radio buttons manipulate the graph (through the heart object):
def setAfib_mode(label):
    global heart
    if label == 'AFib':
        heart.set_rhythm('AFib')
    elif label == 'NSR':
        heart.set_rhythm('NSR')
    elif label == 'AV Block':
        heart.set_rhythm('AV_Block')
    elif label == 'AFib + Block':
        heart.set_rhythm('AFib_AV_Block')

def setPace(label):
    if label == 'On':
        pacemaker = Pacemaker.ModeSwitching(heart)
        heart.set_pacemaker(pacemaker)
    if label == 'Off':
        heart.remove_pacemaker()

radio.on_clicked(setAfib_mode)
radio2.on_clicked(setPace)

# Initialize and display the animation:
anim = animation.FuncAnimation(fig, animate, init_func=init,
                                interval=10, blit=True, cache_frame_data=False)
plt.show()