# combo box
style_combo = ("""
            QComboBox {
                background-color: white;
                border: 0px solid gray;
                height: 20px; 
                border-radius: 5px;
                padding: 0px;
                font-family: "Segoe UI";
                font-size: 14px;
                text-align: center;
                color: black;
                
            }
            QComboBox::drop-down {
                border: none;  /* Remove border around the drop-down button */
                background-color: orange;  /* Background color of the drop-down button */
                width: 20px;  /* Set the width of the drop-down button */
                border-radius: 3px;
            }
            QComboBox::down-arrow {
                width: 10px;  /* Set the width of the arrow */
                height: 10px;  /* Set the height of the arrow */
            }
            QComboBox:hover {
                color: black; 
            }
            QComboBox QAbstractItemView {
                background-color: white;  /* Drop-down background color */
                color: black;  /* Text color for items in the drop-down */
            }
            """)


## checkbox
style_checkbox = ("""
            QCheckBox {
                background-color: lightgray;
                border: 0px solid gray;
                border-radius: 5px;
                font-family: "Segoe UI";
                font-size: 12px;
                color: black; 
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 0px solid grsay;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: green;
                border: 0px solid grsay;
                border-radius: 3px;
            }
            """)

style_checkbox_io = ("""
            QCheckBox {
                background-color: lightgray;
                border: 0px solid gray;
                border-radius: 5px;
                font-family: "Segoe UI";
                font-size: 12px;
                color: black; 
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
                font-size: 14px;
                font-family: "Segoe UI";
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
            """)

style_button_menu = ("""
            QPushButton { 
                background-color: orange; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 25px; 
                font-size: 14px;
                font-family: "Segoe UI";
                padding: 0;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
            """)

style_button_zoom = ("""
            QPushButton { 
                background-color: rgba(150, 155, 155, 128);
                color: black; 
                border: 0px solid black; 
                border-radius: 15px; 
                height: 20px; 
                font-size: 14px;
                font-family: "Segoe UI";
                padding: 20px;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: gray; 
            }
                     
            """)


style_button_pressed = ("""
            QPushButton { 
                background-color: green; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 25px; 
                font-size: 14px;
                font-family: "Segoe UI";
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
                font-size: 14px;
                font-family: Arial;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: darkorange; 
            }
            """)

style_button_3d = ("""
            QPushButton { 
                background-color: lightgray; 
                color: black; 
                border: 0px solid black; 
                border-radius: 3px; 
                height: 20px; 
                font-size: 14px;
                font-family: "Segoe UI";
            }
            QPushButton:hover { 
                background-color: gray; 
            }
            QPushButton:pressed { 
                background-color: gray; 
            }
                     
            """)

style_button_tab = ( """
            QRadioButton::indicator {
                width: 1px; /* Reduce size to minimal without setting it to 0 */
                height: 1px; /* Same for height to avoid the error */
                background-color: transparent; /* Make the indicator invisible */            
            }
            QRadioButton {
                background-color: orange;
                border: 0px solid gray;
                border-radius: 3px;
                height: 35px;
                padding: 0px 25px; /* Adjust padding to ensure text is centered */
                font-size: 12px;
                font-family: Arial;
                text-align: center; /* Center the text horizontally */
                color: black; 
             }
            QRadioButton:hover {
                background-color: white;
            }
            QRadioButton:checked {
                background-color: green;
                color: black;
            }
        """)

style_button_help = ("""
            QPushButton { 
                background-color: rgba(150, 155, 155, 128);
                color: black; 
                border: 0px solid black; 
                border-radius: 10px; 
                height: 20px; 
                font-size: 14px;
                font-family: "Segoe UI";
                padding: 20px;
            }
            QPushButton:hover { 
                background-color: white; 
            }
            QPushButton:pressed { 
                background-color: gray; 
            }
                     
            """)





## label
style_label_title = ("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 16px; 
                font-weight: bold;
                text-align: center;
                color: black; 
            }
            """)

style_label_bold = ("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 13px; 
                font-weight: bold;
                text-align: center;
                color: black; 
                height: 20px;
            }
            """)

