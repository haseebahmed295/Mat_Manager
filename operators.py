import bpy
import time

# Category Add Operator
class MATERIAL_OT_category_add(bpy.types.Operator):
    """Add a new category to the list"""
    bl_idname = "material.category_add"
    bl_label = "Add Category"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        scene = context.scene
        item = scene.mat_categories_list.add()
        item.name = "New Category"
        item.id_str = f"cat_{int(time.time())}"
        scene.mat_categories_active_index = len(scene.mat_categories_list) - 1
        return {'FINISHED'}

# Category Remove Operator
class MATERIAL_OT_category_remove(bpy.types.Operator):
    """Remove the active category from the list"""
    bl_idname = "material.category_remove"
    bl_label = "Remove Category"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        scene = context.scene
        idx = scene.mat_categories_active_index
        if idx >= 0 and idx < len(scene.mat_categories_list):
            scene.mat_categories_list.remove(idx)
            scene.mat_categories_active_index = min(max(0, idx - 1), len(scene.mat_categories_list) - 1)
            
            # Redraw viewports to update filtering immediately
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
        return {'FINISHED'}

# Category Edit Dialog Operator
class MATERIAL_OT_edit_categories(bpy.types.Operator):
    """Manage and edit material categories"""
    bl_idname = "material.edit_categories"
    bl_label = "Edit Categories"
    bl_options = {'REGISTER', 'UNDO'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        col = row.column()
        col.template_list("MATERIAL_UL_categories", "", scene, "mat_categories_list", scene, "mat_categories_active_index")
        
        col_btns = row.column(align=True)
        col_btns.operator("material.category_add", icon='ADD', text="")
        col_btns.operator("material.category_remove", icon='REMOVE', text="")
        
    def execute(self, context):
        # Force panel redrawing when editing is complete
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=350)

