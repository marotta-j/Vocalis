import sys
import os
from vocalis_main import Vocalis
from playsound import playsound
import multiprocessing
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QTimer, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# GUI file
from ui_mainwindow import Ui_MainWindow

# Import functions
from ui_functions import *

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.v = Vocalis() # define the Vocalis function so we can use it

		def moveWindow(event): # moving the window around
			if UIFunctions.returnStatus(self) == 1:
				UIFunctions.maximize_restore(self)
			if event.buttons() == Qt.LeftButton:
				self.move(self.pos() + event.globalPos() - self.dragPos)
				self.dragPos = event.globalPos()
				event.accept()

		self.ui.title_bar.mouseMoveEvent = moveWindow

		# Set UI definitions
		UIFunctions.uiDefinitions(self)

		self.show()

	def start_animation(self, text): # Begin the cool text animation
		self.ui.label.setText('') # erase whats on the screen
		self.text = text
		self.words = self.text.split() # split the response up into words
		self.i = 0

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.animate_text)
		self.timer.start(250)  # set the timer interval to 500ms (0.5 seconds)

	def animate_text(self):
		if self.i >= len(self.words):
			self.timer.stop()
			self.ui.label.setText(self.text)  # display the full sentence
			return

		current_word = self.words[self.i] # go through this list and add word by word
		self.i += 1
		self.ui.label.setText(self.ui.label.text() + " " + current_word) # add the curent word

	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()

if __name__ == "__main__": # run the code
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())
