import backend.core.variables as var

def calculate_mm_per_pixel(Height = None):      
    Zdelta = var.TOOL_SETTINGS_CAM[0] - var.TOOL_SETTINGS_CAM[1]
    Xdelta = var.TOOL_SETTINGS_CAM[2] - var.TOOL_SETTINGS_CAM[3]
    
    print(Zdelta)
    print(Xdelta)
    
    Ratio_height_width = Xdelta/Zdelta
    
    if Height == None:    
        new_Zdelta = var.TOOL_SETTINGS_CAM[0] - float(var.POS_AXIS[2])
    else:
        new_Zdelta = var.TOOL_SETTINGS_CAM[0] - Height
        
    print(new_Zdelta)
        
    mm_per_pixel = (var.TOOL_SETTINGS_CAM[2] - (new_Zdelta * Ratio_height_width)) / var.TOOL_SETTINGS_CAM[4]
    
    return mm_per_pixel