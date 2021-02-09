import cv2
import numpy as np

from PyQt5.QtGui import \
    QImage, \
    QPixmap, \
    QPainter, \
    qRgb

from PyQt5.QtWidgets import \
    QWidget

'''
Show a Numpy / OpenCV image.

This class uses Qt functions to show a given image as a Widget. This way,
we can attach that image to our program directly.

The shown images have a fixed width of 480 pixels (random, it can be changed),
We can show gray level images, or color images.
The shown image can be updated at any time.

IMPORTANT: The input image, if it is color, it is considered to be in BGR, and
not in RGB. If you want to provide an RGB image instead, the updateImage
method must be modified.
'''
class ImageWidget(QWidget):
    def __init__(self, parent=0):
        '''
        Constructor
        '''
        super(QWidget, self).__init__(parent)

        self.desired_width = 480
        self.showed_image = None
        self.clearBuffers()

        self.grayscale_colortable = np.array([qRgb(i, i, i) for i in range(256)])

    def updateImage(self, new_image):
        '''
        Change the shown image. The image provided must not be empty.
        If it is a gray level image, we show it as an indexed image, with a
        gray-level palette (There is not another way to do it in Qt), or if
        it is a color image, we convert it into RGB and we show it as it is.

        In this function, the provided image is resized to have a fixed width
        set on construction, and to keep the aspect ratio.
        '''
        if new_image.size:
            # We compute the required scaling factor, for the desired width we
            # want to set the in image.
            scaling_factor = self.desired_width / new_image.shape[1]
            # We resize the image to have the desired width, and keep the
            # aspect ratio
            scaled_image = cv2.resize(new_image, new_image.shape[0:2], scaling_factor, scaling_factor, interpolation=cv2.INTER_LINEAR)

            # We set the Widget size, so it does not take an unlimited space in
            # the MainWindow.
            self.setFixedSize(
                scaled_image.shape[1],
                scaled_image.shape[0])

            height = scaled_image.shape[0]
            width =  scaled_image.shape[1]

            if len(scaled_image.shape) == 2:
                # We create a QImage as an indexed image to show the grayscale
                # values. Because it is in indexed format, we set its color table
                # too to be grayscale.
                self.showed_image = QImage(
                    scaled_image,
                    width,
                    height,
                    width,
                    QImage.Format_Indexed8)
                self.showed_image.setColorTable(self.grayscale_colortable)
            else:
                # If it is a color image, we convert from BGR (format in OpenCV),
                # to RGB. If a RGB image want to be provided, this this line must
                # be erased.
                scaled_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

                # We convert the input image into a QImage, to be shown by Qt
                self.showed_image = QImage(
                    scaled_image,
                    width,
                    height,
                    3*width,
                    QImage.Format_RGB888)

            # We schedule a repaint, in order to update what we show in the widget
            self.repaint()
        else:
            print("Not updating image. The provided image is empty")


    def clearBuffers(self):
        '''
        This method erases the shown image. After calling this method, the widget
        will be blank
        '''
        self.showed_image = QImage()
        self.repaint()

    def paintEvent(self, event):
        '''
        Overloaded function from Qt. This function is the one that changes what
        we draw in the QWidget. We can draw lines, circles, rectangles, or other
        shapes, if we add the required lines into this function.

        This implementation only draws the image set when calling updateImage.
        '''
        if not self.showed_image is None:
            painter = QPainter(self)
            painter.drawPixmap(0,
                0,
                self.showed_image.width(),
                self.showed_image.height(),
                QPixmap(self.showed_image))