import cv2


def pre_processing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equalized_frame = cv2.equalizeHist(img)
    blurred_frame = cv2.GaussianBlur(equalized_frame, (5, 5), 0)
    return blurred_frame