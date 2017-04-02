import sys,socket,os
from PyQt5 import QtWidgets,QtGui,QtCore
import ui_main,ui_vh
from PyQt5.QtCore import QThread, pyqtSignal
from threads import hDialogdb,arpsniff
######Valid hosts dialog box###########
class vhDialog(QtWidgets.QDialog,ui_vh.Ui_Dialog):
	#Initialize database object with 0 as parameter to specify fetching of valid host entries
	dbthread=hDialogdb(0)
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		self.populate_table()
		self.Refresh.clicked.connect(self.populate_table)
		self.dbthread.signal.connect(self.add_entries)
		self.header = self.tableView.horizontalHeader()
		self.header.ResizeMode(3)
		self.header.setStretchLastSection(True)
	def populate_table(self):
		self.dbthread.start()

	def add_entries(self,model):
		self.tableView.setModel(model)
		self.dbthread.stop

######InValid hosts dialog box###########
class ivhDialog(QtWidgets.QDialog,ui_vh.Ui_Dialog):
	#Initialize database object with 1 as parameter to specify fetching of detected atttackers entries
	dbthread=hDialogdb(1)
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Dialog", "Attackers log"))
		self.populate_table()#start db thread to fetch data
		self.Refresh.clicked.connect(self.populate_table)
		self.dbthread.signal.connect(self.add_entries)#data recieved from db thread as signal to main thread whenever the signal is transmitted refresh
		self.header = self.tableView.horizontalHeader()
		self.header.ResizeMode(3)
		self.header.setStretchLastSection(True)

	def populate_table(self):
		self.dbthread.start()
	def add_entries(self,model):
		self.tableView.setModel(model)
		self.dbthread.stop
#########Main ui###############
class App(QtWidgets.QMainWindow,ui_main.Ui_MainWindow):
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		# self.arpsniffModule = arpsniff()
		try:
			socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
		except Exception as e:
			print "Root privilages required !\n"
			os.system("sudo python "+ __file__)
			sys.exit(1)

		self.vhbutton.clicked.connect(self.show_vhD)
		self.ihbutton.clicked.connect(self.show_ivhD)
		self.startDetect.clicked.connect(self.startDetectfunc)
		self.tableView.setHidden(True)
		self.header = self.tableView.horizontalHeader()
		self.header.ResizeMode(3)
		self.header.setStretchLastSection(True)
		self.label_3.setHidden(True)
		self.startDetect.setFocus()
		# self.startDetect.returnPressed.connect(self.startDetect)
		# self.stopDetect.clicked.connect(self.stopDetectfunc)
		# self.currpac.clicked.connect(self.currpacf)
		try:
			self.arpsniffModule = arpsniff()
		except Exception as e:
			QtWidgets.QMessageBox.critical(self, "Network Error",
										   "Well, this is embarrassing.\n"+str(e),
											   QtWidgets.QMessageBox.Cancel,
											#  QtWidgets.QPushButton("Exit").clicked.connect()
											   )
			self.__init__()
		self.arpsniffModule.spoofDetectedSignal.connect(self.spoofBox)
		self.arpsniffModule.modelUpdateSignal.connect(self.add_entries)

	def add_entries(self,model):
		self.tableView.setModel(model)

	def currpacf(self):
		self.currpacDialog = currpacDialog()
		self.currpacDialog.show()

	def spoofBox(self,src_ip):
		QtWidgets.QMessageBox.critical(self, "Spoof Detected",
									   "IP "+src_ip+" is spoofed!\nCheck attckers log for more info.",
									   QtWidgets.QMessageBox.Ok)
	def show_vhD(self):
		self.validHostsDialog = vhDialog()
		self.validHostsDialog.show()

	def show_ivhD(self):
		self.validHostsDialog = ivhDialog()
		self.validHostsDialog.show()

	def startDetectfunc(self):
		_translate = QtCore.QCoreApplication.translate
		self.vhbutton.setEnabled(True)
		# self.stopDetect.setEnabled(True)
		self.ihbutton.setEnabled(True)
		self.tableView.setHidden(False)
		self.label_3.setHidden(False)
		# self.currpac.setEnabled(True)
		# self.startDetect.setEnabled(False)
		self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Status : </span><span style=\" font-weight:600; color:#008000;\">Listening</span></p></body></html>"))
		try:
			self.arpsniffModule.start();
		except Exception as e:
			QtWidgets.QMessageBox.critical(self, "Error",
	                                       "Exception occured in creating listner thread.\n"+str(e) ,
	                                       QtWidgets.QMessageBox.Ok)
			self.startDetect.setText(_translate("MainWindow", "Start Detection"))
			self.startDetect.setStyleSheet("background-color: rgb(115, 210, 22);\n"
	"color: rgb(0, 0, 0);\n"
	"\n"
	"")
			self.startDetect.clicked.connect(self.startDetectfunc)
			return
		self.startDetect.setText(_translate("MainWindow", "Stop Detection"))
		self.startDetect.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(0, 0, 0);\n"
"\n"
"")
		self.startDetect.clicked.connect(self.stopDetectfunc)


	def stopDetectfunc(self):
		_translate = QtCore.QCoreApplication.translate
		self.vhbutton.setEnabled(False)
		# self.stopDetect.setEnabled(False)
		self.ihbutton.setEnabled(False)
		# self.currpac.setEnabled(False)
		# self.startDetect.setEnabled(True)
		self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Status : </span><span style=\" font-weight:600; color:#ef2929;\">Not Listening</span></p></body></html>"))
		try:
			self.arpsniffModule.__del__()
		except Exception as e:
			QtWidgets.QMessageBox.critical(self, "Error",
	                                       "Error Stoping sniffer thread.\n"+str(e),
	                                       QtWidgets.QMessageBox.Ok)
		self.startDetect.setText(_translate("MainWindow", "Start Detection"))
		self.startDetect.setStyleSheet("background-color: rgb(115, 210, 22);\n"
"color: rgb(0, 0, 0);\n"
"\n"
"")
		self.startDetect.clicked.connect(self.startDetectfunc)
####### opens main ui ##########
def main():
	app = QtWidgets.QApplication(sys.argv)
	form = App()
	form.show()
	app.exec_()
######opens main function########:p
if __name__ == '__main__':
	main()
