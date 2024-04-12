from PyQt6 import QtWidgets
from gui import Ui_MainWindow
from backend.object import Object
from backend.models import Point


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.simulatePushButton.clicked.connect(lambda: self.simulate())

    def simulate(self):
        coords = Point(self.ui.coords_x.value(), self.ui.coords_y.value(), self.ui.coords_z.value())
        speed = Point(self.ui.speed_x.value(), self.ui.speed_y.value(), self.ui.speed_z.value())
        station_coords = Point(self.ui.station_coords_x.value(), self.ui.station_coords_y.value(), self.ui.station_coords_z.value())
        print(coords, speed, station_coords)
        self.ui.distance_label.setText(f'{abs(coords - station_coords):.3f}')
        self.ui.speed_label.setText(f'{abs(speed):.3f}')
        obj = Object(coords, speed)
        positions = obj.get_location_at_time(10)
        for i in positions:
            print(i)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
