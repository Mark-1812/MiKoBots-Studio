import backend.core.variables as var

def calculate_mm_per_pixel(image, Height = None):    
    settings_cam = var.TOOLS3D[var.SELECTED_TOOL][11]
    
    z1 = float(settings_cam[0]) # Z distance big square
    z2 = float(settings_cam[1]) # Z distance small square
    
    size1 = float(settings_cam[2]) # size big square
    size2 = float(settings_cam[3]) # size small square
      
    Zdelta = z1 - z2
    Xdelta = size1 - size2
    
    Ratio_height_width = Xdelta/Zdelta
    
    if Height == None:    
        new_Zdelta = z1 - float(var.POS_AXIS[2])
    else:
        new_Zdelta = z1 - Height
        
    height_picture, width_picture, ch = image.shape 
        
    square_width_pixel = width_picture * 0.8
        
    mm_per_pixel = (size1 - (new_Zdelta * Ratio_height_width)) / square_width_pixel
    
    return mm_per_pixel