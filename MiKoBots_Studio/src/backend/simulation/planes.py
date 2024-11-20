import vtk

class Planes():
    def __init__(self, renderer):
        renderer = renderer
        
        origin = [0, 0, 0]
        size = 100  # Example size; set as needed
        
        self.add_vtk_plane(renderer, origin, [0, 0, 1], size, "blue")  # XY plane
        self.add_vtk_plane(renderer, origin, [0, 1, 0], size, "red")   # XZ plane
        self.add_vtk_plane(renderer, origin, [1, 0, 0], size, "green") # ZY plane
        
    def add_vtk_plane(self, renderer, origin, normal, size, color):
        # Create a plane source
        plane_source = vtk.vtkPlaneSource()
        plane_source.SetCenter(origin)

        # Set the normal vector for the plane
        plane_source.SetNormal(normal)

        # Set the size of the plane by defining two points in the plane
        if normal == [0, 0, 1]:  # XY plane
            plane_source.SetOrigin(-size / 2, -size / 2, 0)
            plane_source.SetPoint1(size / 2, -size / 2, 0)
            plane_source.SetPoint2(-size / 2, size / 2, 0)

        elif normal == [0, 1, 0]:  # XZ plane
            plane_source.SetOrigin(-size / 2, 0, -size / 2)
            plane_source.SetPoint1(size / 2, 0, -size / 2)
            plane_source.SetPoint2(-size / 2, 0, size / 2)

        elif normal == [1, 0, 0]:  # ZY plane
            plane_source.SetOrigin(0, -size / 2, -size / 2)
            plane_source.SetPoint1(0, size / 2, -size / 2)
            plane_source.SetPoint2(0, -size / 2, size / 2)

        # Mapper for the plane
        plane_mapper = vtk.vtkPolyDataMapper()
        plane_mapper.SetInputConnection(plane_source.GetOutputPort())

        # Actor for the plane
        plane_actor = vtk.vtkActor()
        plane_actor.SetMapper(plane_mapper)
        plane_actor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d(color))
        plane_actor.GetProperty().SetOpacity(0.5)

        # Add the actor to the renderer
        renderer.AddActor(plane_actor)