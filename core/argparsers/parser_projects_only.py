import argparse


def parser_projects_only(
    module_name: str,
    description: str,
    is_parent: bool
) -> argparse.ArgumentParser:
    if is_parent:
        add_help = False
    else:
        add_help = True

    parser = argparse.ArgumentParser(
        prog=f"python -m {module_name}",
        description=description,
        add_help=add_help
    )
    parser.add_argument(
        "projects",
        help=" ".join(
            [
                "List of projects.",
                "Each project should be a subdirectory of the html directory."
            ]
        ),
        nargs="+"
    )
    return parser
