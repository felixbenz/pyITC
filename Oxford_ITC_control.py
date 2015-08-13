# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:01:16 2015

@author: Felix Benz (fb400)
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Oxford_ITC import *
import ITC_widget
import sys
import time
import threading

class ITC_GUI(QWidget, ITC_widget.Ui_OxfordITC):
    def __init__(self,parent=None):
        super(ITC_GUI,self).__init__(parent)
        self.setupUi(self)
        self.current_temperature = 273
        self.ITC = OxfordITC()
        self.setupSignals()
        self.setupGUI()
        
        
        
    def setupSignals(self):
        self.btn_open_connection.clicked.connect(self._btn_open_connection)
        self.btn_close_connection.clicked.connect(self._btn_close_connection)
        self.btn_read_temp.clicked.connect(self._btn_read_temp)
        
        self.spin_set_temp.valueChanged.connect(self._spin_set_temp)
        self.spin_man_heat.valueChanged.connect(self._spin_man_heat)
        
        self.check_live_temp.stateChanged.connect(self._check_live_temp)
        self.check_auto_heat.stateChanged.connect(self._check_auto_heat)
        self.check_auto_PID.stateChanged.connect(self._check_auto_PID)

    def setupGUI(self):
        self.btn_close_connection.setEnabled(False) 
        self.btn_read_temp.setEnabled(False)
        
        self.spin_set_temp.setEnabled(False)
        self.spin_man_heat.setEnabled(False)
        
        self.check_live_temp.setEnabled(False)
        self.check_auto_heat.setEnabled(False)
        self.check_auto_PID.setEnabled(False)       
        
        
    def _btn_open_connection(self):
        self.ITC.open_connection()
        self.btn_open_connection.setEnabled(False) 
        self.btn_close_connection.setEnabled(True) 
        self.btn_read_temp.setEnabled(True)
        
        self.spin_set_temp.setEnabled(True)
        self.spin_man_heat.setEnabled(True)
        
        self.check_live_temp.setEnabled(True)
        self.check_auto_heat.setEnabled(True)
        self.check_auto_PID.setEnabled(True)
        
    def _btn_close_connection(self):
        if(self.check_live_temp.isChecked()):
            self.check_live_temp.setChecked(False)
            
        self.btn_open_connection.setEnabled(True) 
        self.btn_close_connection.setEnabled(False) 
        self.btn_read_temp.setEnabled(False)
        
        self.spin_set_temp.setEnabled(False)
        self.spin_man_heat.setEnabled(False)
        
        self.check_live_temp.setEnabled(False)
        self.check_auto_heat.setEnabled(False)
        self.check_auto_PID.setEnabled(False)
        self.ITC.close_connection()
        
    def _btn_read_temp(self):
        self.cur_temperature = self.ITC.getTemperature()
        self.disp_current_temp.setNum(self.cur_temperature)
        
    def _spin_set_temp(self):
        self.ITC.setSetTemperature(self.spin_set_temp.value())
    
    def _spin_man_heat(self):
        self.ITC.setHeaterPower(self.spin_man_heat.value())
        
    def _check_live_temp(self):
        if(self.check_live_temp.isChecked()):
            try:
                self._live_temp_stop_event = threading.Event()
                self._live_temp_thread = threading.Thread(target=self._live_temperature_function)
                self._live_temp_thread.start()
            except AttributeError as e: #if any of the attributes aren't there
                print "Error:", e
        else:
            print "stopping live view thread"
            try:
                self._live_temp_stop_event.set()
                self._live_temp_thread.join()
                del(self._live_temp_stop_event, self._live_temp_thread)
            except AttributeError:
                raise Exception("Tried to stop live view but it doesn't appear to be running!")
                
    def _live_temperature_function(self):
        """this function should only EVER be executed by _check_live_temp."""
        while not self._live_temp_stop_event.wait(timeout=0.1):
            self.cur_temperature = self.ITC.getTemperature()
            self.disp_current_temp.setNum(self.cur_temperature)
            time.sleep(0.5)
        
    def _check_auto_heat(self):
        if(self.check_auto_heat.isChecked()):
            self.ITC.setHeaterMode(1)
        else:
            self.ITC.setHeaterMode(0)
            
        
    def _check_auto_PID(self):
        if(self.check_auto_PID.isChecked()):
            self.ITC.setAutoPID(1)
        else:
            self.ITC.setAutoPID(0)
            
    def closeEvent(self, event):
        if(self.check_live_temp.isChecked()):
            self.check_live_temp.setChecked(False)
        self.ITC.close_connection()
        event.accept()
        
            
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    

    ITCControlWindow = ITC_GUI()

    ITCControlWindow.show()
    sys.exit(app.exec_())
    
    try:
        from IPython.lib.guisupport import start_event_loop_qt4
        start_event_loop_qt4(app)
    except ImportError:
        app.exec_()     
        