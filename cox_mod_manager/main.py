import argparse
import re

from cox_mod_manager.context import context


class NoExitParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if status:
            print(message)


def make_parser() -> NoExitParser:
    # TODO: find a way to clean this up despite argparse's love of mutation
    parser = NoExitParser()
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument(
        "which", choices=["all", "installed"], help="which set of mods to show"
    )
    list_parser.add_argument(
        "-n", "--name", help="show only mods whose name contains this string"
    )
    list_parser.set_defaults(func=listmods)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument(
        "names", nargs="+", help="exact name(s) of the mod(s) to install"
    )
    install_parser.set_defaults(func=install)

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument(
        "names", nargs="+", help="exact name(s) of the mod(s) to uninstall"
    )
    uninstall_parser.set_defaults(func=uninstall)

    exit_parser = subparsers.add_parser("exit", aliases=["quit"])
    exit_parser.add_argument("exit", nargs="?", default=True)  # hacky

    return parser


def listmods(which: str, name: str = "") -> None:
    with context() as ctx:
        if which == "all":
            mods = ctx.mods.keys()
        elif which == "installed":
            mods = ctx.installed
        else:
            return
        if name:
            mods = [mod for mod in mods if name in mod]
        print(mods)


def install(names: str) -> None:
    with context() as ctx:
        for name in names:
            try:
                ctx.mods[name].install()
                ctx.installed.add(name)
            except KeyError:
                print(f'"{name}" is not a valid mod.')


def uninstall(names: str) -> None:
    with context() as ctx:
        for name in names:
            if name in ctx.installed:
                try:
                    ctx.mods[name].uninstall()
                    ctx.installed.remove(name)
                except KeyError:
                    print(f'"{name}" is not a valid mod.')
            else:
                print(f'"{name}" is not installed.')


if __name__ == "__main__":
    parser = make_parser()
    input_re = re.compile(r'"(.*)"|([^" ]+)')  # exactly one group should always match

    while True:
        try:
            print("Enter command:", end=" ")
            args = parser.parse_args(
                m[1] or m[2] for m in re.finditer(input_re, input())
            )
            if hasattr(args, "exit"):
                break
            else:
                # pass other args to func
                args.func(**{k: v for k, v in vars(args).items() if k != "func"})
        except TypeError:
            pass  # don't exit on unknown commands
