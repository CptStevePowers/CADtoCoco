import bpy
import os, sys
from mathutils import Vector
import random as rd
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from common import math_util

def all_lights_off():
    all_lights = [obj for obj in bpy.data.lights]
    for light in all_lights:
        light.energy = 0

def unhide_all():
    for object in bpy.data.objects:
        object.hide_viewport = False

def hide_all(exclude=['LIGHT', 'CAMERA']):
    for object in bpy.data.objects:
        if object.type in exclude:
            continue
        object.hide_viewport = True

def fix_name(name):
    ret = os.path.splitext(name)[0]
    ret = ret.replace('_', ' ')
    return ret

def hide_other_objects(*argv):
    names = []
    for arg in argv:
        if not isinstance(arg, list):
            l_out = [arg]
        else:
            l_out = arg
        names += l_out

    names = list(map(fix_name, names))

    for object in bpy.data.objects:
        if (object.name not in names) or object.type != 'LIGHT' or object.type != 'CAMERA':
            object.hide_viewport = True

def import_stl_folder(input_dir):
    files = os.listdir(input_dir)
    for file in files:
        absolut = os.path.join(input_dir, file)
        bpy.ops.import_mesh.stl(
            filepath=absolut, axis_forward='Y', axis_up='Z')

def calcBoundingBox(objs):
    cornerApointsX = []
    cornerApointsY = []
    cornerApointsZ = []
    cornerBpointsX = []
    cornerBpointsY = []
    cornerBpointsZ = []

    for ob in objs:
        bbox_corners = [ob.matrix_world @
                        Vector(corner) for corner in ob.bound_box]
        cornerApointsX.append(bbox_corners[0].x)
        cornerApointsY.append(bbox_corners[0].y)
        cornerApointsZ.append(bbox_corners[0].z)
        cornerBpointsX.append(bbox_corners[6].x)
        cornerBpointsY.append(bbox_corners[6].y)
        cornerBpointsZ.append(bbox_corners[6].z)

    minA = Vector((min(cornerApointsX), min(
        cornerApointsY), min(cornerApointsZ)))
    maxB = Vector((max(cornerBpointsX), max(
        cornerBpointsY), max(cornerBpointsZ)))

    center_point = Vector(
        ((minA.x + maxB.x)/2, (minA.y + maxB.y)/2, (minA.z + maxB.z)/2))
    dimensions = Vector((maxB.x - minA.x, maxB.y - minA.y, maxB.z - minA.z))

    return center_point, dimensions

def center_objects(objs):
    center_point, _ = calcBoundingBox(objs)
    for obj in objs:
        obj.location -= center_point
        obj.rotation_euler = (0.0, 0.0, 0.0)

def unselect_all():
    for obj in bpy.data.objects:
        obj.select_set(False)

def select_objs(objs):
    unselect_all()
    for obj in objs:
        obj.select_set(True)

def rot_all(objs, angle, axis, center_override=[0.0, 0.0, 0.0]):
    unselect_all()
    select_objs(objs)

    bpy.ops.transform.rotate(
        value=angle, orient_axis=axis, center_override=center_override)
    unselect_all()

def rescale_all(objs, value=(1, 1, 1)):
    unselect_all()
    select_objs(objs)

    bpy.ops.transform.resize(value=value, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, True), mirror=True,
                            use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    unselect_all()

def update_camera(camera, focus_point=Vector((0.0, 0.0, 0.0)), distance=2.0):
    # Credit to J. Bakker at https://blender.stackexchange.com/questions/100414/how-to-set-camera-location-in-the-scene-while-pointing-towards-an-object-with-a
    '''
    Focus the camera to a focus point and place the camera at a specific distance from that
    focus point. The camera stays in a direct line with the focus point.

    :param camera: the camera object
    :type camera: bpy.types.object
    :param focus_point: the point to focus on (default=``mathutils.Vector((0.0, 0.0, 0.0))``)
    :type focus_point: mathutils.Vector
    :param distance: the distance to keep to the focus point (default=``10.0``)
    :type distance: float
    '''
    looking_direction = camera.location - focus_point
    rot_quat = looking_direction.to_track_quat('Z', 'Y')

    camera.rotation_euler = rot_quat.to_euler()
    # Use * instead of @ for Blender <2.8
    camera.location = rot_quat @ Vector((0.0, 0.0, distance))

