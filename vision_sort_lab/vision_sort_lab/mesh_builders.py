from stl import mesh as stl_mesh
from geometry_msgs.msg import Point
from shape_msgs.msg import Mesh, MeshTriangle


def load_stl_mesh(file_path):
    result = Mesh()
    source = stl_mesh.Mesh.from_file(str(file_path))
    for triangle_vertices in source.vectors:
        start = len(result.vertices)
        for xyz in triangle_vertices:
            point = Point()
            point.x = float(xyz[0])
            point.y = float(xyz[1])
            point.z = float(xyz[2])
            result.vertices.append(point)
        triangle = MeshTriangle()
        triangle.vertex_indices = [start, start + 1, start + 2]

        result.triangles.append(triangle)

    return result