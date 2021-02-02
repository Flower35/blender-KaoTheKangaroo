################################################################
# "__init__.py"

bl_info = {
    "name": "Kao the Kangaroo Add-on",
    "description": "Import and Export levels and models from \"Kao the Kangaroo\" game series.",
    "author": "Radosław Krzyśków",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export"
}

################################################################

import bpy
from bpy_extras.io_utils import (ImportHelper, ExportHelper)

import traceback

from .KAO2.TypeInfo import KAO2_TypeInfo
from .KAO2.Archive import KAO2_Archive
from .KAO2.KeyframesExporter import BLENDER_OT_KAO2_KeyframesExporter
from .KAO2.HelperTools import *

from .KaoUtility import *


################################################################

BLENDER_KAO2_GameVersionProperty = bpy.props.EnumProperty (
    name = "Game version",
    items = [
        ("KAO2_PL", "Runda 2 (Polish, Retail)", ""),
        ("KAO2_USA", "Round 2 (Digital)", ""),
        ("KAO_TW", "Tajemnica Wulkanu", "")
    ],
    default = "KAO_TW"
)



class BLENDER_OT_KAO2_Importer(bpy.types.Operator, ImportHelper):
    """Import a \"Kao the Kangaroo: Round 2\" scene."""

    bl_idname = "kao_the_kangaroo_round_2.import_scene"
    bl_label = "Import AR"

    filter_glob: bpy.props.StringProperty (
        default = "*.ar",
        options = {"HIDDEN"},
        maxlen = 255
    )

    setting_workspace: bpy.props.StringProperty (
        name = "Workspace (\"/media/\") directory",
        default = "",
        maxlen = 255
    )

    setting_invbindmat: bpy.props.BoolProperty (
        name = "Apply Inverse Bind Matrices on Transforms",
        description = "\n Try to guess the Rest-Pose binding for any transform (bone) referenced by a mesh modifier.\n \n Leave unchecked if the model was exported in \"zero_pos\" animation.",
        default = True
    )

    setting_norestpose: bpy.props.BoolProperty (
        name = "Ignore the Rest-Pose setting for armatures",
        description = "\n Makes meshes with Armature modifiers compatible with Kao2 bone transformations (all bones placed at [0,0,0]).\n \n Leave unchecked if you want to create new animations.",
        default = False
    )

    setting_animations: bpy.props.BoolProperty (
        name = "Load animations",
        description = "\n This option will only work when previous option (ignoring Rest-Pose) is Enabled!",
        default = False
    )

    setting_version: BLENDER_KAO2_GameVersionProperty

    def execute(self, context):

        try:

            ar = KAO2_Archive()
            ar.open(self.filepath, True, self.setting_version)

            text = "Archive serialization success."
            self.report({"INFO"}, text)
            print("-" * 64)
            print("[KAO2] " + text)

            obj = ar.convertToBlender(self.setting_workspace, self.setting_invbindmat, self.setting_norestpose, self.setting_animations)

            if (obj is not None) and isinstance(obj, bpy.types.Object):

                link_objects_to_scene_collection(obj)

                bpy.context.scene.render.fps = 30
                bpy.context.scene.frame_start = 0
                bpy.context.scene.frame_end = 1000

                text = "Archive conversion success."

            else:

                text = "Archive was empty?!"

            self.report({"INFO"}, text)
            print("-" * 64)
            print("[KAO2] " + text)

            return {"FINISHED"}

        except Exception as e:

            print("-" * 64)
            traceback.print_exc()
            self.report({"ERROR"}, str(e))

            return {"CANCELLED"}


class BLENDER_OT_KAO2_Exporter(bpy.types.Operator, ExportHelper):
    """Export a \"Kao the Kangaroo: Round 2\" scene."""

    bl_idname = "kao_the_kangaroo_round_2.export_scene"
    bl_label = "Export AR"

    filename_ext = ".ar"
    filter_glob: bpy.props.StringProperty (
        default = "*.ar",
        options = {"HIDDEN"},
        maxlen = 255
    )

    setting_game_version: BLENDER_KAO2_GameVersionProperty

    def execute(self, context):

        try:

            #@@ ar = KAO2_Archive()
            #@@ ar.open(self.filepath, False, self.setting_game_version)

            self.report({"WARNING"}, "NOT SUPPORTED YET !!!")

            return {"FINISHED"}

        except Exception as e:

            traceback.print_exc()
            self.report({"ERROR"}, str(e))

            return {"CANCELLED"}


################################################################

def menu_func_kao2_import(self, context) -> None:

    self.layout.operator(BLENDER_OT_KAO2_Importer.bl_idname, text = "Kao the Kangaroo: Round 2 (.ar)")


def menu_func_kao2_export(self, context) -> None:

    self.layout.operator(BLENDER_OT_KAO2_Exporter.bl_idname, text = "Kao the Kangaroo: Round 2 (.ar)")


################################################################

class BLENDER_PT_KAO2_ToolPanel(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_label = "\"Kao the Kangaroo: Round 2\" Tools"
    bl_idname = "kao_the_kangaroo_round_2._PT_.misc"

    def draw(self, context):

        col = self.layout.column(align = True)
        col.operator(BLENDER_OT_KAO2_KeyframesExporter.bl_idname, text = "Export keyframes")
        col.operator(BLENDER_OT_KAO2_ProxiesExporter.bl_idname, text = "Write Selected Objects as Proxies")


################################################################

def register() -> None:

    bpy.utils.register_class(BLENDER_OT_KAO2_Importer)
    bpy.utils.register_class(BLENDER_OT_KAO2_Exporter)
    bpy.utils.register_class(BLENDER_OT_KAO2_KeyframesExporter)
    bpy.utils.register_class(BLENDER_OT_KAO2_ProxiesExporter)
    bpy.utils.register_class(BLENDER_PT_KAO2_ToolPanel)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_kao2_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_kao2_export)

    KAO2_TypeInfo.register()


def unregister() -> None:

    KAO2_TypeInfo.unregister()

    bpy.types.TOPBAR_MT_file_export.remove(menu_func_kao2_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_kao2_import)

    bpy.utils.unregister_class(BLENDER_PT_KAO2_ToolPanel)
    bpy.utils.unregister_class(BLENDER_OT_KAO2_ProxiesExporter)
    bpy.utils.unregister_class(BLENDER_OT_KAO2_KeyframesExporter)
    bpy.utils.unregister_class(BLENDER_OT_KAO2_Exporter)
    bpy.utils.unregister_class(BLENDER_OT_KAO2_Importer)


if __name__ == "__main__":
    register()


################################################################
