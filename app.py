#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pymysql.cursors

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from dialogs import CommitWishDialog

class MainWindow(QWidget):

  rowCount = 0

  def __init__(self):

    super(MainWindow, self).__init__()

    self.db = pymysql.connect(host='localhost',
      user='root',
      password='Uzumymw98',
      db='test',
      charset='utf8',
      cursorclass=pymysql.cursors.DictCursor
    )

    self.cur = self.db.cursor()

    grid = QGridLayout()
    grid.setSpacing(10)

    addNewWishButton = QPushButton('Add new wish')
    addNewWishButton.clicked.connect(self.addNewWish)
    grid.addWidget(addNewWishButton, 0, 0)

    editSelectedWishButton = QPushButton('Edit wish')
    editSelectedWishButton.clicked.connect(self.editWish)
    grid.addWidget(editSelectedWishButton, 0, 1)

    deleteSelectedWishButton = QPushButton('Delete wish')
    deleteSelectedWishButton.clicked.connect(self.deleteWish)
    grid.addWidget(deleteSelectedWishButton, 0, 2)

    self.table = QTableWidget(self)
    self.table.setFocusPolicy(Qt.NoFocus)
    self.table.verticalHeader().hide()
    self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    self.columnNames = self.getColumnNames()
    self.table.setColumnCount(len(self.columnNames))
    self.table.setHorizontalHeaderLabels([name[0].upper() + name[1:] for name in self.columnNames])  

    header = self.table.horizontalHeader()
    for i in range(0, len(self.columnNames)):
      header.setSectionResizeMode(i, QHeaderView.Stretch)

    self.updateTable()
    grid.addWidget(self.table, 1, 0, 2, 0)

    self.setLayout(grid)
    self.setFixedSize(500, 250)
    self.setWindowTitle('Wish List')

  def handleException(self, exception):
    QMessageBox.critical(self, 'Error', str(exception))

  def addRow(self, wish, setRowCountFlag=False):
    if setRowCountFlag:
      self.table.setRowCount(self.rowCount + 1)
    for pos, columnName in enumerate(self.columnNames):
      self.table.setItem(self.rowCount, pos, QTableWidgetItem(str(wish[columnName])))
    self.rowCount += 1

  def clearTable(self):
    while self.rowCount > 0:
      self.table.removeRow(0)
      self.rowCount -= 1

  def updateTable(self):
    self.clearTable()
    wishes = self.getAllWishes()
    self.table.setRowCount(len(wishes))
    for wish in wishes:
      self.addRow(wish)

  def getColumnNames(self):
    columnNames = []
    self.cur.execute('SHOW COLUMNS FROM test.wishes')
    columns = self.cur.fetchall()
    for column in columns:
      columnNames.append(column['Field'])
    return columnNames

  def getAllWishes(self):
    self.cur.execute('SELECT * FROM wishes')
    return self.cur.fetchall()

  def getWishById(self, wishId):
    self.cur.execute('SELECT * FROM wishes WHERE id=\'%s\'' % wishId)
    wish = self.cur.fetchone()
    if wish:
      return wish
    else:
      raise Exception('No such wish id')

  def addNewWish(self):

    try:
      dialog = CommitWishDialog()
    except Exception as e:
      self.handleException(e)
      return

    if dialog.exec_() == QDialog.Accepted:

      wish = {
        'title': dialog.title.text(),
        'price': dialog.price.text(),
        'link': dialog.link.text(),
        'note': dialog.note.text()
      }

      self.cur.execute('INSERT INTO wishes (title, price, link, note) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')'
        % (wish['title'], wish['price'], wish['link'], wish['note']))
      self.db.commit()

      wish.update({'id': self.cur.lastrowid})
      self.addRow(wish, True)

  def editWish(self):

    wishId, ok = QInputDialog.getInt(self, '', 'Enter a wish id')

    if ok:

      try:
        wish = self.getWishById(wishId)
        dialog = CommitWishDialog(wish)
      except Exception as e:
        self.handleException(e)
        return

      if dialog.exec_() == QDialog.Accepted:

        editedWish = {
          'title': dialog.title.text(),
          'price': dialog.price.text(),
          'link': dialog.link.text(),
          'note': dialog.note.text()
        }

        self.cur.execute('UPDATE wishes SET title=\'%s\', price=\'%s\', link=\'%s\', note=\'%s\' WHERE id=\'%s\''
          % (editedWish['title'], editedWish['price'], editedWish['link'], editedWish['note'], wishId))
        self.db.commit()
        self.updateTable()

  def deleteWish(self):

    wishId, ok = QInputDialog.getInt(self, '', 'Enter a wish id')

    if ok:

      try:
        self.getWishById(wishId)
      except Exception as e:
        self.handleException(e)

      self.cur.execute('DELETE FROM wishes WHERE id=\'%s\'' % wishId)
      self.db.commit()
      self.updateTable()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
