import tkinter as tk
from cbr import cbr_algorithm
import pandas as pd
import numpy as np


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.init_widgets()

    def get_symptom(self):
        symptom = pd.read_csv(
            'input/symptom.csv')
        arr = []
        for i in range(symptom.shape[0]):
            case_row = symptom.loc[i, :]
            arr.append(case_row.to_numpy())

        return arr

    def callback(self):
        checksVals = self.checksVals
        arrLabel = []
        arrValue = []
        for i in range(np.array(checksVals).size):
            arrLabel.append(f'mahh{i}')
            arrValue.append(checksVals[i].get())
        case = pd.DataFrame(np.array([arrValue]), columns=arrLabel)
        res = cbr_algorithm(case)
        print(res)

    def init_widgets(self):
        symptom = pd.read_csv(
            'input/symptom.csv')
        self.checks = []
        self.checksVals = []

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

        submit = tk.Button(self.master, text="Submit", command=self.callback)
        submit.pack()

        self.quit = tk.Button(self.master, text="QUIT",
                              command=self.master.destroy)
        self.quit.pack()


root = tk.Tk()
app = Application(master=root)
app.master.title("Predict diseases")
app.master.minsize(1000, 600)
app.mainloop()
