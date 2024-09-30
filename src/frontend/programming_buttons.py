import backend.core.variables as v
import tkinter.messagebox
import os
import time
import tkinter as tk
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QImage, QPixmap, QIcon, QMovie
from PyQt5.QtWidgets import QPushButton, QFrame, QComboBox, QLineEdit, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5 import  QtGui
from PyQt5 import QtCore

from backend.robot import robot_var as RV

class FunctionsProgrammingButtons:
    def __init__(self, program_text, program_name):
        self.program_text = program_text
        self.program_name = program_name

    def MoveL(self):
        fields = ["X", "Y", "Z", "y", "p", "r", "speed", "acceleration"]  
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"MoveL X{val[0]} Y{val[1]} Z{val[2]} y{val[3]} p{val[4]} r{val[5]} s{val[6]} a{val[7]}"
            self.insert_new_line(line)
        except:
            pass

    def MoveJ(self):
        fields = ["X", "Y", "Z", "y", "p", "r", "speed", "acceleration"]  
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"MoveJ X{val[0]} Y{val[1]} Z{val[2]} y{val[3]} p{val[4]} r{val[5]} s{val[6]} a{val[7]}"
            self.insert_new_line(line)
        except:
            pass

    def TeachMoveL(self):
        if v.SIM == 1:
            line = f"robot.MoveJ(pos = [{round(RV.POS_AXIS_SIM[0],1)}, {round(RV.POS_AXIS_SIM[1],1)}, {round(RV.POS_AXIS_SIM[2],1)}, {round(RV.POS_AXIS_SIM[3],1)}, {round(RV.POS_AXIS_SIM[4],1)}, {round(RV.POS_AXIS_SIM[5],1)}], v = {v.SPEED}, a = {v.ACCEL})"
        else:
            line = f"robot.MoveL(pos = [{round(RV.POS_AXIS[0],1)}, {round(RV.POS_AXIS[1],1)}, {round(RV.POS_AXIS[2],1)}, {round(RV.POS_AXIS[3],1)}, {round(RV.POS_AXIS[4],1)}, {round(RV.POS_AXIS[5],1)}], v = {v.SPEED} a = {v.ACCEL}"
        self.insert_new_line(line)

    def TeachMoveJ(self):
        if v.SIM == 1:
            line = f"robot.MoveJ(pos = [{round(RV.POS_AXIS_SIM[0],1)}, {round(RV.POS_AXIS_SIM[1],1)}, {round(RV.POS_AXIS_SIM[2],1)}, {round(RV.POS_AXIS_SIM[3],1)}, {round(RV.POS_AXIS_SIM[4],1)}, {round(RV.POS_AXIS_SIM[5],1)}], v = {v.SPEED}, a = {v.ACCEL})"
        else:
            line = f"robot.MoveL(pos = [{round(RV.POS_AXIS[0],1)}, {round(RV.POS_AXIS[1],1)}, {round(RV.POS_AXIS[2],1)}, {round(v.POS_AXIS[3],1)}, {round(RV.POS_AXIS[4],1)}, {round(RV.POS_AXIS[5],1)}], v = {v.SPEED} a = {v.ACCEL}"
        self.insert_new_line(line)

    def OffsetL(self):
        fields = ["X", "Y", "Z", "y", "p", "r", "speed", "acceleration"]  
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"OffsetL X{val[0]} Y{val[1]} Z{val[2]} y{val[3]} p{val[4]} r{val[5]} s{val[6]} a{val[7]}"
            self.insert_new_line(line)
        except:
            pass

    def OffsetJ(self):
        fields = ["X", "Y", "Z", "y", "p", "r", "speed", "acceleration"]  
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"OffsetJ X{val[0]} Y{val[1]} Z{val[2]} y{val[3]} p{val[4]} r{val[5]} s{val[6]} a{val[7]}"
            self.insert_new_line(line)
        except:
            pass

    def Delay(self):
        fields = ["delay"]
        dialog = MultiInputDialog("Fill in the delay", fields)
        dialog.exec_()
        try:          
            val = dialog.returnValue()
            line = f"Delay {val[0]}"
            self.insert_new_line(line)
        except:
            pass

    def Home(self):
        self.insert_new_line("Home")

    def Gripper(self):
        fields = ["Pos", "speed"] 
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"Gripper G{val[0]} s{val[1]}"
            self.insert_new_line(line)
        except:
            pass

    def ForLoop(self):
        fields = ["X", "Y", "Z", "y", "p", "r", "speed", "acceleration"]  
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"int {val[0]} = {val[1]}"
            self.insert_new_line(line)
        except:
            pass

    def Var(self):
        fields = ["Variable name", "Variable value"]
        dialog = MultiInputDialog("Fill in the coordinates", fields)
        dialog.exec_()
        try:
            val = dialog.returnValue()
            line = f"int {val[0]} = {val[1]}"
            self.insert_new_line(line)
        except:
            pass
             
    def GCode(self):
        self.insert_new_line("Run Gcode")
    
    def Origin(self):
        origin = OriginwindowProgram()
        origin.exec_()
        try:
            val = origin.returnValue()
            line = f"origin X{val[0]} Y{val[0]} Z{val[0]}"
            self.insert_new_line(line)
        except:
            pass
    
    def Connect4(self):
        pass
                
    def insert_new_line(self, new_line):
        cursor = self.program_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"\n{new_line}")
        self.program_text.setTextCursor(cursor)
        