# The Custom Operator to Assign Materials
class MATERIAL_OT_assign_from_manager(bpy.types.Operator):
    """Assigns the selected material to all selected objects"""
    bl_idname = "material.assign_from_manager"
    bl_label = "Assign Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    mat_name: bpy.props.StringProperty()
    
    def execute(self, context):
        selected_objs = [obj for obj in context.selected_objects if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT'}]
        
        if not selected_objs:
            self.report({'WARNING'}, "Please select at least one valid object first!")
            return {'CANCELLED'}
            
        mat = bpy.data.materials.get(self.mat_name)
        if not mat:
            return {'CANCELLED'}
            
        for obj in selected_objs:
            if len(obj.material_slots) > 0:
                obj.material_slots[obj.active_material_index].material = mat
            else:
                obj.data.materials.append(mat)
            
        return {'FINISHED'}

# Operator to open the operations menu
class MATERIAL_OT_open_ops_menu(bpy.types.Operator):
    """Open the operations menu for this material"""
    bl_idname = "material.open_ops_menu"
    bl_label = "Material Options"
    bl_options = {'INTERNAL'}
    
    mat_name: bpy.props.StringProperty()
    
    def execute(self, context):
        context.window_manager.mat_active_menu_name = self.mat_name
        bpy.ops.wm.call_menu(name="MATERIAL_MT_operations_menu")
        return {'FINISHED'}

# Operator to select all users of a material
class MATERIAL_OT_ops_select_users(bpy.types.Operator):
    """Select all objects using this material"""
    bl_idname = "material.ops_select_users"
    bl_label = "Select Users"
    bl_options = {'REGISTER', 'UNDO'}
    
    mat_name: bpy.props.StringProperty()
    
    def execute(self, context):
        mat = bpy.data.materials.get(self.mat_name)
        if not mat:
            return {'CANCELLED'}
            
        bpy.ops.object.select_all(action='DESELECT')
        
        count = 0
        for obj in context.scene.objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT'}:
                for slot in obj.material_slots:
                    if slot.material == mat:
                        obj.select_set(True)
                        context.view_layer.objects.active = obj
                        count += 1
                        break
                        
        if count > 0:
            self.report({'INFO'}, f"Selected {count} object(s) using {self.mat_name}")
        else:
            self.report({'WARNING'}, f"No objects in the scene are using {self.mat_name}")
            
        return {'FINISHED'}

# Operator to duplicate a material
class MATERIAL_OT_ops_duplicate(bpy.types.Operator):
    """Create a duplicate of this material"""
    bl_idname = "material.ops_duplicate"
    bl_label = "Duplicate"
    bl_options = {'REGISTER', 'UNDO'}
    
    mat_name: bpy.props.StringProperty()
    
    def execute(self, context):
        mat = bpy.data.materials.get(self.mat_name)
        if not mat:
            return {'CANCELLED'}
            
        new_mat = mat.copy()
        self.report({'INFO'}, f"Duplicated {self.mat_name} to {new_mat.name}")
        return {'FINISHED'}

# Operator to delete a material
class MATERIAL_OT_ops_delete(bpy.types.Operator):
    """Delete this material from the file"""
    bl_idname = "material.ops_delete"
    bl_label = "Delete Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    mat_name: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
        
    def execute(self, context):
        mat = bpy.data.materials.get(self.mat_name)
        if not mat:
            return {'CANCELLED'}
            
        bpy.data.materials.remove(mat)
        self.report({'INFO'}, f"Deleted material {self.mat_name}")
        return {'FINISHED'}

# Operator to rename a material from a dialog box
class MATERIAL_OT_rename(bpy.types.Operator):
    """Rename this material"""
    bl_idname = "material.rename"
    bl_label = "Rename Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    old_name: bpy.props.StringProperty()
    new_name: bpy.props.StringProperty(name="New Name")
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_name")
        
    def invoke(self, context, event):
        self.new_name = self.old_name
        return context.window_manager.invoke_props_dialog(self)
        
    def execute(self, context):
        mat = bpy.data.materials.get(self.old_name)
        if not mat:
            self.report({'WARNING'}, "Material not found!")
            return {'CANCELLED'}
            
        if not self.new_name.strip():
            self.report({'WARNING'}, "Name cannot be empty!")
            return {'CANCELLED'}
            
        old = mat.name
        mat.name = self.new_name
        self.report({'INFO'}, f"Renamed material '{old}' to '{mat.name}'")
        
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
                    
        return {'FINISHED'}

# Operator to merge duplicate materials
class MATERIAL_OT_merge_duplicates(bpy.types.Operator):
    """Finds duplicate materials ending in .001, .002, etc. and merges them back to their base material"""
    bl_idname = "material.merge_duplicates"
    bl_label = "Merge Duplicates"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        mats = bpy.data.materials
        merge_count = 0
        
        to_merge = []
        for mat in mats:
            if "." in mat.name:
                base_name, _, ext = mat.name.rpartition(".")
                if ext.isnumeric() and base_name in mats:
                    original_mat = mats[base_name]
                    to_merge.append((mat, original_mat))
                    
        for duplicate_mat, original_mat in to_merge:
            try:
                duplicate_mat.user_remap(original_mat)
                mats.remove(duplicate_mat)
                merge_count += 1
            except Exception as e:
                self.report({'ERROR'}, f"Failed to merge {duplicate_mat.name}: {str(e)}")
                
        if merge_count > 0:
            self.report({'INFO'}, f"Successfully merged {merge_count} duplicate material(s)!")
        else:
            self.report({'INFO'}, "No duplicate materials found to merge.")
            
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
                    
        return {'FINISHED'}

# Operator to purge unused materials
class MATERIAL_OT_purge_unused(bpy.types.Operator):
    """Deletes all materials with zero users (not assigned to any object or protected by Fake User)"""
    bl_idname = "material.purge_unused"
    bl_label = "Purge Unused Materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    do_local: bpy.props.BoolProperty(
        name="Local Data-blocks",
        description="Purge unused materials created in this file",
        default=True
    )
    do_linked: bpy.props.BoolProperty(
        name="Linked Data-blocks",
        description="Purge unused materials linked from external libraries",
        default=True
    )
    do_recursive: bpy.props.BoolProperty(
        name="Recursive Delete",
        description="Recursively purge materials that become unused after purging other data",
        default=True
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "do_local")
        layout.prop(self, "do_linked")
        layout.prop(self, "do_recursive")
        
    def invoke(self, context, event):
        unused_count = sum(1 for mat in bpy.data.materials if mat.users == 0)
        if unused_count == 0:
            self.report({'INFO'}, "No unused materials to purge.")
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, title="Purge Unused Data from This File", confirm_text="Delete")
        
    def execute(self, context):
        mats = bpy.data.materials
        purge_count = 0
        iterations = 10 if self.do_recursive else 1
        
        for _ in range(iterations):
            current_purge = 0
            to_remove = []
            for mat in mats:
                if mat.users == 0:
                    is_linked = mat.library is not None
                    if is_linked and not self.do_linked:
                        continue
                    if not is_linked and not self.do_local:
                        continue
                    to_remove.append(mat)
                    
            if not to_remove:
                break
                
            for mat in to_remove:
                try:
                    mats.remove(mat)
                    current_purge += 1
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to purge {mat.name}: {str(e)}")
            
            purge_count += current_purge
            if current_purge == 0:
                break
                
        if purge_count > 0:
            self.report({'INFO'}, f"Successfully purged {purge_count} unused material(s)!")
        else:
            self.report({'INFO'}, "No unused materials purged.")
            
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
                    
        return {'FINISHED'}
