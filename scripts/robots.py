import os
import genesis as gs

from genesis_go2 import GENESIS_GO2_MODEL_DIR

gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True,
        world_frame_size = 1.0,
        show_link_frame  = False,
        show_cameras     = False,
        plane_reflection = True,
        ambient_light    = (0.1, 0.1, 0.1),
    ),
    renderer=gs.renderers.Rasterizer(),
    # sim_options=gs.options.SimOptions(
    #     dt=0.01,
    #     gravity=(0, 0, 0.1)
    # ),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.MJCF(
        file=f"{GENESIS_GO2_MODEL_DIR}/franka_emika_panda/panda.xml",
    ),
    # pos=base_init_pos.cpu().numpy(),
    # quat=base_init_quat.cpu().numpy(),
)
go2 = scene.add_entity(
    gs.morphs.URDF(
        file=f"{GENESIS_GO2_MODEL_DIR}/go2/urdf/go2.urdf",
        pos=[1.0, 1.0, 0.42],
        quat=[1.0, 0.0, 0.0, 0.0],
    )
)
kimanoid = scene.add_entity(
    # gs.morphs.MJCF(
    #     file=f"{GENESIS_GO2_MODEL_DIR}/kimanoid/urdf/kist_humanoid3.xml",
    #     pos=[0.0, -1.0, 0.85],
    #     quat=[1.0, 0.0, 0.0, 0.0],
    # ),
    gs.morphs.URDF(
        file=f"{GENESIS_GO2_MODEL_DIR}/kimanoid/urdf/kist_humanoid3.urdf",
        pos=[0.0, -1.0, 0.85],
        quat=[1.0, 0.0, 0.0, 0.0],
    ),
)

cam = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 2.5),
    lookat = (0, 0, 0.5),
    fov    = 30,
    GUI    = False,
)

scene.build()

# render rgb, depth, segmentation, and normal
# rgb, depth, segmentation, normal = cam.render(rgb=True, depth=True, segmentation=True, normal=True)

cam.start_recording()
import numpy as np

for i in range(1000):
    scene.step()
    cam.set_pose(
        pos    = (3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
        lookat = (0, 0, 0.5),
    )
    cam.render()
cam.stop_recording(save_to_filename=os.path.join('video', 'video.mp4'), fps=60)