class OriginwindowProgram(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("origin")
        self.setWindowIcon(QIcon('mikobot.ico'))
         
        layout1 = QGridLayout()
        self.setLayout(layout1)
        
        frame = QFrame()
        layout1.addWidget(frame, 0, 0)
        layout = QGridLayout()
        frame.setLayout(layout)
        
        self.setStyleSheet(
            "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
            "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
            "QPushButton:hover { background-color: white; }"
            "QPushButton:pressed { background-color: darkorange; }"+
            "QCheckBox {  background-color: white; }"+
            "QLabel {font-size: 12px; font-family: Arial;}"+
            "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
            )        
        
        
        
        origins = []
        for i in range(len(RV.ORIGIN)):
            print(RV.ORIGIN[i][0])
            origins.append(RV.ORIGIN[i][0])
            
        name = ["X", "Y", "Z"]  
        labels = []
        for i in range(3):
            label = QLabel(f"{name[i]}:")
            layout.addWidget(label, 1 + i, 0)
            labels.append(label)
            
        def on_combobox_change(index):
            selected_value = self.combo.currentText()
            if selected_value:
                for i in range(3):
                    labels[i].setText("test")
            
            
        self.fields = ["X", "Y", "Z"]
        self.entries =[]
        self.combo = QComboBox()
        self.combo.addItems(origins)
        self.combo.currentIndexChanged.connect(on_combobox_change)
        self.combo.setStyleSheet("background-color: " + "white")
        self.combo.setStyleSheet("QComboBox {text-align: center;}")
        self.combo.setMaximumWidth(80)
        layout.addWidget(self.combo,1,1,3,1)


        title = QLabel("custom origin")
        title.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        title.setMaximumHeight(20)
        layout.addWidget(title, 4, 0, 1, 2)

        for i in range(len(self.fields)):
            label = QLabel(f"{self.fields[i]}:")
            layout.addWidget(label, 6 + i, 0)
            entry = QLineEdit()
            entry.setText('0')
            layout.addWidget(entry, 6 + i, 1)
            self.entries.append(entry)       

            
        # Create a button to close the window
        self.cancel_button = QPushButton('Cancel', self)
        layout.addWidget(self.cancel_button,layout.rowCount(), 0)
        self.cancel_button.clicked.connect(self.accept)
        
        self.close_button = QPushButton('Ok', self)
        layout.addWidget(self.close_button,layout.rowCount(), 0)
        self.close_button.clicked.connect(self.get_values)
        
    def get_values(self):
        self.result = [0] * len(self.fields)
        for i in range(len(self.fields)):
            self.result[i] = self.entries[i].text()
        self.accept()
        
    def returnValue(self):
        return self.result
        
class MultiInputDialog(QDialog):
    def __init__(self, name ,fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(name)
        self.setWindowIcon(QtGui.QIcon('mikobot.ico'))
         
        layout = QGridLayout()
        self.setLayout(layout)
        
        self.fields = fields
        self.entries =[]

       
        for i in range(len(self.fields)):
            label = QLabel(f"{self.fields[i]}:")
            layout.addWidget(label, 1 + i, 0)
            entry = QLineEdit()
            entry.setText('0')
            layout.addWidget(entry, 1 + i, 1)
            self.entries.append(entry)
            
        # Create a button to close the window
        self.cancel_button = QPushButton('Cancel', self)
        layout.addWidget(self.cancel_button,layout.rowCount(), 0)
        self.cancel_button.clicked.connect(self.accept)
        
        self.close_button = QPushButton('Ok', self)
        layout.addWidget(self.close_button,layout.rowCount(), 0)
        self.close_button.clicked.connect(self.get_values)
        
    def get_values(self):
        self.result = [0] * len(self.fields)
        for i in range(len(self.fields)):
            self.result[i] = self.entries[i].text()
        self.accept()
        
    def returnValue(self):
        return self.result