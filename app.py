#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pymysql.cursors

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class AddNewWishDialog(QDialog):

  def __init__(self):

    super().__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(QLabel('Title'), 0, 0)
    self.title = QLineEdit()
    grid.addWidget(self.title, 0, 1)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    self.grid.addWidget(buttonBox, 1, 0)

    self.setFixedSize(250, 0)
    self.setLayout(grid)

class MainWindow(QWidget):

  title = 'Wish List'

  def __init__(self):

    super(MainWindow, self).__init__()

    self.db = pymysql.connect(host='localhost',
      user='root',
      password='password',
      db='db',
      charset='utf8',
      cursorclass=pymysql.cursors.DictCursor)

    grid = QGridLayout()
    grid.setSpacing(10)

    addNewWishButton = QPushButton('Add new wish')
    addNewWishButton.clicked.connect(self.addNewWish)
    grid.addWidget(addNewWishButton, 0, 0)

    table = QTableWidget(self)

    labels = ['Title', 'Price', 'Link', 'Note']
    table.setColumnCount(len(labels))
    table.setHorizontalHeaderLabels(labels)

    wishes = self.getAllWishes()
    table.setRowCount(len(wishes))

    for i in range(0, len(wishes)):
      for j in range(0, len(labels)):
        table.setItem(i, j, QTableWidgetItem(wishes[i][j]))

    table.resizeColumnsToContents()
    grid.addWidget(table, 1, 0)

    self.setLayout(grid)
    self.setFixedSize(400, 200)
    self.setWindowTitle(self.title)

  def addNewWish(self):
    dialog = AddNewWishDialog()
    if dialog.exec_() == QDialog.Accepted:
      print('Title: %s' % dialog.title.text())
      # with self.db.cursor() as cursor:
      #   cursor.execute('INSERT INTO wishes (title, price, link, note) VALUES (%s, %s, %s, %s)')
      #   self.db.commit()

  def getAllWishes(self):
    with connection.cursor() as cursor:
      cursor.execute('SELECT * FROM wishes')
      return cursor.fetchall()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
