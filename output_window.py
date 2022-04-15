import tkinter
from tkinter import *
import aspose.words as aw


def show_output_window(string, doc):
    def btn_clicked3():
        download_path = tkinter.filedialog.askdirectory()
        doc.save(download_path + "/result.docx")
        output_window.destroy()

    output_window = Tk()

    output_window.geometry("794x420")
    output_window.configure(bg="#ffffff")
    output_window.title("Output Of the Converter")

    output_canvas = Canvas(
        output_window,
        bg="#ffffff",
        height=420,
        width=794,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    output_canvas.place(x=0, y=0)

    output_canvas.create_text(
        397.0, 29.5,
        text="From Image to Text Converter",
        fill="#000000",
        font=("Gotham-Bold", int(20.0)))

    output_canvas.create_text(
        90, 90,
        text=string,
        fill="#000000",
        font=("TimesNewRomanPS-BoldMT", int(15.0)))

    img3 = PhotoImage(file=f"img3.png")
    b2 = Button(
        image=img3,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked3,
        relief="flat",
        activebackground="#FFFFFF")

    b2.place(
        x=313, y=353,
        width=167,
        height=50)

    output_window.resizable(False, False)
    output_window.mainloop()