from env import PolicyServerEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
# from stable_baselines3.common.logger import configure


def make_env():
    return PolicyServerEnv('localhost', 8000)


vec_env = DummyVecEnv([make_env])

model = PPO('MultiInputPolicy', vec_env, verbose=1)
# model.set_logger(configure('./sb3_log', ['stdout', 'csv']))
model.learn(total_timesteps=10)

obs = vec_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
