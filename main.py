import sys
from PyQt5 import QtWidgets,QtGui,QtCore
import ui_main,ui_vh
from PyQt5.QtCore import QThread, pyqtSignal
from threads import hDialogdb,arpsniff
##########
arpsniffModule = arpsniff()
###########
class currpacDialog(QtWidgets.QDialog,ui_vh.Ui_Dialog):
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Dialog", "Recieved packets"))
		# self.populate_table()
		# self.Refresh.clicked.connect(self.populate_table)
		arpsniffModule.signal.connect(self.add_entries)
	def add_entries(self,model):
		self.tableView.setModel(model)


######Valid hosts dialog box###########
class vhDialog(QtWidgets.QDialog,ui_vh.Ui_Dialog):
	# signal = pyqtSignal(QtGui.QStandardItemModel)
	dbthread=hDialogdb(0)
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		self.populate_table()
		self.Refresh.clicked.connect(self.populate_table)
		self.dbthread.signal.connect(self.add_entries)
		self.tableView.resizeColumnsToContents()
	def populate_table(self):
		self.dbthread.start()

	def add_entries(self,model):
		self.tableView.setModel(model)
		# self.dbthread.exit

######InValid hosts dialog box###########
class ivhDialog(QtWidgets.QDialog,ui_vh.Ui_Dialog):
	dbthread=hDialogdb(1)
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Dialog", "Invalid Hosts"))
		self.populate_table()
		self.Refresh.clicked.connect(self.populate_table)
		self.dbthread.signal.connect(self.add_entries)
	def populate_table(self):
		self.dbthread.start()
	def add_entries(self,model):
		self.tableView.setModel(model)
		# self.dbthread.exit
#########Main ui###############
class App(QtWidgets.QMainWindow,ui_main.Ui_MainWindow):
	def __init__(self,parent=None):
		super(self.__class__,self).__init__(parent)
		self.setupUi(self)
		self.vhbutton.clicked.connect(self.show_vhD)
		self.ihbutton.clicked.connect(self.show_ivhD)
		self.startDetect.clicked.connect(self.startDetectfunc)
		self.stopDetect.clicked.connect(self.stopDetectfunc)
		self.currpac.clicked.connect(self.currpacf)

	def currpacf(self):
		self.currpacDialog = currpacDialog()
		self.currpacDialog.show()
		#QtWidgets.QMessageBox.critical(self, "No subreddits",
        #                               "You didn't enter any subreddits.",
        #                               QtWidgets.QMessageBox.Ok)

	def show_vhD(self):
		self.validHostsDialog = vhDialog()
		self.validHostsDialog.show()

	def show_ivhD(self):
		self.validHostsDialog = ivhDialog()
		self.validHostsDialog.show()

	def startDetectfunc(self):
		_translate = QtCore.QCoreApplication.translate
		self.vhbutton.setEnabled(True)
		self.stopDetect.setEnabled(True)
		self.ihbutton.setEnabled(True)
		self.currpac.setEnabled(True)
		self.startDetect.setEnabled(False)
		self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Status : </span><span style=\" font-weight:600; color:#008000;\">Listening</span></p></body></html>"))
		arpsniffModule.start();

	def stopDetectfunc(self):
		_translate = QtCore.QCoreApplication.translate
		self.vhbutton.setEnabled(False)
		self.stopDetect.setEnabled(False)
		self.ihbutton.setEnabled(False)
		self.currpac.setEnabled(False)
		self.startDetect.setEnabled(True)
		self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Status : </span><span style=\" font-weight:600; color:#ef2929;\">Not Listening</span></p></body></html>"))
		arpsniffModule.exit()
####### opens main ui ##########
def main():
	app = QtWidgets.QApplication(sys.argv)
	form = App()
	form.show()
	app.exec_()
######opens main function########:p
if __name__ == '__main__':
	main()
