# figma_link = https://www.figma.com/file/sCynZBir5r3hkOBKR7Q52h/Untitled?node-id=9%3A2
# token = 360319-5edeceef-3857-4fed-9f8f-1efdfc96c2d1
import tkinter.filedialog
from tkinter import *
import pytesseract as tess
import cv2
import aspose.words as aw
import pyttsx3
import speech_recognition as sr
import datetime
import threading
import queue
import output_window

tess.pytesseract.tesseract_cmd = r'C:\Users\Faysal Ahmad\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def btn_clicked2():

    file_path = tkinter.filedialog.askopenfile()
    img = cv2.imread(file_path.name)

    string = tess.image_to_string(img)
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    builder.write(string)

    print(string)

    h, w, _ = img.shape  # assumes color image

    # run tesseract, returning the bounding boxes
    boxes = tess.image_to_boxes(img)

    # draw the bounding boxes on the image
    for b in boxes.splitlines():
        b = b.split()

        cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
        cv2.putText(img, b[0], (int(b[1]), h - int(b[2]) + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

    cv2.imshow("Detected Image", img)

    window.withdraw()
    output_window.show_output_window(string, doc)


def speak(text):
    engine.setProperty('rate', 125)
    engine.say(text)
    engine.runAndWait()


def wishme(queue):
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir"
    else:
        text = "Good Evening sir"

    queue.put(f'{text}.')
    speak(text)

    queue.put("Welcome to Image to Text Converter??\n")
    speak("Welcome to Image to Text Converter?")


r = sr.Recognizer()


def takecommand():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 5, 5)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")

    except Exception as e:
        print(e)

        speak("")
        return "None"

    return query


def my_loop(queue):
    wishme(queue)

    while True:
        query = takecommand()

        # Logic for executing task based query
        if 'upload photo' in query:
            btn_clicked2()

        elif 'close the application' in query:
            queue.put("Thank You For Using Image to Text Converter")
            speak("Thank You For Using Image to Text Converter")
            queue.put("\Thank You For Using Image to Text Converter")
            window.destroy()
            exit()
            break  # exit loop and thread will end


def update_text():
    if not queue.empty():
        text = queue.get()
        if text == '\quit':
            window.destroy()  # close window and stop `window.mainloop()`
            return  # don't run `after` again

    window.after(200, update_text)


def btn_clicked():
    print("TP")


if __name__ == '__main__':
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # Main Window
    window = Tk()

    window.configure(bg="#ffffff")
    window.title("Image to Text Converter")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (794 / 2))
    y_cordinate = int((screen_height / 2) - (420 / 2))

    window.geometry("{}x{}+{}+{}".format(794, 420, x_cordinate, y_cordinate))

    canvas = Canvas(
        window,
        bg="#ffffff",
        height=420,
        width=794,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"background.png")
    background = canvas.create_image(
        397.0, 210.0,
        image=background_img)

    img0 = PhotoImage(file=f"img0.png")
    b0 = Button(
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked,
        relief="flat",
        activebackground="#0094FF")

    b0.place(
        x=316, y=234,
        width=167,
        height=50)

    img1 = PhotoImage(file=f"img1.png")
    b1 = Button(
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked2,
        relief="flat",
        activebackground="#0094FF")

    b1.place(
        x=298, y=285,
        width=204,
        height=50)

    window.resizable(False, False)

    # t = tk.Text()
    # t.pack()

    queue = queue.Queue()

    update_text()

    task = threading.Thread(target=my_loop,
                            args=(queue,))  # it has to be `,` in `(queue,)` to create tuple with one value
    task.start()  # start thread

    window.mainloop()

    task.join()  # wait for end of thread
