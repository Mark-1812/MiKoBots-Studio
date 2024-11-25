from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QListWidget, QMainWindow, QComboBox, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtGui import QIcon
from serial.tools import list_ports

from backend.core.event_manager import event_manager
from backend.file_managment.file_management import FileManagement

from backend.robot_management.communication  import scan_for_io
from backend.robot_management.communication import connect_io

from backend.robot_management.communication import scan_for_robots
from backend.robot_management.communication import connect_robot

from backend.vision import connect_cam

from gui.style import *

class ConnectDevice(QWidget):
    def __init__(self, type):
        super().__init__()
        self.type = type

        self.setWindowTitle("Connect " + type)
        self.setFixedSize(300, 400)
        self.setStyleSheet(style_widget)
        
        file_management = FileManagement()
        image_path = file_management.resource_path('mikobot.ico')
        self.setWindowIcon(QIcon(image_path))

        layout = QVBoxLayout(self)

        self.BT_device_list = []
        self.port_list = []

        
        label1 = QLabel("COM ports:")
        label1.setStyleSheet(style_label_bold)
        self.list_com = QListWidget(self)
        self.list_com.setStyleSheet(style_listwidget)
        label2 = QLabel("The com port of a webcam does not always show. Fill here 0 in if you have one camere, or 1 if it's your second cam")
        label2.setWordWrap(True)
        label2.setStyleSheet(style_label)
        self.com_port_entry = QLineEdit()
        self.com_port_entry.setStyleSheet(style_entry)
        self.com_port_entry.setPlaceholderText("0")
        self.scan_button_com = QPushButton("Scan com ports", self)
        self.scan_button_com.setStyleSheet(style_button_menu)
        self.connect_com_button = QPushButton("Connect to " + self.type, self)
        self.connect_com_button.setStyleSheet(style_button_menu)

        layout.addWidget(label1)
        layout.addWidget(self.list_com)
        if self.type == "CAMERA":
            layout.addWidget(self.com_port_entry)
            layout.addWidget(label2)
        layout.addWidget(self.scan_button_com)
        layout.addWidget(self.connect_com_button)
        
        self.scan_button_com.clicked.connect(self.refresh_ports)
        self.connect_com_button.clicked.connect(self.connect_com_device)
                
        if self.type == "ROBOT" or self.type == "IO":
            label2 = QLabel("Bluetooth devices:")
            label2.setStyleSheet(style_label_bold)
            self.device_list = QListWidget(self)
            self.device_list.setStyleSheet(style_listwidget)
            self.scan_button = QPushButton("Scan bluetooth devices", self)
            self.scan_button.setStyleSheet(style_button_menu)
            self.connect_bt_button = QPushButton("Connect to bluetooth " + self.type, self)
            self.connect_bt_button.setStyleSheet(style_button_menu)

            layout.addWidget(label2)
            layout.addWidget(self.device_list)
            layout.addWidget(self.scan_button)
            layout.addWidget(self.connect_bt_button)

            self.scan_button.clicked.connect(self.start_scanning)
            self.connect_bt_button.clicked.connect(self.connect_bt_device)

            self.subscribeToEvents()

        elif self.type == "CAMERA":
            label3 = QLabel("fill in the IP adress")
            label3.setStyleSheet(style_label_bold)
            self.entry = QLineEdit("http://192.168.1.185:81/stream")
            self.entry.setStyleSheet(style_entry)
            button_ip = QPushButton("Connect to " + self.type)
            button_ip.setStyleSheet(style_button_menu)
            
            button_ip.clicked.connect(self.connect_ip_device)

            layout.addWidget(label3)
            layout.addWidget(self.entry)
            layout.addWidget(button_ip)

        #self.label_connected.hide()
        self.selected_port = None
        

    def subscribeToEvents(self):
        event_manager.subscribe("request_bt_channels", self.update_device_list)
        
    def empty_list(self):
        # com 
        self.list_com.clear()
        self.com_port_entry.setText("")
        
        # bluetooth
        self.device_list.clear()
        self.BT_device_list.clear()
        
        

    #### IP adress
    def connect_ip_device(self):
        addres = self.entry.text()
        connect_cam(addres)

    #### COM porst
    def refresh_ports(self):    
        ports = list_ports.comports()
        
        self.list_com.clear()
        self.port_list.clear()
        for port in ports:
            self.port_list.append(port.device)
            self.list_com.addItem(str(port))  # Pass the list to addItems

        
    def connect_com_device(self):
        item = self.list_com.currentItem()
        position = self.list_com.row(item)
        
        if position == None:
            return
        
        if self.type == "CAMERA" and self.com_port_entry.text():
            device = int(self.com_port_entry.text())
            connect_cam(device)
            return
        
        if item:
            device = self.port_list[position]
            if self.type == "ROBOT":
                connect_robot(device, True)
            elif self.type == "IO":
                connect_io(device, True)
            elif self.type == "CAMERA":
                connect_cam(device)



    ### Bluetooth
    def start_scanning(self):
        if self.type == "ROBOT":
            scan_for_robots()
        elif self.type == "IO":
            scan_for_io()
        
    def connect_bt_device(self):
        item = self.device_list.currentItem()
        position = self.device_list.row(item)

        if position == None:
            return

        if item:
            device = self.BT_device_list[position]
            if self.type == "ROBOT":
                connect_robot(device, False)
            elif self.type == "IO":
                connect_io(device, False)

    def update_device_list(self, devices):
        self.device_list.clear()
        self.BT_device_list.clear()
        for device in devices:
            self.BT_device_list.append(device)
            name = str(device.name)
            self.device_list.addItem(name)  # Pass the list to addItems


