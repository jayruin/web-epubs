def identity(command_output: str) -> str:
    return command_output


def comma_separated_ints(command_output: str) -> list[int]:
    return [int(item) for item in command_output.split(",")]
