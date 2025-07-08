def get_application_styles():
    return """
    QMainWindow {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                  stop: 0 #f0f8ff, stop: 1 #e6f3ff);
    }
    
    #title {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin: 10px;
    }
    
    #subtitle {
        font-size: 14px;
        color: #7f8c8d;
        margin-bottom: 20px;
    }
    
    #searchFrame {
        background: white;
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    #prefixLabel {
        font-size: 14px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    
    #searchInput {
        font-size: 14px;
        padding: 10px;
        border: 2px solid #bdc3c7;
        border-radius: 5px;
        margin-right: 10px;
    }
    
    #searchInput:focus {
        border-color: #3498db;
    }
    
    #searchButton {
        font-size: 14px;
        font-weight: bold;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                  stop: 0 #3498db, stop: 1 #2980b9);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        min-width: 120px;
    }
    
    #searchButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                  stop: 0 #5dade2, stop: 1 #3498db);
    }
    
    #searchButton:pressed {
        background: #2980b9;
    }
    
    #resultsFrame {
        background: white;
        border: 2px solid #27ae60;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    #resultsLabel {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    #resultsList {
        border: 1px solid #bdc3c7;
        border-radius: 5px;
        background: #fafafa;
        selection-background-color: #3498db;
        selection-color: white;
        font-size: 13px;
        padding: 5px;
    }
    
    #resultsList::item {
        padding: 8px;
        border-bottom: 1px solid #ecf0f1;
    }
    
    #resultsList::item:hover {
        background: #e8f4fd;
    }
    
    #resultsList::item:selected {
        background: #3498db;
        color: white;
    }
    
    #infoLabel {
        font-size: 12px;
        color: #7f8c8d;
        margin-top: 10px;
        font-style: italic;
    }
    
    #footerFrame {
        background: rgba(255, 255, 255, 0.8);
        border-top: 1px solid #bdc3c7;
        margin-top: 10px;
    }
    
    #footerLabel {
        font-size: 11px;
        color: #95a5a6;
        font-style: italic;
    }
    """

def get_error_styles():
    return """
    .error-message {
        color: #e74c3c;
        font-weight: bold;
        background: #fdf2f2;
        border: 1px solid #e74c3c;
        border-radius: 5px;
        padding: 10px;
    }
    """

def get_success_styles():
    return """
    .success-message {
        color: #27ae60;
        font-weight: bold;
        background: #f2f8f2;
        border: 1px solid #27ae60;
        border-radius: 5px;
        padding: 10px;
    }
    """