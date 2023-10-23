from main import *
global_state = 0

class UIFunctions(MainWindow):
	def maximize_restore(self): # maximize the window
		global global_state
		status = global_state

		if status == 0:
			self.showMaximized()

			global_state = 1

			# IF MAXIMIZED REMOVE MARGINS AND BORDER RADIUS
			self.ui.drop_shadow_layout.setContentsMargins(0, 0, 0, 0)
			self.ui.drop_shadow_frame.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(19, 33, 212, 255), stop:0.0170455 rgba(23, 37, 212, 255), stop:1 rgba(172, 7, 246, 255));\n"
"border-radius: 10px;") # reset the style sheet
			self.ui.btn_maximize.setToolTip("Restore")

		else: # minimize !!
			global_state = 0
			self.showNormal()
			self.resize(self.width()+1, self.height()+1)
			self.ui.drop_shadow_layout.setContentsMargins(10,10,10,10)
			self.ui.drop_shadow_frame.setStyleSheet(
				u"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(19, 33, 212, 255), stop:0.0170455 rgba(23, 37, 212, 255), stop:1 rgba(172, 7, 246, 255));\n"
				"border-radius: 10px;")
			self.ui.btn_maximize.setToolTip("Maximize")

	def get_user_input(self): # What happens when you press the button
		try:
			self.p.terminate() # try to stop the playsound process if it is running
		except Exception:
			pass
		self.ui.label.setText('Listening...') # write listening on the screen
		self.ui.label.show()
		self.repaint()
		QCoreApplication.processEvents() # need to force "Listening..." on the screen before we actually listen

		response = self.v.create_response(self.v.listen_and_decode()) # go to vocalis_main.py and get response

		UIFunctions.start_animation(self, response)
		self.p = multiprocessing.Process(target=playsound, args=("audio.mp3",)) # play the mp3 file that was generated
		self.p.start() # use multiprocessing so the sound doesn't interrupt the execution of the main loop

	def uiDefinitions(self):
		# Remove Windows Title bar and make transparent
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		# Drop Shadow (looks real nice)
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(20)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 100))

		# apply dropshadow to frame
		self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)

		# Size grip (you can resize the GUI in the bottom left corner)
		self.sizegrip = QSizeGrip(self.ui.frame_grip)
		self.sizegrip.setStyleSheet("QSizeGrip { width: 10px; height: 10px; margin: 5px } QSizeGrip:hover {background-color: rgb(50,42,94) }")
		self.sizegrip.setToolTip("Resize Window")

		# Connect all the buttons ------------

		# Maximize / Restore
		self.ui.btn_maximize.clicked.connect(lambda: UIFunctions.maximize_restore(self))
		self.ui.btn_minimize.clicked.connect(lambda: UIFunctions.showMinimized(self))
		self.ui.btn_close.clicked.connect(lambda: self.close())

		# Press to talk button
		self.ui.pushButton.clicked.connect(lambda: UIFunctions.get_user_input(self))


	def returnStatus(self):
		return global_state
