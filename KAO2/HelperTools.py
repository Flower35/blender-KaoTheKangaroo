################################################################
# "KAO2/HelperTools.py"

import bpy
import traceback
from bpy_extras.io_utils import ExportHelper

from .Basic import (KAO2_ePoint3, KAO2_eQuat, KAO2_eSRP)
from ..KaoUtility import *


################################################################

class BLENDER_OT_KAO2_ProxiesExporter(bpy.types.Operator, ExportHelper):
    """Export selected objects as proxies into a text format importable in ZookieWizard."""
    bl_idname = "kao_the_kangaroo_round_2.export_proxies"
    bl_label = "Export Selected as Proxies"

    filename_ext = ".log"
    filter_glob: bpy.props.StringProperty (
        default = "*.log",
        options = {"HIDDEN"},
        maxlen = 255
    )

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        try:
            with open(self.filepath, "w") as file:

                _debug_header = "[KAO2] ProxiesExporter():\n\t"

                print("-" * 64)
                print(_debug_header + "Saving text instructions...")

                file.write("/*\n    ZookieWizard instructions.\n*/\n\n")

                for obj in context.selected_objects:
                    pos = obj.location
                    rot = obj.rotation_quaternion
                    scl = obj.scale

                    file.write("    AddNode eProxy\n    (\n")
                    if obj.parent is not None:
                        file.write("        // parent = \"" + obj.parent.name + "\"\n")
                    file.write("        name = \"" + obj.name + "\"\n")
                    file.write("        pos  = [{} {} {}]\n".format(pos.x, pos.y, pos.z))

                    if (1.0 != rot.w) or (0.0 != rot.x) or (0.0 != rot.y) or (0.0 != rot.z):
                        file.write("        rot  = [{} {} {} {}]\n".format(- rot.x, - rot.y, - rot.z, rot.w))

                    if (1.0 != scl.x) or (1.0 != scl.y) or (1.0 != scl.z):
                        scl = (scl.x + scl.y + scl.z) / 3.0
                        file.write("        scl  = {}\n".format(scl))

                    file.write("    )\n\n")

            text = "Proxies exporting success!"
            self.report({"INFO"}, text)
            print("-" * 64)
            print("[KAO2] " + text)

            return {"FINISHED"}

        except Exception as e:

            traceback.print_exc()
            self.report({"ERROR"}, str(e))

            return {"CANCELLED"}


################################################################
