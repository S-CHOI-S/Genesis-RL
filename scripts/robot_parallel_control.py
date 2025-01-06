import genesis as gs
import torch
import numpy as np

from genesis_go2 import GENESIS_GO2_MODEL_DIR

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (3.5, -1.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
    ),
    rigid_options = gs.options.RigidOptions(
        dt                = 0.01,
    ),
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)

franka = scene.add_entity(
    gs.morphs.MJCF(file=f"{GENESIS_GO2_MODEL_DIR}/franka_emika_panda/panda.xml"),
)

########################## build ##########################

# create 20 parallel environments
B = 20
scene.build(n_envs=B, env_spacing=(1.0, 1.0))

franka_jnt_names = [
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'joint5',
    'joint6',
    'joint7',
    'finger_joint1',
    'finger_joint2',
]
franka_dofs_idx = [franka.get_joint(name).dof_idx_local for name in franka_jnt_names]

############ Optional: set control gains ############
# franka
# set positional gains
franka.set_dofs_kp(
    kp             = np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
    dofs_idx_local = franka_dofs_idx,
)
# set velocity gains
franka.set_dofs_kv(
    kv             = np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
    dofs_idx_local = franka_dofs_idx,
)
# set force range for safety
franka.set_dofs_force_range(
    lower          = np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    upper          = np.array([ 87,  87,  87,  87,  12,  12,  12,  100,  100]),
    dofs_idx_local = franka_dofs_idx,
)

# control all the robots
franka.control_dofs_position(
    torch.tile(
        torch.tensor([0, 0, 0, -1.0, 0, 0, 0, 0.02, 0.02], device=gs.device), (B, 1)
    ),
)

# PD control
for i in range(1250):
    if i == 0:
        franka.control_dofs_position(
            torch.tile(
                torch.tensor([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04], device=gs.device), (B, 1)
            ),
        )
    elif i == 250:
        franka.control_dofs_position(
            torch.tile(
                torch.tensor([-1, 0.8, 1, -2, 1, 0.5, -0.5, 0.04, 0.04], device=gs.device), (B, 1)
            ),
        )
    elif i == 500:
        franka.control_dofs_position(
            torch.tile(
                torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device), (B, 1)
            ),
        )
    elif i == 750:
        # control first dof with velocity, and the rest with position
        franka.control_dofs_position(
            torch.tile(
                torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device), (B, 1)
            ),
        )
        franka.control_dofs_velocity(
            torch.tile(
                torch.tensor([1.0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device), (B, 1)
            ),
        )
    elif i == 1000:
        franka.control_dofs_force(
            torch.tile(
                torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0], device=gs.device), (B, 1)
            ),
        )
        
    scene.step()

# for i in range(1000):
#     scene.step()