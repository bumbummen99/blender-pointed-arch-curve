import bpy
from math import sqrt, acos, cos, sin, pi
from mathutils import Vector

def create_pointed_arch(width=2.0, pointiness=0.0, vertices=9):
    """
    width      = final width of the arch (ABSOLUTE)
    pointiness = 0 → half circle, 1 → very sharp
    vertices   = total vertices INCLUDING apex
    """

    if vertices < 3:
        vertices = 3

    # -------------------------
    # 1. Normalized construction
    r = 1.0  # normalized Radius

    # Pointiness defines space between circles
    # 0 = Perfect half circle (d = 0)
    # 1 = Circles touch but don't overlap
    d = r * min(max(pointiness, 0.0), 0.999)

    h = sqrt(r * r - d * d)

    left_center  = Vector((-d, 0, 0))
    right_center = Vector(( d, 0, 0))
    apex = Vector((0, h, 0))

    alpha = acos(d / r)

    left_count = right_count = (vertices - 1) // 2

    left_arc = []
    right_arc = []

    # Left part
    for i in range(left_count):
        t = i / left_count
        ang = alpha * t
        x = left_center.x + r * cos(ang)
        y = left_center.y + r * sin(ang)
        left_arc.append(Vector((x, y, 0)))

    # Right part
    for i in range(right_count):
        t = i / right_count
        ang = pi - alpha * t
        x = right_center.x + r * cos(ang)
        y = right_center.y + r * sin(ang)
        right_arc.append(Vector((x, y, 0)))

    verts = left_arc + [apex] + right_arc[::-1]

    # -------------------------
    # 2. Scale to final width
    min_x = min(v.x for v in verts)
    max_x = max(v.x for v in verts)
    current_width = max_x - min_x

    scale = width / current_width

    verts = [Vector((v.x * scale, v.y * scale, 0)) for v in verts]

    # -------------------------
    # 3. Generate the Curve
    curve_data = bpy.data.curves.new("PointedArch", type='CURVE')
    curve_data.dimensions = '2D'

    spline = curve_data.splines.new('POLY')
    spline.points.add(len(verts) - 1)

    for i, v in enumerate(verts):
        spline.points[i].co = (v.x, v.y, 0, 1)

    obj = bpy.data.objects.new("PointedArch", curve_data)
    bpy.context.collection.objects.link(obj)

    return obj

class OBJECT_OT_add_pointed_arch(bpy.types.Operator):
    bl_idname = "curve.add_pointed_arch"
    bl_label = "Add Pointed Arch"
    bl_options = {'REGISTER', 'UNDO'}

    width: bpy.props.FloatProperty(
        name="Width",
        default=2.0,
        min=0.01
    )

    pointiness: bpy.props.FloatProperty(
        name="Pointiness",
        default=0.0,
        min=0.0,
        max=1.0
    )

    vertices: bpy.props.IntProperty(
        name="Vertices",
        default=9,
        min=3,
        max=128
    )

    def execute(self, context):
        create_pointed_arch(
            width=self.width,
            pointiness=self.pointiness,
            vertices=self.vertices
        )
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(
        OBJECT_OT_add_pointed_arch.bl_idname,
        icon='CURVE_BEZCURVE'
    )

def register():
    bpy.utils.register_class(OBJECT_OT_add_pointed_arch)
    bpy.types.VIEW3D_MT_curve_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_pointed_arch)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_func)
