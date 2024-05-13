from PyQt6 import QtWidgets
from gui import Ui_MainWindow
from backend.simulation import simulate
import matplotlib.pyplot as plt
import matplotlib.figure
import numpy as np
import json


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
        self.ui.actionDraw_plots.triggered.connect(lambda: self.DrawPlots())
        self.ui.actionSave_values.triggered.connect(lambda: self.SaveValues())
        self.ui.actionOpen_values.triggered.connect(lambda: self.LoadValues())

        self.plots = plt.figure()
        self.scene = plt.figure(facecolor='lightblue')
        self.scene.canvas.manager.set_window_title('Simulation result')

    def SaveValues(self):
        self.data = {
            "OBJ": {"COORD": (self.ui.obj_coords_x.value(), self.ui.obj_coords_y.value(), self.ui.obj_coords_z.value()),
                    "SPEED": (self.ui.obj_speed_x.value(), self.ui.obj_speed_y.value(), self.ui.obj_speed_z.value()),
                    "RADIUS": self.ui.obj_radius.value()}, "RLS": {"COORD": (
                self.ui.station_coords_x.value(), self.ui.station_coords_y.value(), self.ui.station_coords_z.value()),
                "ENERGY": self.ui.station_energy.value(),
                "AMPL": self.ui.station_amplification.value()},
            "DISTORTION": self.ui.station_distortion.value() / 100, "DT": self.ui.station_delta.value(),
            "INPC": self.ui.impulse_count.value()}

        with open('../values.json', 'w') as save:
            json.dump(self.data, save)

    def LoadValues(self):
        try:
            with open('../values.json', 'r') as save:
                self.data = json.load(save)
            self.ui.obj_radius.setValue(float(self.data['OBJ']['RADIUS']))
            self.ui.obj_coords_x.setValue(float(self.data['OBJ']["COORD"][0]))
            self.ui.obj_coords_y.setValue(float(self.data['OBJ']["COORD"][1]))
            self.ui.obj_coords_z.setValue(float(self.data['OBJ']["COORD"][2]))
            self.ui.obj_speed_x.setValue(float(self.data["OBJ"]["SPEED"][0]))
            self.ui.obj_speed_y.setValue(float(self.data["OBJ"]["SPEED"][1]))
            self.ui.obj_speed_z.setValue(float(self.data["OBJ"]["SPEED"][2]))
            self.ui.station_coords_x.setValue(float(self.data["RLS"]["COORD"][0]))
            self.ui.station_coords_y.setValue(float(self.data["RLS"]["COORD"][1]))
            self.ui.station_coords_z.setValue(float(self.data["RLS"]["COORD"][2]))
            self.ui.station_energy.setValue(float(self.data["RLS"]["ENERGY"]))
            self.ui.station_amplification.setValue(float(self.data["RLS"]["AMPL"]))
            self.ui.station_distortion.setValue(float(self.data["DISTORTION"]))
            self.ui.station_delta.setValue(float(self.data["DT"]))
            self.ui.impulse_count.setValue(int(self.data["INPC"]))
        except:
            return

    def Simulate(self):
        self.data = {
            "OBJ": {"COORD": (self.ui.obj_coords_x.value(), self.ui.obj_coords_y.value(), self.ui.obj_coords_z.value()),
                    "SPEED": (self.ui.obj_speed_x.value(), self.ui.obj_speed_y.value(), self.ui.obj_speed_z.value()),
                    "RADIUS": self.ui.obj_radius.value()}, "RLS": {"COORD": (
                self.ui.station_coords_x.value(), self.ui.station_coords_y.value(), self.ui.station_coords_z.value()),
                "ENERGY": self.ui.station_energy.value(),
                "AMPL": self.ui.station_amplification.value()},
            "DISTORTION": self.ui.station_distortion.value() / 100, "DT": self.ui.station_delta.value(),
            "INPC": self.ui.impulse_count.value()}
        try:
            res = simulate(self.data)
        except:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Something went wrong. Please, put different values.',
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok,
                                           defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.results = res
        self.distance = res["MUFDIST"]
        self.speed = res["SPEED"]
        self.sigma = res["SIGMA"]
        self.wave_len = res["WAVEL"]
        self.fc = res["L"]
        self.coords = res["OBJCOORD"]
        if np.isnan(self.distance) or np.isnan(self.speed):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Something went wrong. Please, put different values.',
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok,
                                           defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            self.ui.distance_label.setText(f'{self.distance:.3f}')
            self.ui.speed_label.setText(f'{self.speed:.3f}')

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

        real_dist = self.results["MUFDIST"]
        axes.plot([self.data["RLS"]["COORD"][0], self.obj_coords[0]],
                  [self.data["RLS"]["COORD"][1], self.obj_coords[1]],
                  [self.data["RLS"]["COORD"][2], self.obj_coords[2]])

        list_center = [self.obj_coords, self.data["RLS"]["COORD"], self.data["RLS"]["COORD"]]
        list_radius = [self.data["OBJ"]["RADIUS"], 1, real_dist]
        list_color = [('red', 0.8), ('green', 0.8), ('blue', 0.1)]
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
            f"distance={round(float(real_dist), 3)}", size=15,
            zorder=5, zdir=(list(dist_rl_obj / np.linalg.norm(dist_rl_obj))),
            color="darkorange"
        )
        print(8)
        axes.set_xlim3d(min_, max_)
        axes.set_ylim3d(min_, max_)
        axes.set_zlim3d(min_, max_)
        axes.set_aspect("equal")
        axes.legend()

        self.scene.show()

    def closeEvent(self, a0):
        plt.close('all')
        message = QtWidgets.QMessageBox.question(self, 'Save values', 'Do you want to save values?', (
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No),
                                                 QtWidgets.QMessageBox.StandardButton.Yes)
        if message == QtWidgets.QMessageBox.StandardButton.Yes:
            self.SaveValues()
        a0.accept()

    def DrawPlots(self):
        if ("NULL" in (self.ui.distance_label.text(), self.ui.speed_label.text())):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Nothing to draw. Please, make simulation.',
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok,
                                           defaultButton=QtWidgets.QMessageBox.StandardButton.Ok)
            return

        plt.close(self.plots)
        self.plots.clear()
        grafics = self.results["PREDICT"]

        self.plots, axes = plt.subplots()
        self.plots.canvas.manager.set_window_title('Plot')
        axes.plot(grafics[0], grafics[1])
        axes.set_title('Prediction Accuracy(Noise)')
        axes.set_xlabel('Noise(%)')
        axes.set_ylabel('Accuracy(%)')
        self.plots.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
