# GUI tool to select month
import tkinter as tk
from datetime import datetime


def select_month() -> int:
    window = tk.Tk()
    window.title("Select a Month")

    # Set the height of the window to 100 pixels
    window_width = 570
    window_height = 120
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int(screen_width / 4)
    y = int(screen_height / 2 - window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Disable the ability to resize the window
    window.resizable(False, False)

    month_values = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    month = tk.StringVar(window)

    month_now = datetime.now().strftime('%B')
    month.set(month_now)

    option_menu = tk.OptionMenu(window, month, *month_values.keys())
    # configure the size after creating it by using the config method
    option_menu.config(width=35, height=3)
    option_menu.pack()

    def get_month_num():
        window.quit()
        return month_values[month.get()]

    tk.Button(window, text="Get Month Number", command=get_month_num).pack()

    window.mainloop()

    window.withdraw()
    # window.destroy()
    return get_month_num()


if __name__ == '__main__':
    print(type(select_month()))
