import numpy as np

import genesis as gs

from genesis_go2 import GENESIS_GO2_MODEL_DIR

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (0, -3.5, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        res           = (960, 640),
        max_FPS       = 60,
    ),
    sim_options = gs.options.SimOptions(
        dt = 0.01,
    ),
    show_viewer = True,
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.MJCF(
        file=f"{GENESIS_GO2_MODEL_DIR}/franka_emika_panda/panda.xml",
    ),
)
go2 = scene.add_entity(
    gs.morphs.URDF(
        file=f"{GENESIS_GO2_MODEL_DIR}/go2/urdf/go2.urdf",
        pos=[1.0, 1.0, 0.42],
        quat=[1.0, 0.0, 0.0, 0.0],
    )
)
kimanoid = scene.add_entity(
    gs.morphs.URDF(
        file=f"{GENESIS_GO2_MODEL_DIR}/kimanoid/urdf/kist_humanoid3.urdf",
        pos=[0.0, -1.0, 0.85],
        quat=[1.0, 0.0, 0.0, 0.0],
    ),
)
########################## build ##########################
scene.build()

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

go2_jnt_names = [
    "FR_hip_joint",
    "FR_thigh_joint",
    "FR_calf_joint",
    "FL_hip_joint",
    "FL_thigh_joint",
    "FL_calf_joint",
    "RR_hip_joint",
    "RR_thigh_joint",
    "RR_calf_joint",
    "RL_hip_joint",
    "RL_thigh_joint",
    "RL_calf_joint",
]
go2_dofs_idx = [go2.get_joint(name).dof_idx_local for name in go2_jnt_names]

kimanoid_jnt_names = [
    "LLJ1",
    "RLJ1",
    "BWJ1",
    "LLJ2",
    "RLJ2",
    "BWJ2",
    "LLJ3",
    "RLJ3",
    "BWJ3",
    "LLJ4",
    "RLJ4",
    "LLJ5",
    "RLJ5",
    "LLJ6",
    "RLJ6",
    "LLJ7",
    "RLJ7",
]
kimanoid_dofs_idx = [kimanoid.get_joint(name).dof_idx_local for name in kimanoid_jnt_names]

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

# go2
# set positional gains
go2.set_dofs_kp(
    kp             = np.array([20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]),
    dofs_idx_local = go2_dofs_idx,
)
# set velocity gains
go2.set_dofs_kv(
    kv             = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
    dofs_idx_local = go2_dofs_idx,
)
# set force range for safety
go2.set_dofs_force_range(
    lower          = np.array([-23.7, -23.7, -35.55, -23.7, -23.7, -35.55, -23.7, -23.7, -35.55, -23.7, -23.7, -35.55]),
    upper          = np.array([ 23.7,  23.7,  35.55,  23.7,  23.7,  35.55,  23.7,  23.7,  35.55,  23.7,  23.7,  35.55]),
    dofs_idx_local = go2_dofs_idx,
)

# kimanoid
# set positional gains
kimanoid.set_dofs_kp(
    # kp             = np.array([150, 150, 20, 150, 150, 20, 150, 150, 20, 150, 150, 20, 20, 20, 20, 20, 20]),
    kp             = np.array([150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150]),
    dofs_idx_local = kimanoid_dofs_idx,
)
# set velocity gains
kimanoid.set_dofs_kv(
    # kv             = np.array([5, 5, 2, 5, 5, 2, 5, 5, 2, 5, 5, 2, 2, 2, 2, 2, 2]),
    kv             = np.array([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]),
    dofs_idx_local = kimanoid_dofs_idx,
)
# set force range for safety
kimanoid.set_dofs_force_range(
    lower          = np.array([-100, -100, -300, -100, -100, -300, -300, -300, -300, -300, -300, -100, -100, -100, -100, -20, -20]),
    upper          = np.array([ 100,  100,  300,  100,  100,  300,  300,  300,  300,  300,  300,  100,  100,  100,  100,  20,  20]),
    dofs_idx_local = kimanoid_dofs_idx,
)

# Hard reset
for i in range(150):
    if i < 50:
        franka.set_dofs_position(np.array([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04]), franka_dofs_idx)
    elif i < 100:
        franka.set_dofs_position(np.array([-1, 0.8, 1, -2, 1, 0.5, -0.5, 0.04, 0.04]), franka_dofs_idx)
    else:
        franka.set_dofs_position(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]), franka_dofs_idx)
        
    go2.set_dofs_position(np.array([0, 0.8, -1.5, 0, 0.8, -1.5, 0, 1.0, -1.5, 0, 1.0, -1.5]), go2_dofs_idx)
    kimanoid.set_dofs_position(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), kimanoid_dofs_idx)

    scene.step()

# PD control
for i in range(1250):
    if i == 0:
        franka.control_dofs_position(
            np.array([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04]),
            franka_dofs_idx,
        )
        kimanoid.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            kimanoid_dofs_idx,
        )
    elif i == 250:
        franka.control_dofs_position(
            np.array([-1, 0.8, 1, -2, 1, 0.5, -0.5, 0.04, 0.04]),
            franka_dofs_idx,
        )
        kimanoid.control_dofs_position(
            np.array([-0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            kimanoid_dofs_idx,
        )
        # kimanoid.control_dofs_position(
        #     np.array([0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        #     kimanoid_dofs_idx,
        # )
    elif i == 500:
        franka.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]),
            franka_dofs_idx,
        )
        # kimanoid.control_dofs_force(
        #     np.array([0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        #     kimanoid_dofs_idx,
        # )
        kimanoid.control_dofs_position(
            np.array([-0.5, 0.5, 0, 0.255, -0.255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            kimanoid_dofs_idx,
        )
    elif i == 750:
        # control first dof with velocity, and the rest with position
        franka.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])[1:],
            franka_dofs_idx[1:],
        )
        franka.control_dofs_velocity(
            np.array([1.0, 0, 0, 0, 0, 0, 0, 0, 0])[:1],
            franka_dofs_idx[:1],
        )
        kimanoid.control_dofs_position(
            np.array([-0.5, 0.5, 0, 0.255, -0.255, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            kimanoid_dofs_idx,
        )
    elif i == 1000:
        franka.control_dofs_force(
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]),
            franka_dofs_idx,
        )
        # kimanoid.control_dofs_position(
        #     np.array([0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        #     kimanoid_dofs_idx,
        # )
        kimanoid.control_dofs_position(
            np.array([-0.5, 0.5, 0, 0.255, -0.255, 0, 1, -1, 0, 1, -1, 0, 0, 0, 0, 0, 0]),
            kimanoid_dofs_idx,
        )
    
    go2.control_dofs_position(
        np.array([0, 0.8, -1.5, 0, 0.8, -1.5, 0, 1.0, -1.5, 0, 1.0, -1.5]),
        go2_dofs_idx,
    )
        
    # This is the control force computed based on the given control command
    # If using force control, it's the same as the given control command
    print('franka control force:', franka.get_dofs_control_force(franka_dofs_idx))
    print('go2 control force:', go2.get_dofs_control_force(go2_dofs_idx))
    print('kimanoid control force:', kimanoid.get_dofs_control_force(kimanoid_dofs_idx))

    # This is the actual force experienced by the dof
    print('franka internal force:', franka.get_dofs_force(franka_dofs_idx))
    print('go2 internal force:', go2.get_dofs_force(go2_dofs_idx))
    print('kimanoid control force:', kimanoid.get_dofs_force(kimanoid_dofs_idx))

    scene.step()