# ARC Go2 Robot Training for Genesis

[![Genesis](https://img.shields.io/badge/Genesis-25Y01M-skyblue.svg)](https://genesis-embodied-ai.github.io/)
[![Python](https://img.shields.io/badge/python-3.9-blue.svg)](https://docs.python.org/3/whatsnew/3.9.html)
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/22.04/)
[![License](https://img.shields.io/badge/license-Apache--2.0-yellow.svg)](https://opensource.org/license/apache-2-0)

## Overview
>[!note]  
> This repository is for training Go2 using RL in Genesis.  
> _All the code is sourced from __[Genesis](https://github.com/Genesis-Embodied-AI/Genesis.git)__._  
> **Editor**: [_Sol Choi_](https://github.com/S-CHOI-S)

This repository serves as a template for building projects or extensions based on Genesis. It allows you to develop in an isolated environment, outside of the core Genesis repository.
This template was inspired by the [IsaacLab extension template](https://github.com/isaac-sim/IsaacLabExtensionTemplate.git) structure.

**Keywords:** extension, template, genesis


### Installation

- Install Genesis, see the [installation guide](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html).

    - Alternatively, follow the steps below for a simpler installation.
        ```
        conda env create -f environment.yaml
        conda activate genesis
        pip install genesis-world
        ```

- Install rsl_rl to use the PPO reinforcement learning algorithm.

    ```
    git submodule init
    git submodule update
    cd rsl_rl && pip install -e .
    ```

- Using a python interpreter that has Genesis installed, install the library.

    ```
    cd exts/genesis_go2
    python -m pip install -e .
    ```


#### Genesis
- Project page :link: (https://genesis-embodied-ai.github.io/)
- Github code :link: (https://github.com/Genesis-Embodied-AI/Genesis.git)
- Documentation :link: (https://genesis-world.readthedocs.io/en/latest/index.html)