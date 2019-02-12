from PyQt5.QtWidgets import *

class CommitWishDialog(QDialog):

  rowCount = 0

  def __init__(self, wish=None):

    super().__init__()

    self.grid = QGridLayout()
    self.grid.setSpacing(10)

    self.title = QLineEdit(wish['title'] if wish else '')
    self.addRow('Title', self.title)

    self.price = QLineEdit(str(wish['price']) if wish else '')
    self.addRow('Price', self.price)

    self.link = QLineEdit(wish['link'] if wish else '')
    self.addRow('Link', self.link)

    self.note = QLineEdit(wish['note'] if wish else '')
    self.addRow('Note', self.note)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.accepted.connect(self.accept)
    buttonBox.rejected.connect(self.reject)
    self.grid.addWidget(buttonBox, self.rowCount, 0, 1, 0)

    self.setFixedSize(250, 0)
    self.setLayout(self.grid)
    self.setWindowTitle('Commit wish')

  def addRow(self, name, lineEdit):
    self.grid.addWidget(QLabel(name), self.rowCount, 0)
    self.grid.addWidget(lineEdit, self.rowCount, 1)
    self.rowCount += 1

  def isPrice(self, price):
    try:
      float(price)
      return True
    except ValueError:
      return False

  def accept(self):
    try:
      if self.title.text() and self.price.text() and self.link.text() and self.note.text():
        if self.isPrice(self.price.text()):
          super().accept()
        else:
          raise Exception('Price isn\'t numeric')
      else:
        raise Exception('Some fields are empty')
    except Exception as e:
      QMessageBox.critical(self, 'Error', str(e))
