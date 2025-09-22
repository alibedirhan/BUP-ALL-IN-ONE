import tkinter as tk
from ISKONTO_HESABI.ui_components import ModernPriceCalculatorUI

def main():
    root = tk.Tk()
    root.title("İskonto Hesaplama")
    app = ModernPriceCalculatorUI(root)
    root.mainloop()

def run_program():
    main()

if __name__ == "__main__":
    main()
