bl_info = {
    "name": "MatShelf",
    "author": "haseebahmed295",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3D View > Sidebar > MatShelf",
    "description": "Manage and assign materials from a visual grid gallery shelf",
    "warning": "",
    "doc_url": "",
    "category": "Material",
}

import bpy

# Support reload of sub-modules when reloading scripts in Blender
if "bpy" in locals():
    import importlib
    if "helpers" in locals():
        importlib.reload(helpers)
    if "properties" in locals():
        importlib.reload(properties)
    if "operators" in locals():
        importlib.reload(operators)
    if "ui" in locals():
        importlib.reload(ui)

from . import helpers
from . import properties
from . import operators
from . import ui

# Explicitly import classes for registration
from .properties import (
    MATERIAL_PG_category_item,
    register_properties,
    unregister_properties
)
from .ui import (
    MATERIAL_UL_categories,
    MATERIAL_PT_refined_settings_popover,
    MATERIAL_MT_operations_menu,
    MATERIAL_PT_refined_manager
)
from .operators import (
    MATERIAL_OT_category_add,
    MATERIAL_OT_category_remove,
    MATERIAL_OT_edit_categories,
    MATERIAL_OT_assign_from_manager,
    MATERIAL_OT_open_ops_menu,
    MATERIAL_OT_ops_select_users,
    MATERIAL_OT_ops_duplicate,
    MATERIAL_OT_ops_delete,
    MATERIAL_OT_rename,
    MATERIAL_OT_merge_duplicates,
    MATERIAL_OT_purge_unused
)

classes = [
    MATERIAL_PG_category_item,
    MATERIAL_UL_categories,
    MATERIAL_OT_category_add,
    MATERIAL_OT_category_remove,
    MATERIAL_OT_edit_categories,
    MATERIAL_OT_assign_from_manager,
    MATERIAL_OT_open_ops_menu,
    MATERIAL_OT_ops_select_users,
    MATERIAL_OT_ops_duplicate,
    MATERIAL_OT_ops_delete,
    MATERIAL_OT_rename,
    MATERIAL_OT_merge_duplicates,
    MATERIAL_OT_purge_unused,
    MATERIAL_MT_operations_menu,
    MATERIAL_PT_refined_settings_popover,
    MATERIAL_PT_refined_manager
]

def register():
    # 1. Register UI List and other classes first so types are available in RNA
    for cls in classes:
        bpy.utils.register_class(cls)

    # 2. Register properties (e.g. Scene, WindowManager, Material properties)
    register_properties()

def unregister():
    # 1. Unregister properties first
    unregister_properties()

    # 2. Unregister classes in reverse order
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
