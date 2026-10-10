import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("360x510")
        self.root.resizable(False, False)

        self.display_value = tk.StringVar(value="0")
        self.first_operand = None
        self.pending_operator = None
        self.new_input = True
        self.memory = 0
        self.create_interface()

    def create_interface(self):
        display = tk.Entry(
            self.root,
            textvariable=self.display_value,
            font=("Arial", 25),
            justify="right",
            state="readonly",
            readonlybackground="white"
        )
        display.grid(
            row=0, column=0, columnspan=4,
            padx=10, pady=15, sticky="nsew", ipady=10
        )

        buttons = [
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
            ["7", "8", "9", ""],
            ["4", "5", "6", ""],
            ["1", "2", "3", ""],
            ["", "0", ".", ""],
            ["", "", "", ""]
        ]

        for row_index, row in enumerate(buttons, start=1):
            for column_index, value in enumerate(row):
                if not value:
                    continue

                button = tk.Button(
                    self.root,
                    text=value,
                    font=("Arial", 15),
                    command=lambda v=value: self.on_button_click(v)
                )
                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=3, pady=3, sticky="nsew",
                    ipadx=3, ipady=8
                )

        for column in range(4):
            self.root.grid_columnconfigure(column, weight=1)

        for row in range(1, 9):
            self.root.grid_rowconfigure(row, weight=1)

    def input_digit(self, digit):
        current = self.display_value.get()

        if self.new_input or current == "0":
            self.display_value.set(digit)
        else:
            self.display_value.set(current + digit)

        self.new_input = False

    def input_decimal(self):
        current = self.display_value.get()

        if self.new_input:
            self.display_value.set("0.")
            self.new_input = False
        elif "." not in current:
            self.display_value.set(current + ".")

    def on_button_click(self, value):
        if value.isdigit():
            self.input_digit(value)
        elif value == ".":
            self.input_decimal()

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
