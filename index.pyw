from tkinter.ttk import Button, Label
from tkinter import Tk, filedialog, Text, Frame
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import sys

model = load_model("./rock-paper-scissors.h5")

loaded = False
paths = []

class StdIO:
    def __init__(self, target):
        self.target = target
    def write(self, text):
        self.target.insert("end", text)
    def flush(self):
        pass
    def clear(self):
        self.target.delete(0.0, "end")

def open_file():
    global loaded

    if loaded:
        return
    path = filedialog.askopenfilename()
    if path:
        paths.append(path)
        load["text"] = path.split("/")[-1]
        loaded = True

picture = None
def process():
    global loaded
    def set_picture(path):
        global picture
        picture_ = Image.open(path)
        width, height = picture_.size
        aspect_ratio = width / height

        if width > height:
            new_width = 314
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 314
            new_width = int(new_height * aspect_ratio)
        
        picture = ImageTk.PhotoImage(picture_.resize((new_width, new_height)))
        picture_label["image"] = picture

    if loaded:
        image = load_img(paths[-1], target_size=(150, 150))
        image = np.expand_dims(img_to_array(image) / 255, axis=0)
        print(image.shape)
        sys.stdout = StdIO(answer)
        sys.stdout.target["state"] = "normal"
        sys.stdout.clear()
        prediction = model.predict(image)[0]
        sys.stdout.clear()
        print("Prediction: (%.3f, %.3f, %.3f )" % (*prediction,))
        if prediction[0] > prediction[1] and prediction[0] > prediction[2]:
            print("Answer: Paper")
        elif prediction[1] > prediction[0] and prediction[1] > prediction[2]:
            print("Answer: Rock")
        else:
            print("Answer: Scissors")
        loaded = False
        sys.stdout.target["state"] = "disabled"
        sys.stdout = sys.__stdout__
        set_picture(paths[-1])

window = Tk()
window.geometry("640x320+100+100")
window.title("Rock paper scissors Cursed")
window.resizable(width=False, height=False)

frame1 = Frame(bd=3, relief="groove")
frame1.pack(side="left", fill="both", expand=True)
frame1.pack_propagate(False)
frame2 = Frame(bd=3, relief="groove")
frame2.pack(side="left", fill="both", expand=True)
frame2.pack_propagate(False)

Label(frame1, text="Open image").pack(side="top")
load = Button(frame1, text="Load image")
load.pack(side="top")
load.bind("<Button-1>", lambda e: open_file())

Label(frame1, text="Then process it with my CNN").pack(side="top")
start = Button(frame1, text="Process")
start.pack(side="top")
start.bind("<Button-1>", lambda e: process())

Label(frame1, text="And its prediction").pack(side="top")
answer = Text(frame1, state="disabled")
answer.pack(side="bottom", fill="both")

picture_label = Label(frame2)
picture_label.pack(side="top")

window.mainloop()