def new_camera(name=''): # , location=Vector((0.0, 0.0, 0.0))): #FIXME: Location setting does not work somehow
    if name == '':
        name = 'Camera'
    camera_data = bpy.data.cameras.new(name=name)
    camera_object = bpy.data.objects.new(name, camera_data)
    bpy.context.scene.collection.objects.link(camera_object)
    return camera_object

def new_lamp(name='', location=(1,1,1), energy=30):
    if name == '':
        name = 'Point'
    light_data = bpy.data.lights.new(name=name, type='POINT')
    light_data.energy = energy

    light_object = bpy.data.objects.new(name=name, object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    bpy.context.view_layer.objects.active = light_object
    light_object.location = location
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    return light_object

def make_obj_grey(objs):
    if not isinstance(objs, list):
        objs = [objs]

    mat = bpy.data.materials.get("grey")
    for obj in objs:
        obj.data.materials.clear()
        obj.data.materials.append(mat)

def make_obj_green(objs):
    if not isinstance(objs, list):
        objs = [objs]

    mat = bpy.data.materials.get('green')
    for obj in objs:
        obj.data.materials.clear()
        obj.data.materials.append(mat)

def make_obj_black(objs):
    if not isinstance(objs, list):
        objs = [objs]

    mat = bpy.data.materials.get('black')
    for obj in objs:
        obj.data.materials.clear()
        obj.data.materials.append(mat)

def make_obj_transparent(objs):
    if not isinstance(objs, list):
        objs = [objs]
    mat = bpy.data.materials.get('transparent')
    for obj in objs:
        obj.data.materials.clear()
        obj.data.materials.append(mat)

def norm_and_center(mesh_objs):
    unhide_all()
    center, dims = calcBoundingBox(mesh_objs)
    select_objs(mesh_objs)
    resize_factor = 1 / max(dims)
    rescale_all(mesh_objs, (resize_factor, resize_factor, resize_factor))
    center_objects(mesh_objs)
    return center, dims

def get_filename(output_dir, assembly_name, mode, camera_name, suffix):
    return os.path.join(output_dir, '{0}-{1}-{2}-{3}.png'.format(assembly_name, mode, camera_name, suffix))

def create_cam_sphere(n_cams, cam_distance):
    new_cams = []
    points = math_util.point_sphere(n_cams, cam_distance)
    for p in points:
        v = Vector(p)
        c = new_camera()
        c.location = v
        update_camera(c, distance=cam_distance)
        new_cams.append(c)
    return new_cams

def create_light_sphere(n_lights, light_distance):
    lamps = []
    points = math_util.point_sphere(n_lights, light_distance)
    for p in points:
        lamps.append(new_lamp(location=p))
    return lamps

class RenderManager:
    def __init__(self, output_dir, components, assembly_name, cameras=None, lights=None, brightness_default=10, brightness_range=(0,200), light_colors_random=False, textures=None):
        assert os.path.exists(os.path.dirname(output_dir)), "{0} directory does not exist".format(os.path.dirname(output_dir))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.output_dir = output_dir
        self.components = components
        self.assembly_name = assembly_name
        self.cameras = cameras
        self.lights = lights
        self.light_colors_random = light_colors_random
        self.brightness_default = brightness_default
        self.brightness_range = brightness_range
        self.textures = textures

    def render_mask_image_set(self, camera, brightness=30):
        """Generates the necessary image set with green highlightes for each component to creat masks for the given camera. Returns the paths to the images.

        Args:
            camera (): Blender Camera Object to render image from
            brightness (int, optional): Brightness for the lamps used in the images. Defaults to 30.

        Returns:
            [string]: Paths to rendered images
        """

        # Set Camera
        bpy.context.scene.camera = camera

        # Make Scene bright enough for minimal shadows
        all_lights = [obj for obj in bpy.data.lights]
        for light in all_lights:
            light.energy = brightness

        # Render Image for each component with green highlight
        mesh_objs = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        make_obj_black(mesh_objs)
        paths = []
        mask_img_dir = os.path.join(self.output_dir, 'mask_images')
        if not os.path.exists(mask_img_dir):
            os.makedirs(mask_img_dir)
        for component in self.components:
            objs = [obj for obj in mesh_objs if obj.name in self.components[component]]
            make_obj_green(objs)
            file_path = get_filename(mask_img_dir,self.assembly_name,'mask_image_set',camera.name,component)
            bpy.data.scenes['Scene'].render.filepath = file_path
            bpy.ops.render.render(write_still=True)
            paths.append(file_path)
            print('For',component, 'saving green key image to', file_path)
            make_obj_black(objs)

        make_obj_grey(mesh_objs)
        return paths

    def generate_complete_mask_image_set(self,brightness=30):
        paths = {}
        for cam in self.cameras:
            paths[cam.name] = self.render_mask_image_set(cam, brightness)
        return paths

    def render_random_image(self, k_lights_max=None, k_textures_max=None, sub_folder=None):
        cam = rd.sample(self.cameras, 1)[0]
        if k_lights_max is None:
            k_lights_max = len(self.lights)
        k_lights = rd.randint(1,k_lights_max)
        lights = rd.sample(self.lights, k_lights)

        # textures = None
        # if self.textures is not None:
        #     if k_textures_max is None:
        #         k_textures_max = len(self.textures)
        #     k_textures = rd.randint(1, k_textures_max)
        #     textures = rd.sample(self.textures, k_textures)
        #TODO: add texture variation

        bpy.context.scene.camera = cam
        all_lights_off()
        brs = ''
        colors = []
        if 0.3 < rd.randint(0, 100):
            for i in range(k_lights + 1):
                if 0.5 < rd.randint(0, 100) and self.light_colors_random:
                    h = round(rd.randint(0, 100) / 100, 3)
                    s = round(rd.randint(50,100) / 100, 3)
                    v = round(rd.randint(30,100) / 100, 3)
                    colors.append((h,s,v))
                else:
                   colors.append((0,0,1))
        else:
            for i in range(k_lights + 1):
                colors.append((0,0,1))
        brs = []
        for i, light in enumerate(lights):
            br = rd.randint(self.brightness_range[0], self.brightness_range[1])
            light.energy = br
            light.color = colors[i]
            brs.append(br)
        light_id = 'L'+str(len(lights)).upper()+'_'+str(min(brs))+'_'+str(max(brs))
        file_dir = self.output_dir
        if sub_folder is not None:
            file_dir = os.path.join(self.output_dir, sub_folder)
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
        file_path = get_filename(file_dir,self.assembly_name,light_id,cam.name,'')
        bpy.data.scenes['Scene'].render.filepath = file_path
        bpy.ops.render.render(write_still=True)
        return file_path


def gen_data_set(output_dir, components, cam_objs, lamp_objs, assembly_name='test', light_default=50, light_range=(0,100), n_images=1000, part_train=0.7, part_val=0.2, part_test=0.1):
    renderManager = RenderManager(output_dir,
                                  components,
                                  assembly_name,
                                  cameras=cam_objs,
                                  lights=lamp_objs,
                                  light_colors_random=True,
                                  brightness_default=light_default,
                                  brightness_range=light_range)
    train_cams = rd.sample(cam_objs, round(part_train*len(cam_objs)))
    other = [obj for obj in cam_objs if obj not in train_cams]
    val_cams = rd.sample(other, round((part_val/(part_val+part_test))*len(other)))
    test_cams = [obj for obj in other if obj not in val_cams]
    val_cams += rd.sample(train_cams, round(0.1*len(train_cams))) #TODO: so okay? -> Überlagerung der Winkel Train und Val bei 10%
    print('Number of Cameras')
    print('train :', len(train_cams))
    print('val :', len(val_cams))
    print('test :', len(test_cams))

    renderManager.light_colors_random = False
    renderManager.generate_complete_mask_image_set()

    renderManager.light_colors_random = True
    renderManager.cameras = train_cams
    for i in range(round(n_images*part_train) + 1):
        renderManager.render_random_image(k_lights_max=10, sub_folder='train')

    renderManager.cameras = val_cams
    for i in range(round(n_images*part_val) + 1):
        renderManager.render_random_image(k_lights_max=10, sub_folder='val')

    renderManager.cameras = test_cams
    for i in range(round(n_images*part_test) + 1):
        renderManager.render_random_image(k_lights_max=10, sub_folder='test')




