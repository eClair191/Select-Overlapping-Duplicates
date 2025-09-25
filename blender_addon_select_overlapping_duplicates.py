bl_info = {
    "name": "Select Overlapping Duplicates",
    "author": "eClair",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Select > Select Overlapping Duplicates",
    "description": "Compare two collections and select overlapping duplicate objects based on vertex count and proximity",
    "category": "Object",
}

import bpy
from mathutils import Vector

def get_bbox_center(obj):
    """Get the center of the bounding box in world space"""
    bbox_corners = [obj.matrix_world @ Vector(vertex) for vertex in obj.bound_box]
    center = Vector((0, 0, 0))
    for corner in bbox_corners:
        center += corner
    center /= len(bbox_corners)
    return center

def get_vert_count(obj):
    """Get vertex count for mesh objects"""
    if obj.type == 'MESH':
        return len(obj.data.vertices)
    return None

def get_collection_items(self, context):
    """Generate collection list for enum property"""
    items = []
    for i, col in enumerate(bpy.data.collections):
        items.append((col.name, col.name, f"{len(col.objects)} objects", i))
    return items if items else [('NONE', 'No Collections', 'No collections available', 0)]

class OBJECT_OT_compare_collections(bpy.types.Operator):
    """Compare two collections for overlapping duplicate objects"""
    bl_idname = "object.compare_collections_duplicates"
    bl_label = "Select Overlapping Duplicates"
    bl_options = {'REGISTER', 'UNDO'}
    
    collection_1: bpy.props.EnumProperty(
        name="First Collection",
        description="First collection to compare",
        items=get_collection_items
    )
    
    collection_2: bpy.props.EnumProperty(
        name="Second Collection",
        description="Second collection to compare",
        items=get_collection_items
    )
    
    select_from: bpy.props.EnumProperty(
        name="Select Duplicates From",
        description="Which collection to select matching objects from",
        items=[
            ('FIRST', 'First Collection', 'Select duplicates from first collection'),
            ('SECOND', 'Second Collection', 'Select duplicates from second collection')
        ],
        default='SECOND'
    )
    
    threshold: bpy.props.FloatProperty(
        name="Distance Threshold",
        description="Maximum distance between centers to consider objects as duplicates",
        default=0.1,
        min=0.0001,
        max=100.0,
        precision=4
    )
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "collection_1")
        layout.prop(self, "collection_2")
        layout.prop(self, "select_from")
        layout.prop(self, "threshold")
    
    def execute(self, context):
        # Validate collections exist
        if self.collection_1 not in bpy.data.collections:
            self.report({'ERROR'}, f"Collection '{self.collection_1}' not found")
            return {'CANCELLED'}
        
        if self.collection_2 not in bpy.data.collections:
            self.report({'ERROR'}, f"Collection '{self.collection_2}' not found")
            return {'CANCELLED'}
        
        if self.collection_1 == self.collection_2:
            self.report({'ERROR'}, "Please select two different collections")
            return {'CANCELLED'}
        
        collection_1 = bpy.data.collections[self.collection_1]
        collection_2 = bpy.data.collections[self.collection_2]
        
        # Determine which collection to select from
        select_col = collection_2 if self.select_from == 'SECOND' else collection_1
        
        objects_to_select = []
        
        print("\n" + "="*70)
        print(f"Comparing Collections for Duplicates")
        print(f"First: '{collection_1.name}' | Second: '{collection_2.name}'")
        print(f"Selecting from: '{select_col.name}' | Threshold: {self.threshold}")
        print("="*70)
        
        # Compare every object in collection 1 with every object in collection 2
        for obj1 in collection_1.objects:
            vert_count_1 = get_vert_count(obj1)
            if vert_count_1 is None:
                continue
            
            center_1 = get_bbox_center(obj1)
            
            for obj2 in collection_2.objects:
                vert_count_2 = get_vert_count(obj2)
                if vert_count_2 is None:
                    continue
                
                # Check same vertex count
                if vert_count_1 == vert_count_2:
                    center_2 = get_bbox_center(obj2)
                    distance = (center_1 - center_2).length
                    
                    # Check distance threshold
                    if distance < self.threshold:
                        # Select the object from the target collection
                        if self.select_from == 'SECOND':
                            target_obj = obj2
                        else:
                            target_obj = obj1
                        
                        if target_obj not in objects_to_select:
                            objects_to_select.append(target_obj)
                            print(f"Match: '{obj1.name}' ↔ '{obj2.name}' | Verts: {vert_count_1} | Distance: {distance:.4f}")
        
        # Deselect all and select matches
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects_to_select:
            obj.select_set(True)
        
        print("="*70)
        print(f"Total duplicates found: {len(objects_to_select)}")
        if objects_to_select:
            print(f"Selected: {[obj.name for obj in objects_to_select]}")
        print("="*70 + "\n")
        
        self.report({'INFO'}, f"Found {len(objects_to_select)} duplicate(s)")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_compare_collections.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_compare_collections)
    bpy.types.VIEW3D_MT_select_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_compare_collections)
    bpy.types.VIEW3D_MT_select_object.remove(menu_func)

if __name__ == "__main__":
    register()