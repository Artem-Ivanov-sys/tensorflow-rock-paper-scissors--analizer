from tensorflow.keras.models import load_model
from tensorflow.image import resize
import cv2
import time
import numpy as np

model = load_model("./rock-paper-scissors.h5")

def make_prediction(img):
    image = np.resize(resize(img, (150, 150)) / 255, (1, 150, 150, 3))
    return model.predict(image, verbose=0)[0]

width, height = 480, 270

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
time_prev_ = 0

cv2.namedWindow("Cap", cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("Cap", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if success == False:
        input("Failed to connect")
    time_ = time.time()
    fps = 1 / (time_-time_prev_)

    time_prev_ = time_
    tensor = make_prediction(img)

    cv2.putText(img, f"FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (220, 10, 10), 2)
    index = 0 if tensor[0] > tensor[1] and tensor[0] > tensor[2] else 1 if tensor[1] > tensor[2] and tensor[1] > tensor[0] else 2
    cv2.putText(img, f"{['Paper', 'Rock', 'Scissors'][index]}: {int(tensor[index]*1000)/10}%",
                (20, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (220, 10, 10), 2)

    cv2.imshow("Cap", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
