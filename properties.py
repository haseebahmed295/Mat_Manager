import bpy
from .helpers import (
    get_filter_categories,
    get_material_categories,
    update_search_filter,
    update_category_filter,
    update_preview_shape
)

# Category item data block
class MATERIAL_PG_category_item(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Category Name", default="New Category")
    id_str: bpy.props.StringProperty(name="ID", default="")

def register_properties():
    bpy.types.WindowManager.mat_search_filter = bpy.props.StringProperty(
        name="Search",
        default="",
        description="Filter materials by name",
        options={'TEXTEDIT_UPDATE'},
        update=update_search_filter
    )
    bpy.types.WindowManager.mat_preview_scale = bpy.props.FloatProperty(
        name="Preview Size",
        default=3.0,
        min=1.0,
        max=6.0,
        description="Scale of the material preview thumbnails"
    )
    bpy.types.WindowManager.mat_grid_columns = bpy.props.IntProperty(
        name="Columns",
        default=3,
        min=1,
        max=8,
        description="Number of columns in the material grid"
    )
    bpy.types.WindowManager.mat_filter_category = bpy.props.EnumProperty(
        name="Filter Category",
        description="Filter materials by category",
        items=get_filter_categories,
        default=0,
        update=update_category_filter
    )
    bpy.types.WindowManager.mat_active_menu_name = bpy.props.StringProperty(
        name="Active Material Menu Name",
        default=""
    )
    bpy.types.WindowManager.mat_display_type = bpy.props.EnumProperty(
        name="Display Type",
        description="Choose how to display the materials",
        items=[
            ('GRID', "Grid", "Display as a grid of thumbnails", 'VIEWPANEL', 0),
            ('LIST', "List", "Display as a compact list", 'LINENUMBERS_OFF', 1)
        ],
        default='GRID',
        update=update_search_filter
    )
    bpy.types.WindowManager.mat_show_sort_options = bpy.props.BoolProperty(
        name="Show Sorting",
        description="Show advanced sorting options",
        default=False
    )
    bpy.types.WindowManager.mat_sort_method = bpy.props.EnumProperty(
        name="Sort By",
        description="Method to sort materials",
        items=[
            ('NAME_ASC', "Name (A-Z)", "Sort alphabetically A to Z", 'SORT_ALPHA', 0),
            ('NAME_DESC', "Name (Z-A)", "Sort alphabetically Z to A", 'SORT_ALPHA', 1),
            ('USERS_DESC', "Most Used", "Sort by number of users, highest first", 'GROUP', 2),
            ('USERS_ASC', "Least Used", "Sort by number of users, lowest first", 'GROUP', 3),
        ],
        default='NAME_ASC',
        update=update_search_filter
    )
    bpy.types.Material.mat_category = bpy.props.EnumProperty(
        name="Category",
        description="Category of the material",
        items=get_material_categories,
        default=0,
        update=update_category_filter
    )
    
    # Custom category list stored in scene (saves inside the .blend file)
    bpy.types.Scene.mat_categories_list = bpy.props.CollectionProperty(type=MATERIAL_PG_category_item)
    bpy.types.Scene.mat_categories_active_index = bpy.props.IntProperty(name="Active Category Index", default=0)
    bpy.types.Scene.mat_categories_initialized = bpy.props.BoolProperty(default=False)
    
    # Custom preview shape property stored in scene (saves inside the .blend file)
    bpy.types.Scene.mat_preview_shape = bpy.props.EnumProperty(
        name="Preview Shape",
        description="Choose the shape used for the material preview icon",
        items=[
            ('SPHERE', "Sphere", "Sphere preview shape", 'SPHERE', 0),
            ('CUBE', "Cube", "Cube preview shape", 'CUBE', 1),
            ('SHADERBALL', "Shader Ball", "Shader ball preview shape", 'MATERIAL', 2),
            ('FLAT', "Flat", "Flat XY plane preview shape", 'SURFACE', 3),
            ('HAIR', "Hair", "Hair strands preview shape", 'STRAND', 4),
            ('CLOTH', "Cloth", "Cloth preview shape", 'MOD_CLOTH', 5),
            ('FLUID', "Fluid", "Fluid preview shape", 'MOD_FLUID', 6),
        ],
        default='SPHERE',
        update=update_preview_shape
    )

def unregister_properties():
    del bpy.types.WindowManager.mat_search_filter
    del bpy.types.WindowManager.mat_preview_scale
    del bpy.types.WindowManager.mat_grid_columns
    del bpy.types.WindowManager.mat_filter_category
    del bpy.types.WindowManager.mat_active_menu_name
    del bpy.types.WindowManager.mat_display_type
    del bpy.types.WindowManager.mat_show_sort_options
    del bpy.types.WindowManager.mat_sort_method
    del bpy.types.Material.mat_category
    del bpy.types.Scene.mat_categories_list
    del bpy.types.Scene.mat_categories_active_index
    del bpy.types.Scene.mat_categories_initialized
    del bpy.types.Scene.mat_preview_shape
