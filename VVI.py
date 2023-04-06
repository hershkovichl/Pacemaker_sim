import time, threading, queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

consoleBuffer = []

def consoleInput(myBuffer):
    while True:
        myBuffer.append(input())

threading.Thread(target=consoleInput, args=(consoleBuffer,), daemon=True).start()

fig, ax = plt.subplots()
xs = [0]
ys = [0]


def animate(i, xs, ys):
    y = np.random.randint(0,5)
    ys.append(y)
    xs.append(xs[-1] + 1)

    while consoleBuffer:
        userIn = consoleBuffer.pop(0)
        print(f'Output: {userIn}')
        if userIn == 'jump':
            ys[-1] = 10

    xs = xs[-20:]
    ys = ys[-20:]

    ax.clear()
    ax.set_ylim((0,15))
    ax.plot(xs, ys)
    plt.xticks(rotation=45, ha='right')

ani = animation.FuncAnimation(fig, func=animate, fargs=(xs,ys), interval = 1000 * 1/60)
plt.show()

