import argparse
from configparser import ConfigParser


def scrap_n_fill():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["desktop", "cli"], default="desktop")
    parser.add_argument("--input", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--template", type=str)

    args = parser.parse_args()

    config: ConfigParser = ConfigParser()
    config.read("config.ini")

    if args.mode == "desktop":
        from desktop.main import run
    elif args.mode == "cli":
        from cli.main import run
    else:
        raise Exception("Invalid mode")

    run(config, args)


if __name__ == "__main__":
    scrap_n_fill()
