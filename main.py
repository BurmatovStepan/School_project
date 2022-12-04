import os
import sys
import shutil
import requests
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


def icon_check():
    if not os.path.isfile(os.path.join(os.getcwd(), 'icon.png')):
        image = requests.get('https://lh5.ggpht.com/Iy2SF6C-E54bW_AwwPfymQ__MqQgx_iPRnVjvsgI0BbXA3FFiJDU6R6EcqXAZQ9iviRT=w170').content
        with open('icon.png', 'wb') as icon:
            icon.write(image)


def sort_dir(sort_here, new_dirs_here, del_sorted_folder):
    if os.path.isdir(sort_here):
        for step in os.walk(sort_here):
            for file in step[2]:
                type = file.split('.')[-1]
                if not os.path.isdir(os.path.join(new_dirs_here, type)):
                    os.makedirs(os.path.join(new_dirs_here, type))
                if del_sorted_folder:
                    os.rename(os.path.join(step[0], file), os.path.join(new_dirs_here, type, file))
                else:
                    shutil.copyfile(os.path.join(step[0], file), os.path.join(new_dirs_here, type, file))
        if del_sorted_folder:
            shutil.rmtree(sort_here)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('sorter.ui', self)
        self.setWindowTitle('Folder sorter')
        icon_check()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.sort_this.setText(os.getcwd())
        self.new_dirs_here.setVisible(0)
        self.run.clicked.connect(self.start_sort)
        self.custom_folder.toggled.connect(self.show_custom_way)

    def start_sort(self):
        sort_this = self.sort_this.text()
        if self.where_folder.isChecked():
            new_dirs_here = os.path.dirname(sort_this)
        if self.prg_folder.isChecked():
            new_dirs_here = os.getcwd()
        if self.custom_folder.isChecked():
            new_dirs_here = self.new_dirs_here.text()
        del_sorted_folder = self.del_cb.isChecked()
        sort_dir(sort_this, new_dirs_here, del_sorted_folder)

    def show_custom_way(self, value):
        self.new_dirs_here.setVisible(value)


program_work = True
if __name__ == '__main__':
    app = QApplication(sys.argv)
    while program_work:
        try:
            window = Window()
            window.show()
            sys.exit(app.exec())
        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(str(ex) + '\n\n' + 'Попробовать запустить программу ещё раз?')
            msg.setWindowTitle('Ошибка')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            value = msg.exec()

            if value == QMessageBox.No:
                program_work = False