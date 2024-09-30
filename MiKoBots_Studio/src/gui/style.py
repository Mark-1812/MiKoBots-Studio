


## checkbox
style_checkbox = ("""
            QCheckBox {
                background-color: lightgray;
                border: 0px solid gray;
                border-radius: 5px;
                font-family: "Segoe UI";
                font-size: 12px;
            }
            """)

style_checkbox_io = ("""
            QCheckBox {
                background-color: lightgray;
                border: 0px solid gray;
                border-radius: 5px;
                font-family: "Segoe UI";
                font-size: 12px;
            }
            QCheckBox::indicator { 
                border-radius: 5px; 
            }
            QCheckBox::indicator:checked { 
                background-color: green; 
            }
            QCheckBox::indicator:unchecked { 
                background-color: white; 
            }
            """)
            
                
## button
style_button = ("""
            QPushButton { 
                background-color: orange; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 20px; 
                font-size: 12px;
                font-family: "Segoe UI";
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
            """)

style_button_pressed = ("""
            QPushButton { 
                background-color: green; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 20px; 
                width: 40px; 
                font-size: 12px;
                font-family: Arial;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
            """)

style_button_red = ("""
            QPushButton { 
                background-color: red; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 20px; 
                width: 40px; 
                font-size: 12px;
                font-family: Arial;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
            """)



## label
style_label_title = ("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 16px; 
                font-weight: bold;
                text-align: center;
            }
            """)

style_label_bold = ("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 13px; 
                font-weight: bold;
                text-align: center;
            }
            """)

style_label = ("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 12px;
                text-align: center;
            }
            """)

## line edit/ entry
style_entry = ("""
            QLineEdit {
                background-color: white;
                border: 0px solid gray;
                border-radius: 3px;
                padding: 0px;
                font-family: "Segoe UI";
                font-size: 12px;
            }
        """)

## radio button
style_radiobutton = ("""
            QCheckBox {
                background-color: lightgray
                font-family: "Segoe UI";
                font-size: 12px;
            }
        """)

# combo box
style_combo = ("""
            QComboBox {
                background-color: white;
                border: 0px solid gray;
                border-radius: 3px;
                padding: 0px;
                font-family: "Segoe UI";
                font-size: 12px;
                text-align: center;
            }
            QComboBox:hover {
                color: black; 
            }
            QComboBox QAbstractItemView {
                background-color: white;  /* Drop-down background color */
                color: black;  /* Text color for items in the drop-down */
            }
            """)



style_textedit = ("""
            QTextEdit {
                background-color: white;
                border: 0px solid gray;
                border-radius: 5px;
            }
            """)

style_frame = ("""
            QFrame {
                background-color: lightgray;
                border: 0px solid gray;
                border-radius: 5px;
            }
            """)

style_scrollarea = ("""
            QScrollArea {
                background-color: lightgray;
                border: 0px solid gray;
                border-radius: 0px;
                padding: 0px;
            }
            QScrollBar:vertical {
                background-color: lightgray;
                width: 15px;
            }
            """)

style_widget = ("""
            QWidget { 
                background-color: lightgray;
            }
            """)

style_slider = ("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: white;
                margin: 0px 12px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: lightgray;
                background: orange;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0; /* Handle is placed by default on the contents rect of the groove. Expand outside the groove */
                border-radius: 3px;
            }
            QSlider {
                background-color: lightgray;
            }
            """)

style_tabs = ("""
            QTabWidget::pane { /* The tab widget frame */
                border: 1px solid #999999;
                border-radius: 5px;
                background: lightgray;
            }
            QTabBar::tab { 
                background-color: orange; 
                color: black;  
                height: 20px; 
                width: 80px; 
                font-size: 12px; 
                font-family: Arial;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
            }
            """)



style_messagebox = ("""
            QMessageBox {
                background-color: lightgray;
                color: #333;
                font-size: 14px;
                border: 1px solid black; 
                border-radius: 6px;
            }
            QPushButton { 
                background-color: orange; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 20px; 
                width: 60px; 
                font-size: 12px;
                font-family: Arial;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
        """)

