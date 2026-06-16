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
    MATERIAL_OT_purge_unused,
    MATERIAL_OT_batch_assign_category
)

class MATERIAL_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def update_panel_location(self, context):
        from .ui import MATERIAL_PT_refined_manager
        
        try:
            bpy.utils.unregister_class(MATERIAL_PT_refined_manager)
        except Exception:
            pass
            
        space = self.panel_space
        if space == 'VIEW_3D':
            MATERIAL_PT_refined_manager.bl_space_type = 'VIEW_3D'
            MATERIAL_PT_refined_manager.bl_region_type = 'UI'
            if hasattr(MATERIAL_PT_refined_manager, 'bl_context'):
                delattr(MATERIAL_PT_refined_manager, 'bl_context')
        elif space == 'NODE_EDITOR':
            MATERIAL_PT_refined_manager.bl_space_type = 'NODE_EDITOR'
            MATERIAL_PT_refined_manager.bl_region_type = 'UI'
            if hasattr(MATERIAL_PT_refined_manager, 'bl_context'):
                delattr(MATERIAL_PT_refined_manager, 'bl_context')
        elif space == 'PROPERTIES':
            MATERIAL_PT_refined_manager.bl_space_type = 'PROPERTIES'
            MATERIAL_PT_refined_manager.bl_region_type = 'WINDOW'
            MATERIAL_PT_refined_manager.bl_context = 'scene'
            
        try:
            bpy.utils.register_class(MATERIAL_PT_refined_manager)
        except Exception as e:
            print(f"Mat_Manager: Could not re-register panel: {e}")

    panel_space: bpy.props.EnumProperty(
        name="Panel Location",
        items=[
            ('VIEW_3D', "3D Viewport", "Sidebar of 3D Viewport"),
            ('NODE_EDITOR', "Shader Editor", "Sidebar of Shader Editor"),
            ('PROPERTIES', "Properties (Scene Tab)", "Scene tab in Properties Editor")
        ],
        default='VIEW_3D',
        update=update_panel_location
    )
    
    show_utility_buttons: bpy.props.BoolProperty(
        name="Show Merge & Purge Tools",
        description="Show the Merge Duplicates and Purge Unused buttons in the UI",
        default=True
    )
    
    show_context_warning: bpy.props.BoolProperty(
        name="Show Active Object Context",
        description="Show the box at the top displaying the active object and its material",
        default=True
    )
    
    use_collapsible_panel: bpy.props.BoolProperty(
        name="Use Collapsible Panel",
        description="Wrap the material gallery in a collapsible panel",
        default=True
    )
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="UI Layout & Placement", icon='WINDOW')
        box.prop(self, "panel_space")
        
        box = layout.box()
        box.label(text="Minimalist UI Toggles", icon='RESTRICT_VIEW_OFF')
        box.prop(self, "show_utility_buttons")
        box.prop(self, "show_context_warning")
        box.prop(self, "use_collapsible_panel")

classes = [
    MATERIAL_AddonPreferences,
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
    MATERIAL_OT_batch_assign_category,
    MATERIAL_MT_operations_menu,
    MATERIAL_PT_refined_settings_popover,
    MATERIAL_PT_refined_manager
]

from bpy.app.handlers import persistent

@persistent
def load_post_handler(dummy):
    # Initialize defaults for the active scene when loading a file
    context = bpy.context
    if hasattr(context, "scene") and context.scene:
        from .helpers import init_default_categories
        init_default_categories(context.scene)

def register():
    # 1. Register all classes except the main panel
    for cls in classes:
        if cls.__name__ != 'MATERIAL_PT_refined_manager':
            bpy.utils.register_class(cls)

    # 2. Apply saved panel location preference BEFORE registering the panel class
    prefs = bpy.context.preferences.addons.get(__package__)
    if prefs and getattr(prefs, 'preferences', None):
        space = prefs.preferences.panel_space
        if space == 'VIEW_3D':
            MATERIAL_PT_refined_manager.bl_space_type = 'VIEW_3D'
            MATERIAL_PT_refined_manager.bl_region_type = 'UI'
        elif space == 'NODE_EDITOR':
            MATERIAL_PT_refined_manager.bl_space_type = 'NODE_EDITOR'
            MATERIAL_PT_refined_manager.bl_region_type = 'UI'
        elif space == 'PROPERTIES':
            MATERIAL_PT_refined_manager.bl_space_type = 'PROPERTIES'
            MATERIAL_PT_refined_manager.bl_region_type = 'WINDOW'
            MATERIAL_PT_refined_manager.bl_context = 'scene'

    # 3. Now register the main panel with correct attributes
    bpy.utils.register_class(MATERIAL_PT_refined_manager)

    # 2. Register properties (e.g. Scene, WindowManager, Material properties)
    register_properties()

    # 3. Register load handler
    bpy.app.handlers.load_post.append(load_post_handler)

    # 4. Initialize for current scene if available
    if hasattr(bpy.context, "scene") and bpy.context.scene:
        from .helpers import init_default_categories
        try:
            init_default_categories(bpy.context.scene)
        except Exception as e:
            print(f"Mat_Manager: Could not initialize categories during register: {e}")

def unregister():
    # 1. Unregister properties first
    unregister_properties()

    # 2. Unregister classes in reverse order
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # 3. Unregister load handler
    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)

if __name__ == "__main__":
    register()
