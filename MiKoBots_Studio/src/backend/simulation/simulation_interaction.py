import vtk

class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        super().__init__()

    # Override the middle mouse button press event to rotate
    def OnMiddleButtonDown(self):
        self.StartRotate()

    def OnMiddleButtonUp(self):
        self.EndRotate()

    def OnMouseMove(self):
        if self.GetInteractor().GetControlKey():  # If Control is pressed
            return  # Do not rotate if Control is pressed

        self.Rotate()  # Rotate the camera