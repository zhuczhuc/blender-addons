bl_info = {
    "name": "New Object",
    "author": "zhuc",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import math

def add_cross_plane():
    bpy.ops.mesh.primitive_plane_add(
        location=(0, 0, 0), rotation=(0, 0, 0))
    bpy.data.objects['Plane'].name = 'xy'

    bpy.ops.mesh.primitive_plane_add(
        location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    bpy.data.objects['Plane'].name = 'xz'

    bpy.ops.mesh.primitive_plane_add(
        location=(0, 0, 0), rotation=(0, math.pi / 2, 0))
    bpy.data.objects['Plane'].name = 'yz'


def check_fbx(fbx_path):
    bpy.ops.import_scene.fbx(filepath=fbx_path)

    bpy.data.scenes['Scene'].render.filepath = r'F:\qq\lx\0228\nighttable02\\a.png'
    bpy.ops.render.render(use_viewport=True, write_still=True)

    # add xy, xz plane
    bpy.ops.mesh.primitive_plane_add(
        location=(0, 0, 0), rotation=(0, 0, 0))
    bpy.data.objects['Plane'].name = 'xy'
    bpy.ops.mesh.primitive_plane_add(
        location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    bpy.data.objects['Plane'].name = 'xz'
    # set up camera
    bpy.data.objects['Camera'].rotation_euler = (math.pi / 2, 0, 0)
    bpy.data.objects['Camera'].location = (0, 3, 1)

    bpy.data.scenes['Scene'].render.filepath = r'F:\qq\lx\0228\nighttable02\\b.png'
    bpy.ops.render.render(use_viewport=True, write_still=True)


def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    def execute(self, context):

        # add_object(self, context)

        fbx_path = r'F:\qq\lx\0228\nighttable02\chuangtougui02.fbx'
        check_fbx(fbx_path)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/dev/"
    url_manual_mapping = (
         ("bpy.ops.mesh.add_object", "editors/3dview/object"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_add.remove(add_object_button)


if __name__ == "__main__":
    register()
