import bpy

DEFAULTS = ["Metal", "Wood", "Glass", "Plastic", "Fabric", "Organic", "Paint", "Other"]

def init_default_categories(scene):
    if not scene.mat_categories_initialized:
        for idx, name in enumerate(DEFAULTS):
            item = scene.mat_categories_list.add()
            item.name = name
            item.id_str = f"cat_{idx}_{name.lower()}"
        scene.mat_categories_initialized = True

def get_material_categories(self, context):
    items = [('NONE', "Unassigned", "No category assigned")]
    if context and hasattr(context, "scene") and context.scene:
        scene = context.scene
        if scene.mat_categories_initialized:
            for cat in scene.mat_categories_list:
                if cat.name.strip():
                    items.append((cat.id_str, cat.name, f"Category: {cat.name}"))
        else:
            for idx, name in enumerate(DEFAULTS):
                id_str = f"cat_{idx}_{name.lower()}"
                items.append((id_str, name, f"Category: {name}"))
    return items

def get_filter_categories(self, context):
    items = [('ALL', "All", "Show all materials", 'FILTER', 0)]
    items.append(('NONE', "Unassigned", "Show unassigned materials", 'QUESTION', 1))
    if context and hasattr(context, "scene") and context.scene:
        scene = context.scene
        if scene.mat_categories_initialized:
            for idx, cat in enumerate(scene.mat_categories_list):
                if cat.name.strip():
                    items.append((cat.id_str, cat.name, f"Category: {cat.name}", 'MATERIAL', idx + 2))
        else:
            for idx, name in enumerate(DEFAULTS):
                id_str = f"cat_{idx}_{name.lower()}"
                items.append((id_str, name, f"Category: {name}", 'MATERIAL', idx + 2))
    return items

def update_preview_shape(self, context):
    shape = self.mat_preview_shape
    # Update all materials in the file
    for mat in bpy.data.materials:
        if mat.preview_render_type != shape:
            try:
                mat.preview_render_type = shape
                mat.preview_ensure()
            except Exception as e:
                print(f"Mat_Manager: Could not set preview shape for {mat.name}: {e}")
            
    # Redraw all 3D Viewport areas to update the panel instantly
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

def update_search_filter(self, context):
    # Redraw all 3D Viewport areas to update the panel instantly on keystroke
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

def update_category_filter(self, context):
    # Redraw all 3D Viewport areas to update the panel instantly on category change
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
