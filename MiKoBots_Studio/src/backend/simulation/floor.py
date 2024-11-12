import vtk


class Floor():
    def __init__(self, renderer):
        self.renderer = renderer

        self.ShowFloor = False

        size_plane = 750
        
        grid_distance = 50  # 50 mm
        grid_polydata = self.create_grid_plane(grid_distance, size_plane)
        
        # Mapper and Actor for the grid
        grid_mapper = vtk.vtkPolyDataMapper()
        grid_mapper.SetInputData(grid_polydata)
        self.grid_actor = vtk.vtkActor()
        self.grid_actor.SetMapper(grid_mapper)
        
        self.grid_actor.GetProperty().SetColor(0, 0, 0)  # RGB color
        
        # Create a plane on the XY axis
        plane_source = vtk.vtkPlaneSource()
        plane_source.SetOrigin(-size_plane, -size_plane, 0)  # Bottom left corner
        plane_source.SetPoint1(size_plane, -size_plane, 00)   # Bottom right corner
        plane_source.SetPoint2(-size_plane, size_plane, 0)   # Top left corner
        plane_source.SetResolution(10, 10)    # Number of points along the plane

        # Mapper and Actor for the plane
        plane_mapper = vtk.vtkPolyDataMapper()
        plane_mapper.SetInputConnection(plane_source.GetOutputPort())
        self.plane_actor = vtk.vtkActor()
        self.plane_actor.SetMapper(plane_mapper)

        # Set the color of the plane (e.g., light gray)
        self.plane_actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # RGB color
        self.plane_actor.GetProperty().SetOpacity(0.5)


        self.renderer.AddActor(self.grid_actor)  # Add the grid actor
        self.renderer.AddActor(self.plane_actor)
        


    def create_grid_plane(self, distance, size):
        lines = vtk.vtkCellArray()
        points = vtk.vtkPoints()

        # Generate points and lines
        for i in range(-size, size + 1, distance):
            # Horizontal lines
            p1_id = points.InsertNextPoint(-size, i, 0)
            p2_id = points.InsertNextPoint(size, i, 0)
            lines.InsertNextCell(2)
            lines.InsertCellPoint(p1_id)
            lines.InsertCellPoint(p2_id)

            # Vertical lines
            p1_id = points.InsertNextPoint(i, -size, 0)
            p2_id = points.InsertNextPoint(i, size, 0)
            lines.InsertNextCell(2)
            lines.InsertCellPoint(p1_id)
            lines.InsertCellPoint(p2_id)

        # Create a polydata object for the grid
        grid_polydata = vtk.vtkPolyData()
        grid_polydata.SetPoints(points)
        grid_polydata.SetLines(lines)
        
        return grid_polydata
    
    def HideShowFloor(self):
        # Add the plane and axes to the scene
        print(f"Show floor {self.ShowFloor}")
        if self.ShowFloor:
            
            self.grid_actor.SetVisibility(False)  # Set to True to show
            self.plane_actor.SetVisibility(False)  # Set to True to show
            self.ShowFloor = False
        else:
            self.grid_actor.SetVisibility(True)  
            self.plane_actor.SetVisibility(True) 
            self.ShowFloor = True

        # self.rendering()

   