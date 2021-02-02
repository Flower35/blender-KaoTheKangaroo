################################################################
# "KAO2/TypeInfo.py"

from typing import Callable


class KAO2_TypeInfo(object):

    staticListOfTypes = []

    def __init__(self, index: int, name: str, parent: "KAO2_TypeInfo", create: Callable[[], "KAO2_eObject"]) -> None:

        #@@ print("[KAO2] TypeInfo(0x{:08X}, \"{}\")".format(index, name))

        self.index = index
        self.name = name
        self.parent = parent
        self.create = create

    def checkHierarchy(self, other_info: "KAO2_TypeInfo") -> bool:

        my_info = self

        while my_info is not None:

            if my_info == other_info:

                return True

            my_info = my_info.parent

        return False

    @staticmethod
    def registerTypeInfo(new_info: "KAO2_TypeInfo") -> None:

        for info in KAO2_TypeInfo.staticListOfTypes:

            if info.name == new_info.name:
                raise Exception("[KAO2] TypeInfo::registerTypeInfo():\n\t" + "interface \"{}\" is duplicated".format(new_info.name))

            if info.index == new_info.index:
                raise Exception("[KAO2] TypeInfo::registerTypeInfo():\n\t" + "interface \"{}\" has duplicated index 0x{:08X} (see interface \"{}\").".format(new_info.name, new_info.index, info.name))

        KAO2_TypeInfo.staticListOfTypes.append(new_info)

    @staticmethod
    def getTypeInfo(index: int) -> "KAO2_TypeInfo":

        for info in KAO2_TypeInfo.staticListOfTypes:

            if info.index == index:

                return info

        raise Exception("[KAO2] TypeInfo::getTypeInfo():\n\t" + "TypeInfo for Index 0x{:08X} not found!".format(index))

    @staticmethod
    def register() -> None:

        from .eSpline3D import KAO2_E_SPLINE3D_TYPEINFO
        from .eBezierSplineNode import KAO2_E_BEZIERSPLINENODE_TYPEINFO
        from .eALBox import KAO2_E_ALBOX_TYPEINFO
        from .eAmbientLight import KAO2_E_AMBIENTLIGHT_TYPEINFO
        from .eDirectionalLight import KAO2_E_DIRECTIONALLIGHT_TYPEINFO
        from .eSoundCtrl import KAO2_E_SOUNDCTRL_TYPEINFO
        from .eSndEmiterAmb import KAO2_E_SNDEMITERAMB_TYPEINFO
        from .eSndEmiterOmni import KAO2_E_SNDEMITEROMNI_TYPEINFO
        from .eLeafCtrl import (KAO2_E_LEAFCTRL_FLOAT_TYPEINFO, KAO2_E_LEAFCTRL_POINT3_TYPEINFO, KAO2_E_LEAFCTRL_QUAT_TYPEINFO)
        from .eSRPCombineCtrl import KAO2_E_SRPCOMBINECTRL_TYPEINFO
        from .eXYZEulerRotation import KAO2_E_XYZEULERROTATION_TYPEINFO
        from .eXYZPoint3Ctrl import KAO2_E_XYZPOINT3CTRL_TYPEINFO
        from .eMultiCtrl import (KAO2_E_MULTICTRL_SRP_TYPEINFO, KAO2_E_MULTICTRL_FLOAT_TYPEINFO)
        from .eGeoArray import (KAO2_E_GEOARRAY_USHORT_TYPEINFO, KAO2_E_GEOARRAY_POINT2_TYPEINFO, KAO2_E_GEOARRAY_POINT4_TYPEINFO, KAO2_E_GEOARRAY_ABB_TYPEINFO, KAO2_E_GEOARRAY_PHYVERTEX_TYPEINFO)
        from .eBitmap import KAO2_E_BITMAP_TYPEINFO
        from .eTexture import KAO2_E_TEXTURE_TYPEINFO
        from .eTexTransform import KAO2_E_TEXTRANSFORM_TYPEINFO
        from .eMaterialState import KAO2_E_MATERIALSTATE_TYPEINFO
        from .eMaterial import KAO2_E_MATERIAL_TYPEINFO
        from .eGeoSet import KAO2_E_GEOSET_TYPEINFO
        from .eTriMesh import KAO2_E_TRIMESH_TYPEINFO
        from .ePhyTriMesh import KAO2_E_PHYTRIMESH_TYPEINFO
        from .eGroup import KAO2_E_GROUP_TYPEINFO
        from .eTransform import KAO2_E_TRANSFORM_TYPEINFO
        from .eBillboard import KAO2_E_BILLBOARD_TYPEINFO
        from .eCamera import KAO2_E_CAMERA_TYPEINFO
        from .ePathCamCtrl import KAO2_E_PATHCAMCTRL_TYPEINFO
        from .eAnimState import KAO2_E_ANIMSTATE_TYPEINFO
        from .eTrack import KAO2_E_TRACK_TYPEINFO
        from .ePivot import KAO2_E_PIVOT_TYPEINFO
        from .Actor import KAO2_ACTOR_TYPEINFO
        from .eProxy import KAO2_E_PROXY_TYPEINFO
        from .eFogEnv import KAO2_E_FOGENV_TYPEINFO
        from .eEnvironment import KAO2_E_ENVIRONMENT_TYPEINFO
        from .eScene import KAO2_E_SCENE_TYPEINFO

        KAO2_TypeInfo.registerTypeInfo(KAO2_E_SPLINE3D_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_BEZIERSPLINENODE_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_ALBOX_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_AMBIENTLIGHT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_DIRECTIONALLIGHT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_SOUNDCTRL_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_SNDEMITERAMB_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_SNDEMITEROMNI_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_LEAFCTRL_FLOAT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_LEAFCTRL_POINT3_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_LEAFCTRL_QUAT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_SRPCOMBINECTRL_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_XYZEULERROTATION_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_XYZPOINT3CTRL_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_MULTICTRL_SRP_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_MULTICTRL_FLOAT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GEOARRAY_USHORT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GEOARRAY_POINT2_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GEOARRAY_POINT4_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GEOARRAY_ABB_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GEOARRAY_PHYVERTEX_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_BITMAP_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_TEXTURE_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_TEXTRANSFORM_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_MATERIALSTATE_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_MATERIAL_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GEOSET_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_TRIMESH_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_PHYTRIMESH_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_GROUP_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_TRANSFORM_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_BILLBOARD_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_CAMERA_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_PATHCAMCTRL_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_ANIMSTATE_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_TRACK_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_PIVOT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_ACTOR_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_PROXY_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_FOGENV_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_ENVIRONMENT_TYPEINFO)
        KAO2_TypeInfo.registerTypeInfo(KAO2_E_SCENE_TYPEINFO)

        print("-" * 64)
        print("[KAO2] TypeInfo::register():\n\t" + "{} \"AR\" interfaces.".format(len(KAO2_TypeInfo.staticListOfTypes)))

    @staticmethod
    def unregister() -> None:

        del KAO2_TypeInfo.staticListOfTypes[:]

        print("-" * 64)
        print("[KAO2] TypeInfo::unregister() called.")


################################################################
