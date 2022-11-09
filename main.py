import tkinter as tk
from tkinter import ttk
from cbr import cbr_algorithm
import pandas as pd
import numpy as np


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.init_widgets()

    def callback(self):
        checksVals = self.checksVals
        arrLabel = []
        arrValue = []
        for i in range(np.array(checksVals).size):
            arrLabel.append(f'mahh{i}')
            arrValue.append(checksVals[i].get())
        case = pd.DataFrame(np.array([arrValue]), columns=arrLabel)
        res = cbr_algorithm(case)
        self.openNewWindow(data=res)

    def init_widgets(self):
        label = tk.Button(
            self.master, text="Chọn những triệu chứng mà bạn đang mắc phải:")
        label.pack()

        space1 = tk.Label(self.master, text="Space")
        space1.pack()

        # Get list symptom
        symptom = pd.read_csv(
            'input/symptom.csv')
        self.checks = []
        self.checksVals = []

        # Display list checkbox
        for i in range(symptom.shape[0]):
            case_row = symptom.loc[i, :].to_numpy()
            var = tk.IntVar()
            self.checksVals.append(var)
            button = tk.Checkbutton(self.master, text=f"{case_row[1]}", name=case_row[0].lower(),
                                    variable=var,
                                    onvalue=1,
                                    offvalue=0,
                                    )
            self.checks.append(button)
            button.grid(row=int(i/2), column=i)
            button.pack()

        space = tk.Label(self.master, text="Space")
        space.pack()

        submit = tk.Button(self.master, text="Submit", command=self.callback)
        submit.pack()
        self.quit = tk.Button(self.master, text="Quit",
                              command=self.master.destroy)
        self.quit.pack()

    def openNewWindow(self, data):
        disease = pd.read_csv(
            'input/disease.csv')
        res = ''
        for i in range(disease.shape[0]):
            disease_row = disease.loc[i, :]
            if (disease_row[0] == data):
                res = disease_row[1]
                break

        # Toplevel object which will
        # be treated as a new window
        newWindow = tk.Toplevel(self.master)

        # sets the title of the
        # Toplevel widget
        newWindow.title("Kết quả")

        # sets the geometry of toplevel
        newWindow.geometry("700x400")
        label = tk.Button(
            newWindow, text="Kết luận: Bệnh hô hấp mà bạn mắc phải là:")
        label.pack()

        result = tk.Button(newWindow, text=res)
        result.pack()


root = tk.Tk()
app = Application(master=root)
app.master.title("Predict diseases")
app.master.minsize(1000, 600)
app.mainloop()