style_label = ("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 12px;
                text-align: center;
                color: black; 
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
                color: black;
            }
        """)

## radio button
style_radiobutton = ("""
            QRadioButton {
                background-color: lightgray;
                font-family: "Segoe UI";
                font-size: 12px;
                color: black;
                padding: 5px;
                border-radius: 5px;
            }
            QRadioButton::indicator {
                width: 12px;
                height: 12px;
            }
            QRadioButton::indicator:checked {
                background-color: green;
                border: 0px solid grsay;
                border-radius: 6px;
            }
            QRadioButton::indicator:unchecked {
                background-color: white;
                border: 0px solid grsay;
                border-radius: 6px;
            }
        """)





style_textedit = ("""
            QTextEdit {
                background-color: white;
                border: 0px solid gray;
                border-radius: 5px;
            }
                        QTextEdit {
                padding: 5;
                background-color: white;
                border-top-right-radius: 5px;  
                border-bottom-right-radius: 5px;  
                border-bottom-left-radius: 0px;   
                border-top-left-radius: 0px;      
            }
            QScrollBar:horizontal {
                border: 0px; /* No border */
                background: white; /* Background color */
                height: 10px; /* Width of the scrollbar */
            }

            QScrollBar::handle:horizontal {
                background: gray; /* Color of the scrollbar handle */
                min-width: 20px; /* Minimum width of the handle */
                border-radius: 5px; /* Rounded corners for the handle */
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: transparent; /* Hide the end buttons */
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent; /* Background for the add/sub pages */
            }
                    
            QScrollBar:vertical {
                border: 0px; /* No border */
                background: white; /* Background color */
                width: 10px; /* Width of the scrollbar */
            }

            QScrollBar::handle:vertical {
                background: gray; /* Color of the scrollbar handle */
                min-height: 20px; /* Minimum height of the handle */
                border-radius: 5px; /* Rounded corners for the handle */
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: transparent; /* Hide the end buttons */
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent; /* Background for the add/sub pages */
            }
            """)


style_textedit_program = ("""
            QTextEdit {
                padding: 5;
                background-color: white;
                border-top-right-radius: 5px;  
                border-bottom-right-radius: 5px;  
                border-bottom-left-radius: 0px;   
                border-top-left-radius: 0px;      
            }
            QScrollBar:horizontal {
                border: 0px; /* No border */
                background: white; /* Background color */
                height: 10px; /* Width of the scrollbar */
            }

            QScrollBar::handle:horizontal {
                background: gray; /* Color of the scrollbar handle */
                min-width: 20px; /* Minimum width of the handle */
                border-radius: 5px; /* Rounded corners for the handle */
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: transparent; /* Hide the end buttons */
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent; /* Background for the add/sub pages */
            }
                    
            QScrollBar:vertical {
                border: 0px; /* No border */
                background: white; /* Background color */
                width: 10px; /* Width of the scrollbar */
            }

            QScrollBar::handle:vertical {
                background: gray; /* Color of the scrollbar handle */
                min-height: 20px; /* Minimum height of the handle */
                border-radius: 5px; /* Rounded corners for the handle */
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: transparent; /* Hide the end buttons */
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent; /* Background for the add/sub pages */
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
                border: 0px solid #339c9a; 
            }
            QWidget {
                padding: 0;  /* No padding */
            }
            QScrollBar:horizontal {
                border: 0px; /* No border */
                background: #E8E8E8; /* Background color */
                height: 10px; /* Height of the scrollbar */
            }

            QScrollBar::handle:horizontal {
                background: gray; /* Color of the scrollbar handle */
                min-width: 20px; /* Minimum width of the handle */
                border-radius: 5px; /* Rounded corners for the handle */
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: transparent; /* Hide the end buttons */
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent; /* Background for the add/sub pages */
            }
                    
            QScrollBar:vertical {
                border: 0px; /* No border */
                background: lightgray; /* Background color */
                width: 10px; /* Width of the scrollbar */
            }

            QScrollBar::handle:vertical {
                background: gray; /* Color of the scrollbar handle */
                min-height: 20px; /* Minimum height of the handle */
                border-radius: 5px; /* Rounded corners for the handle */
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: transparent; /* Hide the end buttons */
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent; /* Background for the add/sub pages */
            }
                    
            """)

style_widget = ("""
            QWidget { 
                background-color: lightgray;
            }
            """)

style_slider = ("""
            QSlider::groove:horizontal {
                border: 0px solid #999999;
                height: 8px;
                background: white;
                margin: 0px 12px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: lightgray;
                background: orange;
                border: 0px solid #5c5c5c;
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
                border: 0px solid #999999;
                border-radius: 50px;
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
              QTabBar {
                alignment: left;  /* Align tabs to the left */
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

style_listwidget = ("""
    QListWidget {
        font-family: "Arial";
        background-color: white;
        color: black;
        font-size: 14px;
        border: 0px solid black;
        border-radius: 6px;
                    
    }

    /* Scrollbar styles applied directly */
    QListWidget::item {
        padding: 2px;
    }
    
    QScrollBar:vertical {
        border: none;
        background: lightgray;
        width: 12px;
        margin: 0px 0px 0px 0px;
    }

    /* Scrollbar handle */
    QScrollBar::handle:vertical {
        background-color: gray;
        min-height: 20px;
        border-radius: 5px;
    }

    /* Handle on hover */
    QScrollBar::handle:vertical:hover {
        background-color: darkgray;
    }

    /* Handle when pressed */
    QScrollBar::handle:vertical:pressed {
        background-color: dimgray;
    }

    /* Remove end-line buttons */
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }

    /* Transparent scroll area */
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
""")



