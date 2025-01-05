import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton


class MonthSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select a Month")
        self.setFixedSize(570, 120)

        # Set the position of the window
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        x = int(screen_width / 4)
        y = int(screen_height / 2 - 120 / 2)
        self.move(x, y)

        # Month dictionary
        self.month_values = {
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

        self.combo_box = None
        self.button = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Current month
        month_now = datetime.now().strftime('%B')

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(self.month_values.keys())
        self.combo_box.setCurrentText(month_now)
        self.combo_box.setFixedWidth(400)

        # Button to get month number
        self.button = QPushButton("Get Month Number", self)
        self.button.clicked.connect(self.get_month_num)

        # Adding widgets to layout
        layout.addWidget(self.combo_box)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def get_month_num(self):
        selected_month = self.combo_box.currentText()
        month_num = self.month_values[selected_month]
        # print(f"Selected Month Number: {month_num}")
        self.close()
        return month_num


def select_month():
    app = QApplication(sys.argv)
    window = MonthSelector()
    window.show()
    app.exec_()
    return window.get_month_num()


if __name__ == '__main__':
    print(f"{select_month() = }")