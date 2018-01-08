import os
import time
import numpy as np
import matplotlib.pyplot as plt

from utils import img2array
from matplotlib.widgets import Button


class InteractiveImage(object):
    """
    Interactive image class for registering pairs of
    similar points between a crooked image and its
    aligned reference counterpart.
    """
    def __init__(self, img_dir):
        self.dir = img_dir
        self.imgs = self.read_imgs()
        self.counter = 0
        self.prev = 1
        self.curr = None
        self.temp = []
        self.coords = []
        self.N = len(self.imgs)

        # plot the images side by side
        self.fig, self.ax = plt.subplots(nrows=1, ncols=self.N)
        self.draw()

        # add clear button
        clear_ax = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.clear = Button(clear_ax, 'Clear')
        self.clear.on_clicked(self.on_clear)
        done_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.done = Button(done_ax, 'Done')
        self.done.on_clicked(self.on_close)

    def draw(self):

        for i in range(self.N):
            self.ax[i].clear()
            self.ax[i].imshow(self.imgs[i])
            self.ax[i].get_xaxis().set_visible(False)
            self.ax[i].get_yaxis().set_visible(False)

        plt.suptitle('Click on the left and on the right.')
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('close_event', self.on_close)

    def on_clear(self, event):
        print("pressed clear!")

        # clear coordinates
        self.temp = []
        self.coords = []

        # reset previous and counter
        self.counter = 0
        self.prev = 1
        self.curr = None

        # redraw
        print('redrawing')
        self.draw()
        self.update()

    def read_imgs(self):
        """
        Read the reference and crooked img
        from self.dir and return a 4D numpy
        array.
        """
        # grab all file names
        included_extensions = ['png']
        file_names = [
            fn for fn in os.listdir(self.dir)
            if any(fn.endswith(ext) for ext in included_extensions)
        ]

        # loop and convert to numpy array
        imgs = []
        for i in range(len(file_names)):
            filepath = os.path.join(self.dir, file_names[i])
            imgs.append(img2array(filepath, desired_size=(800, 800)))
        imgs = np.array(imgs)

        return imgs

    def on_click(self, event):
        """
        Event handler for button_press_event.

        Registers the mouse click coordinates for
        the original reference image, and the crooked
        image in 2 seperate lists.
        """
        self.counter += 1

        if event.inaxes == self.ax[0]:
            self.curr = 0
            if self.curr == self.prev:
                print("You haven't selected the second pair on the right!")
                return
            self.temp.append((event.x, event.y))
            subplot_num = '1'
            c = plt.Circle((event.xdata, event.ydata), 10, color='b')
            self.ax[0].add_patch(c)
            self.prev = self.curr
        elif event.inaxes == self.ax[1]:
            if self.counter == 1:
                print("You must select from the left first!")
                return
            self.curr = 1
            if self.curr == self.prev:
                print("You haven't select the first pair on the left!")
                return
            self.temp.append((event.x, event.y))
            self.coords.append(self.temp)
            self.temp = []
            subplot_num = '2'
            c = plt.Circle((event.xdata, event.ydata), 10, color='b')
            self.ax[1].add_patch(c)
            self.prev = self.curr
        else:
            return

        msg = "subplot {}: x={}, y={}"
        print(msg.format(subplot_num, event.xdata, event.ydata))
        self.update()

    def on_close(self, event):
        """
        Dump the coordinates as a text file.
        """
        if not self.coords:
            plt.close()
            return

        dump_dir = './dump/'
        if not os.path.exists(dump_dir):
            os.makedirs(dump_dir)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = dump_dir + 'coords_' + timestr + '.txt'
        with open(filename, 'wb') as f:
            for pair in self.coords:
                f.write("{}, {}\n".format(pair[0], pair[1]).encode())

        plt.close()

    def show(self):
        plt.show()

    def update(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def main():

    img_dir = './imgs/'
    inter = InteractiveImage(img_dir)
    inter.show()


if __name__ == '__main__':
    main()
