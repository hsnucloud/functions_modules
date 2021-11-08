# getImgCoords.py
"""
Return a set of x-y coordinates from reading an image
"""
# Import modules
import cv2

class getImageCoords():
    def __init__(self, filename):
        self.filename = filename
        self.img = cv2.imread(self.filename)
        cv2.imshow('image', self.img)
        self.img_height = self.img.shape[0]
        self.data_file = open('data.txt', 'w')
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.data_file.close()

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            y = 706 - self.img_height # Transition of origin to left bottom (moved by image height)
            print('x = ', x, ', = ', y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(self.img, str(x) + ',' + str(y), (x, y), font, 1, (255, 0, 0), 2)
            cv2.imshow('image', self.img)
            self.data_file.write('{}    {}\n'.format(x, y))


if __name__ == '__main__':
    file = 'IMG-7687.jpg'
    img = getImageCoords(file)