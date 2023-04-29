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
radio2 = RadioButtons(ax3, ['Mode Switching','VVI', 'Off'], active = 2, activecolor='r')
fig.set_size_inches(10,4)
def init():
    line.set_data([], [])
    return line,

# Axes styling
from matplotlib.ticker import AutoMinorLocator
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))

# ax.set_ylim(-amplitude_ecg, amplitude_ecg)
# ax.set_xlim(0, secs)

ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
ax.grid(which='minor', linestyle='-', linewidth='0.5', color=(1, 0.7, 0.7))

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

pacemaker = Pacemaker.ModeSwitching(heart)
def setPace(label):
    if label == 'Mode Switching':
        heart.set_pacemaker(pacemaker)
    if label == 'VVI':
        heart.set_pacemaker(pacemaker.VVI)
    if label == 'Off':
        heart.remove_pacemaker()

radio.on_clicked(setAfib_mode)
radio2.on_clicked(setPace)

# Initialize and display the animation:
anim = animation.FuncAnimation(fig, animate, init_func=init,
                                interval=10, blit=True, cache_frame_data=False)
plt.show()