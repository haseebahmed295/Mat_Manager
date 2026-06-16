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
        
        layout.label(text="Layout Style:")
        layout.prop(wm, "mat_display_type", expand=True)
        
        layout.separator()
        
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
        prefs = context.preferences.addons[__package__].preferences

        if self.bl_space_type == 'PROPERTIES':
            layout.label(text="MatShelf (Scene Tab)", icon='SCENE_DATA')
            layout.separator()

        # --- Section 1: Active Object Context ---
        if prefs.show_context_warning:
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
        
        # Category and Sorting
        col = layout.column(align=True)
        
        row_cat = col.row(align=True)
        row_cat.prop(wm, "mat_filter_category", text="Category")
        row_cat.prop(wm, "mat_show_sort_options", icon='THREE_DOTS', text="", icon_only=True)
        
        if wm.mat_show_sort_options:
            row_sort = col.row(align=True)
            row_sort.prop(wm, "mat_sort_method", text="Sort By")
            
        row_cat_ops = col.row(align=True)
        row_cat_ops.operator("material.edit_categories", text="Edit Categories", icon='PREFERENCES')
        row_cat_ops.operator("material.batch_assign_category", text="Batch Assign", icon='GROUP')
    
        # Tools row
        if prefs.show_utility_buttons:
            row_tools = col.row(align=True)
            row_tools.operator("material.merge_duplicates", text="Merge Duplicates", icon='AUTOMERGE_ON')
            row_tools.operator("material.purge_unused", text="Purge Unused", icon='TRASH')
            layout.separator()
        
        search_query = wm.mat_search_filter.lower()
        filter_category = wm.mat_filter_category

        # --- Section 3: The Material List / Grid ---
        is_grid = (wm.mat_display_type == 'GRID')
        
        if prefs.use_collapsible_panel:
            panel_header, panel_body = layout.panel("MATERIAL_PT_preview_subpanel", default_closed=False)
            panel_header.label(text="Materials Preview", icon='MATERIAL')
        else:
            panel_body = layout
        
        if panel_body is not None:
            if is_grid:
                container = panel_body.grid_flow(row_major=True, columns=wm.mat_grid_columns, even_columns=True, align=True)
            else:
                container = panel_body.column(align=True)
                
            match_count = 0
            
            # Sorting logic
            mats = list(bpy.data.materials)
            sort_method = wm.mat_sort_method
            if sort_method == 'NAME_ASC':
                mats.sort(key=lambda m: m.name.lower())
            elif sort_method == 'NAME_DESC':
                mats.sort(key=lambda m: m.name.lower(), reverse=True)
            elif sort_method == 'USERS_DESC':
                mats.sort(key=lambda m: m.users, reverse=True)
            elif sort_method == 'USERS_ASC':
                mats.sort(key=lambda m: m.users)

            for mat in mats:
                if search_query in mat.name.lower():
                    # Filter by category
                    if filter_category != 'ALL' and mat.mat_category != filter_category:
                        continue
                        
                    match_count += 1
                    mat.preview_ensure()
                    
                    if is_grid:
                        box = container.box()
                        
                        # The Thumbnail (Nice and large)
                        box.template_icon(icon_value=layout.icon(mat), scale=wm.mat_preview_scale)
                        
                        # The Material Name
                        box.label(text=mat.name)
                        
                        # Action Buttons Row
                        row = box.row(align=True)
                        op_assign = row.operator("material.assign_from_manager", text="Assign")
                        op_assign.mat_name = mat.name
                        
                        op_select = row.operator("material.ops_select_users", text="", icon='RESTRICT_SELECT_OFF')
                        op_select.mat_name = mat.name
                        
                        op_menu = row.operator("material.open_ops_menu", text="", icon='DOWNARROW_HLT')
                        op_menu.mat_name = mat.name
                    else:
                        # List view item
                        row = container.row(align=True)
                        
                        # Thumbnail and Name
                        row.template_icon(icon_value=layout.icon(mat), scale=1.0)
                        row.label(text=mat.name)
                        
                        # Action Buttons Row (Right aligned)
                        actions = row.row(align=True)
                        op_assign = actions.operator("material.assign_from_manager", text="", icon='CHECKMARK')
                        op_assign.mat_name = mat.name
                        
                        op_select = actions.operator("material.ops_select_users", text="", icon='RESTRICT_SELECT_OFF')
                        op_select.mat_name = mat.name
                        
                        op_menu = actions.operator("material.open_ops_menu", text="", icon='DOWNARROW_HLT')
                        op_menu.mat_name = mat.name

            if match_count == 0:
                panel_body.label(text="No materials found.", icon='INFO')
