from backend.vision.vision_management import VisionManagement

vision_management = VisionManagement()

###########################
#   vision_management
###########################

def close_cam():
    vision_management.CloseCam()

def connect_cam(com_port = None):
    vision_management.ConnectCam(com_port)

def get_image_frame():
    return vision_management.GetImageFrame()

def get_mask(color, image):
    return vision_management.GetMask(color, image)

def draw_axis(img, p_, q_, color, scale):
    return vision_management.DrawAxis(img, p_, q_, color, scale)