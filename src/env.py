from typing import Optional
import json
import numpy as np
import gymnasium as gym
from server import PolicyServer


class PolicyServerEnv(gym.Env):
    def __init__(self, server_hostname: str, server_port: int):
        self.server = PolicyServer(server_hostname, server_port)
        self.observation_space = gym.spaces.Dict(
            {
                'ok_rate': gym.spaces.Box(
                    low=0, high=np.inf, shape=(1,), dtype=np.float32
                ),
                'green_blocked': gym.spaces.Discrete(2),
                'red_blocked': gym.spaces.Discrete(2),
            }
        )

        # 3 actions, corresponding to "Wait", "ToggleGreen" and "ToggleRed"
        self.action_space = gym.spaces.Discrete(3)

        self._action_to_str = {0: 'ToggleGreen', 1: 'ToggleRed', 2: 'Wait'}

    @staticmethod
    def _obs_reward_of_str(raw: str):
        obj = json.loads(raw)
        observation = {
            'ok_rate': np.array([float(obj['ok_rate'])], dtype=np.float32),
            'green_blocked': int(bool(obj['green_blocked'])),
            'red_blocked': int(bool(obj['red_blocked'])),
        }
        reward = int(obj['reward'])
        return observation, reward

    def _get_obs(self):
        obs_reward_str = self.server.get_obs()
        return self._obs_reward_of_str(obs_reward_str)

    def _post_action(self, action):
        action_str = self._action_to_str[action]
        self.server.post_action(action_str)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        observation, _ = self._get_obs()
        info = {}
        return observation, info

    def step(self, action):
        self._post_action(action)
        observation, reward = self._get_obs()
        terminated = False
        truncated = False
        info = {}
        return observation, reward, terminated, truncated, info
