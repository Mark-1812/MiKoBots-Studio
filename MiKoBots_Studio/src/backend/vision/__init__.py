from backend.vision.vision_management import VisionManagement

vision_management = VisionManagement()

###########################
#   vision_management
###########################
def cam_connected():
    if vision_management.connect:
        return True
    else:
        return False
    
def get_square_size_per():
    return vision_management.square_size_per

def set_square_size_per(size):
    vision_management.square_size_per = size
    
def calculate_mm_per_pixel(image = None, Height = None):
    vision_management.calculate_mm_per_pixel(image, Height)
    
def cam_tool_connected(state):
    vision_management.cam_tool = state
    
def show_square_tool(state):
    vision_management.show_square_tool = state
    
def show_square(state):
    vision_management.show_square = state
    
def change_size_square(dir):
    vision_management.ChangeSizeSquare(dir)

def close_cam():
    vision_management.CloseCam()

def connect_cam(com_port = None):
    if vision_management.connect:
        vision_management.DisconnectCam()
    else:
        vision_management.ConnectCam(com_port)
    

def get_image_frame():
    return vision_management.GetImageFrame()

def get_mask(color, image):
    return vision_management.GetMask(color, image)

def draw_axis(img, p_, q_, color, scale):
    return vision_management.DrawAxis(img, p_, q_, color, scale)