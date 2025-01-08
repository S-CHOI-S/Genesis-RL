import argparse
import os
import pickle
import shutil

from datetime import datetime

from genesis_go2.env.kimanoid_env import KimanoidEnv
from rsl_rl.runners import OnPolicyRunner

import genesis as gs


def get_train_cfg(exp_name, max_iterations):

    train_cfg_dict = {
        "algorithm": {
            "clip_param": 0.2,
            "desired_kl": 0.01,
            "entropy_coef": 0.01,
            "gamma": 0.99,
            "lam": 0.95,
            "learning_rate": 0.001,
            "max_grad_norm": 1.0,
            "num_learning_epochs": 5,
            "num_mini_batches": 4,
            "schedule": "adaptive",
            "use_clipped_value_loss": True,
            "value_loss_coef": 1.0,
        },
        "init_member_classes": {},
        "policy": {
            "activation": "elu",
            "actor_hidden_dims": [512, 256, 128],
            "critic_hidden_dims": [512, 256, 128],
            "init_noise_std": 1.0,
        },
        "runner": {
            "algorithm_class_name": "PPO",
            "checkpoint": -1,
            "experiment_name": exp_name,
            "load_run": -1,
            "log_interval": 1,
            "max_iterations": max_iterations,
            "num_steps_per_env": 24,
            "policy_class_name": "ActorCritic",
            "record_interval": -1,
            "resume": False,
            "resume_path": None,
            "run_name": "",
            "runner_class_name": "runner_class_name",
            "save_interval": 100,
        },
        "runner_class_name": "OnPolicyRunner",
        "seed": 1,
    }

    return train_cfg_dict

def get_cfgs():
    env_cfg = {
        "num_actions": 17,
        "default_joint_angles": {
            "LLJ1": 0,
            "LLJ2": 0,
            "LLJ3": 0,
            "LLJ4": 0,
            "LLJ5": 0,
            "LLJ6": 0,
            "LLJ7": 0,

         
            "RLJ1": 0,
            "RLJ2": 0,
            "RLJ3": 0,
            "RLJ4": 0,
            "RLJ5": 0,
            "RLJ6": 0,
            "RLJ7": 0,

         
            "BWJ1": 0,
            "BWJ2": 0,
            "BWJ3": 0,
            
            # "LLJ1": -0.088,
            # "LLJ2": -0.028,
            # "LLJ3":  0.146,
            # "LLJ4":  0.777,
            # "LLJ5":  0.52360,
            # "LLJ6":  0.1,  
            # "LLJ7": -0.01, 

         
            # "RLJ1":  0.088,
            # "RLJ2": -0.028,
            # "RLJ3": -0.146,
            # "RLJ4": -0.777,
            # "RLJ5": -0.52360,
            # "RLJ6": -0.1,  
            # "RLJ7":  0.01, 

         
            # "BWJ1": 0.0,    
            # "BWJ2": 0.0,    
            # "BWJ3": 0.5775,
        },
        "dof_names": [
            "LLJ1", "LLJ2", "LLJ3", "LLJ4", "LLJ5", "LLJ6", "LLJ7",
            "RLJ1", "RLJ2", "RLJ3", "RLJ4", "RLJ5", "RLJ6", "RLJ7",
            "BWJ1", "BWJ2", "BWJ3",
        ],
        # PD
        "kp": 400.0,
        "kd": 40,
        # termination
        "termination_if_roll_greater_than": 40,  # degree
        "termination_if_pitch_greater_than": 40,
        # base pose
        "base_init_pos": [0.0, 0.0, 0.85],
        "base_init_quat": [1.0, 0.0, 0.0, 0.0],
        "episode_length_s": 20.0,
        "resampling_time_s": 4.0,
        "action_scale": 0.25,
        "simulate_action_latency": True,
        "clip_actions": 100.0,
    }
    obs_cfg = {
        "num_obs": 60,
        "obs_scales": {
            "lin_vel": 2.0,
            "ang_vel": 0.25,
            "dof_pos": 1.0,
            "dof_vel": 0.05,
        },
    }
    reward_cfg = {
        "tracking_sigma": 0.25,
        "base_height_target": 0.85,
        "feet_height_target": 0.075,
        "reward_scales": {
            "tracking_lin_vel": 1.0,
            "tracking_ang_vel": 0.2,
            "lin_vel_z": -1.0,
            "base_height": -50.0,
            "action_rate": -0.005,
            "similar_to_default": -0.1,
        },
    }
    command_cfg = {
        "num_commands": 3,
        "lin_vel_x_range": [2.0, 2.0],
        "lin_vel_y_range": [0, 0],
        "ang_vel_range": [0, 0],
    }

    return env_cfg, obs_cfg, reward_cfg, command_cfg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="kimanoid-walking")
    parser.add_argument("-B", "--num_envs", type=int, default=4096)
    parser.add_argument("--max_iterations", type=int, default=500)
    args = parser.parse_args()

    gs.init(logging_level="warning")

    # log_dir = f"logs/{args.exp_name}"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = f"logs/{args.exp_name}/{timestamp}"

    env_cfg, obs_cfg, reward_cfg, command_cfg = get_cfgs()
    train_cfg = get_train_cfg(args.exp_name, args.max_iterations)

    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    env = KimanoidEnv(
        num_envs=args.num_envs, env_cfg=env_cfg, obs_cfg=obs_cfg, reward_cfg=reward_cfg, command_cfg=command_cfg
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device="cuda:0")

    pickle.dump(
        [env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg],
        open(f"{log_dir}/cfgs.pkl", "wb"),
    )

    runner.learn(num_learning_iterations=args.max_iterations, init_at_random_ep_len=True)


if __name__ == "__main__":
    main()

"""
# training
python scripts/kimanoid_train.py
"""