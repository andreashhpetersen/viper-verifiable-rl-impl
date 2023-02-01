import argparse

# Gymnasium replaces gym, so we should try and use that
try:
    import sys
    import gymnasium as gym
    sys.modules['gym'] = gym
except ModuleNotFoundError:
    import gym


from train.oracle import train_oracle
from train.viper import train_viper
from test.oracle import test_oracle
from test.viper import test_viper

COMMAND_MAP = {
    'train-oracle': train_oracle,
    'test-oracle': test_oracle,
    'train-viper': train_viper,
    'test-viper': test_viper,
}

if __name__ == "__main__":
    parent_parser = argparse.ArgumentParser(description="viper", add_help=False)

    # Global arguments
    parent_parser.add_argument(
        "--verbose", type=int, default=0,
        help="Verbosity levels 0: not output 1: info 2: debug")
    parent_parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed")
    parent_parser.add_argument(
        "--render", action='store_true',
        help="Whether to render the environment during training or testing")

    # Env
    parent_parser.add_argument(
        "--env-name", type=str, default="",
        help="OpenAI gym environment name")
    parent_parser.add_argument(
        "--ep-horizon", type=int, default=150,
        help="Episode is terminated when max timestep is reached")
    parent_parser.add_argument(
        "--n-env", type=int, default=8,
        help="Numbers of envs to use when vectorizing")

    # Train
    parent_parser.add_argument(
        "--total-timesteps", type=int, default=10000,
        help="Terminate program when max train iteration is reached")

    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(title="actions", required=True, dest='command')

    train_oracle = subparsers.add_parser('train-oracle', parents=[parent_parser], help="Train oracle")
    train_oracle.add_argument(
        "--resume", action='store_true',
        help="Whether to resume training a previously saved model.")

    test_oracle = subparsers.add_parser('test-oracle', parents=[parent_parser], help="Test oracle")

    train_viper = subparsers.add_parser('train-viper', parents=[parent_parser], help="Run the viper algorithm")
    train_viper.add_argument(
        "--steps", type=int, default=80,
        help="Number of iterations of Viper")
    train_viper.add_argument(
        "--n-steps", type=int, default=1000,
        help="Number of datapoints to sample during each iteration of Viper")
    train_viper.add_argument(
        "--max-leaves", type=int, default=None,
        help="Maximum number of leave nodes to use for the extracted decision tree")
    train_viper.add_argument(
        "--max-depth", type=int, default=None,
        help="Maximum depth to use for the extracted decision tree")

    test_viper = subparsers.add_parser('test-viper', parents=[parent_parser], help="Test viper")
    test_viper.add_argument(
        "--max-leaves", type=int, default=None,
        help="Maximum number of leave nodes to use for the extracted decision tree")
    test_viper.add_argument(
        "--max-depth", type=int, default=None,
        help="Maximum depth to use for the extracted decision tree")

    args = main_parser.parse_args()
    func = COMMAND_MAP[args.command]
    func(args)
