import vtk

class Axis():
    def __init__(self, renderer):
        self.renderer = renderer
        
        self.ShowAxis = False
        # Create axis arrows
        self.x_axis_actor = self.create_arrow_actor([90, 1000, 0, 0], (1, 0, 0))  # Red for X-axis
        self.y_axis_actor = self.create_arrow_actor([90, 0, 0, 1000], (0, 1, 0))  # Green for Y-axis
        self.z_axis_actor = self.create_arrow_actor([90, 0, -1000, 0], (0, 0, 1))   # Blue for Z-axis
        
        # Add the axis actors to the scene
        self.renderer.AddActor(self.x_axis_actor)
        self.renderer.AddActor(self.y_axis_actor)
        self.renderer.AddActor(self.z_axis_actor)

    def create_arrow_actor(self, direction, color):
        # Create an arrow source
        arrow_source = vtk.vtkArrowSource()
        
        # Transform to orient the arrow in the desired direction
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(direction[0], direction[1], direction[2], direction[3])
        transform.Scale(500, 150, 150)
        
        # Apply transformation
        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetTransform(transform)
        transform_filter.SetInputConnection(arrow_source.GetOutputPort())
        
        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())
        
        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        
        return actor    

    def HideShowAxis(self):
        # Add the plane and axes to the scene
        if self.ShowAxis:
            self.x_axis_actor.SetVisibility(False)  # Set to True to show
            self.y_axis_actor.SetVisibility(False)  # Set to True to show
            self.z_axis_actor.SetVisibility(False)  # Set to True to show
            self.ShowAxis = False
        else:
            self.x_axis_actor.SetVisibility(True)  # Set to True to show
            self.y_axis_actor.SetVisibility(True)  # Set to True to show
            self.z_axis_actor.SetVisibility(True)  # Set to True to show
            self.ShowAxis = True

