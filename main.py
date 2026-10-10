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

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
