from PyQt6 import QtWidgets
from gui import Ui_MainWindow
from backend.signal_simulation import simulate
import matplotlib.pyplot as plt
import matplotlib.figure
import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = dict()
        self.results = dict()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signal Simulation")
        self.ui.simulatePushButton.clicked.connect(lambda: self.Simulate())
        self.ui.actionSave.triggered.connect(lambda: self.SaveResults())
        self.ui.actionDrawScene.triggered.connect(lambda: self.DrawScene())

        self.scene = plt.figure(facecolor='lightblue')
        self.scene.canvas.manager.set_window_title('Simulation result')

    def Simulate(self):
        self.data = {
            "OBJ": {"COORD": (self.ui.obj_coords_x.value(), self.ui.obj_coords_y.value(), self.ui.obj_coords_z.value()),
                    "SPEED": (self.ui.obj_speed_x.value(), self.ui.obj_speed_y.value(), self.ui.obj_speed_z.value()),
                    "RADIUS": self.ui.obj_radius.value()}, "RLS": {"COORD": (
                self.ui.station_coords_x.value(), self.ui.station_coords_y.value(), self.ui.station_coords_z.value()),
                "DIRECTION": (self.ui.station_direction_x.value(), self.ui.station_direction_y.value(),
                              self.ui.station_direction_z.value()), "ENERGY": self.ui.station_energy.value(),
                "CRENERGY": self.ui.station_cr_energy.value(), "AMPL": self.ui.station_amplification.value()},
            "DISTORTION": self.ui.station_distortion.value(), "DT": self.ui.station_delta.value()}
        res = simulate(self.data)
        self.distance = res["MUFDIST"]
        self.speed = res["SPEED"]
        self.sigma = res["SIGMA"]
        self.wave_len = res["WAVEL"]
        self.fc = res["L"]
        self.coords = res["OBJCOORD"]
        print(4)
        self.ui.distance_label.setText(str(self.distance))
        self.ui.speed_label.setText(str(self.speed))
        '''
        TODO:
        считываем данные (DONE)
        отправляем данные(DONE)
        возвращаем данные(DONE)
        выводим данные(DONE)
        '''

    def SaveResults(self):
        if ("NULL" in (self.ui.distance_label.text(), self.ui.speed_label.text())):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Nothing to save. Please, make simulation.',
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok,
                                           defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            dist = self.ui.distance_label.text()
            vel = self.ui.speed_label.text()
            file = open('../results.txt', 'w')
            file.write(f'Distance:{dist} Speed:{vel}\n')
            file.close()
        '''
        сохраняем обработанные данные в файл(DONE)
        '''

    def DrawScene(self):
        if ("NULL" in (self.ui.distance_label.text(), self.ui.speed_label.text())):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Nothing to draw. Please, make simulation.',
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok,
                                           defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)
            return

        self.scene.clear()
        self.scene.set_size_inches(5, 5)
        self.obj_coords = self.data["OBJ"]["COORD"]

        axes = self.scene.add_subplot((0, 0.05, 1, 0.9), projection='3d', facecolor='lightblue')

        axes.cla()

        dist_rl_obj = np.array(list(self.obj_coords)) - np.array(list(self.data["RLS"]["COORD"]))

        real_dist = np.linalg.norm(dist_rl_obj)

        axes.plot([self.data["RLS"]["COORD"][0], self.obj_coords[0]],
                  [self.data["RLS"]["COORD"][1], self.obj_coords[1]],
                  [self.data["RLS"]["COORD"][2], self.obj_coords[2]])

        list_center = [self.obj_coords, self.data["RLS"]["COORD"], self.data["RLS"]["COORD"]]
        list_radius = [self.data["OBJ"]["RADIUS"], 1, real_dist]
        list_color = [('red', 0.8), ('green', 0.8), ('blue', 0.3)]
        names = ["OBJECT", "RLS", "DISTANCE"]

        min_, max_ = float("inf"), 0
        for name_, c, r, draw in zip(names, list_center, list_radius,
                                     list_color):
            # draw sphere.
            u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:20j]
            x = r * np.cos(u) * np.sin(v)
            y = r * np.sin(u) * np.sin(v)
            z = r * np.cos(v)
            min_ = min(np.amin(x), np.amin(y), np.amin(z),
                       min_)  # lowest number in the array
            max_ = max(np.amax(x), np.amax(y), np.amax(z),
                       max_)  # highest number in the array
            axes.plot_surface(c[0] - x, c[1] - y, c[2] - z, color=draw[0],
                              alpha=draw[1], label=name_)

        axes.text(
            self.data["RLS"]["COORD"][0], self.data["RLS"]["COORD"][1],
            self.data["RLS"]["COORD"][2],
            f"dist={round(real_dist, 3)}", size=15,
            zorder=5, zdir=(dist_rl_obj / np.linalg.norm(dist_rl_obj)),
            color="darkorange"
        )
        axes.set_xlim3d(min_, max_)
        axes.set_ylim3d(min_, max_)
        axes.set_zlim3d(min_, max_)
        axes.set_aspect("equal")
        axes.legend()

        self.scene.show()

    def closeEvent(self, a0):
        plt.close('all')
        a0.accept()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
