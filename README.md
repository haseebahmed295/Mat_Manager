# MatShelf

A visual material shelf and organization addon for Blender.

## Features
- **Visual Gallery**: Real-time thumbnail previews in a collapsible panel.
- **List & Grid Views**: Toggle between a compact list or a multi-column grid layout.
- **Advanced Sorting**: Sort materials by Name (A-Z, Z-A) or by Usage Count (Most/Least Used).
- **Search & Filters**: Search on-type and filter by custom categories.
- **Category Manager**: Add, remove, rename categories, and batch-assign filtered materials to them.
- **Smart Assignment**: Apply materials to selected objects in Object mode, or to selected faces in Edit mode using `bmesh`.
- **Operations Menu (`▼`)**: Rename, Select Users, Duplicate, Delete, and Set Category per material.
- **Cleanup Utilities**: Merge duplicate materials (`.001`, `.002`) and Purge unused data.
- **Global Preferences**: Fully personalize the UI. Choose the panel location (3D Viewport, Shader Editor, Properties Scene Tab), hide utility tools for a minimalist look, and toggle the collapsible container.

## Installation
1. Zip the `Mat_Manager` folder (containing `__init__.py`, `blender_manifest.toml`, `properties.py`, `operators.py`, `ui.py`, and `helpers.py`).
2. In Blender, go to **Edit > Preferences > Get Extensions**.
3. Click the cog menu at the top-right and select **Install from Disk...**.
4. Select the zip file and click install.

## Usage
1. Depending on your Add-on preferences, open the **3D Viewport**, **Shader Editor**, or **Scene Properties**.
2. Press `N` to toggle the Sidebar (if placed in a viewport).
3. Open the **MatShelf** tab.
