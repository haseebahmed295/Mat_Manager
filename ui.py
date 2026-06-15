import bpy

# Category UI List class
class MATERIAL_UL_categories(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='MATERIAL')

# Settings popover panel
class MATERIAL_PT_refined_settings_popover(bpy.types.Panel):
    bl_label = "Gallery Settings"
    bl_idname = "MATERIAL_PT_refined_settings_popover"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'INSTANCED'}
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        scene = context.scene
        
        layout.label(text="Grid Settings:")
        row = layout.row(align=True)
        row.prop(wm, "mat_grid_columns", text="Columns")
        row.prop(wm, "mat_preview_scale", text="Size")
        
        layout.separator()
        layout.label(text="Preview Shape:")
        layout.prop(scene, "mat_preview_shape", text="Shape")

# The operations menu
class MATERIAL_MT_operations_menu(bpy.types.Menu):
    bl_label = "Material Operations"
    bl_idname = "MATERIAL_MT_operations_menu"
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        wm = context.window_manager
        mat_name = wm.mat_active_menu_name
        
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            return
            
        layout.label(text=f"Material: {mat_name}")
        layout.separator()
        
        # Category assignment dropdown inside the menu (aligned)
        layout.prop_menu_enum(mat, "mat_category", text="Set Category", icon='FILTER')
        layout.separator()
        
        op = layout.operator("material.rename", text="Rename", icon='TEXT')
        op.old_name = mat_name
        
        op = layout.operator("material.ops_select_users", text="Select Users", icon='RESTRICT_SELECT_OFF')
        op.mat_name = mat_name
        
        op = layout.operator("material.ops_duplicate", text="Duplicate", icon='DUPLICATE')
        op.mat_name = mat_name
        
        op = layout.operator("material.ops_delete", text="Delete", icon='TRASH')
        op.mat_name = mat_name

# The Refined Panel
class MATERIAL_PT_refined_manager(bpy.types.Panel):
    bl_label = "Material Gallery"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MatShelf"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        obj = context.active_object

        # --- Section 1: Active Object Context ---
        box = layout.box()
        if obj:
            if obj.active_material:
                box.label(text=f"Current: {obj.active_material.name}", icon='MATERIAL')
            else:
                box.label(text=f"{obj.name} has no material", icon='ERROR')
        else:
            box.label(text="No object selected", icon='INFO')

        # --- Section 2: Search Bar & Settings ---
        row_search = layout.row(align=True)
        row_search.scale_y = 1.4
        row_search.prop(wm, "mat_search_filter", icon='VIEWZOOM', text="")
        row_search.popover(panel="MATERIAL_PT_refined_settings_popover", text="", icon='SETTINGS')
        
        row_cat = layout.row(align=True)
        row_cat.prop(wm, "mat_filter_category", text="Category")
        row_cat.operator("material.edit_categories", text="", icon='PREFERENCES')
        
        # Tools row
        row_tools = layout.row(align=True)
        row_tools.operator("material.merge_duplicates", text="Merge Duplicates", icon='AUTOMERGE_ON')
        row_tools.operator("material.purge_unused", text="Purge Unused", icon='TRASH')
        
        layout.separator()
        search_query = wm.mat_search_filter.lower()
        filter_category = wm.mat_filter_category

        # --- Section 3: The Material Grid ---
        grid = layout.grid_flow(row_major=True, columns=wm.mat_grid_columns, even_columns=True, align=True)
        
        match_count = 0

        for mat in bpy.data.materials:
            if search_query in mat.name.lower():
                # Filter by category
                if filter_category != 'ALL' and mat.mat_category != filter_category:
                    continue
                    
                match_count += 1
                col = grid.column(align=True)
                
                # Ensure the preview is generated/loaded
                mat.preview_ensure()
                
                # The Thumbnail
                col.template_icon(icon_value=layout.icon(mat), scale=wm.mat_preview_scale)
                
                # The Material Name
                col.label(text=mat.name)
                
                # The Working Assign Button & Operations Dropdown
                row = col.row(align=True)
                op = row.operator("material.assign_from_manager", text="Assign")
                op.mat_name = mat.name
                
                op_menu = row.operator("material.open_ops_menu", text="", icon='DOWNARROW_HLT')
                op_menu.mat_name = mat.name

        if match_count == 0:
            layout.label(text="No materials found.", icon='INFO')
