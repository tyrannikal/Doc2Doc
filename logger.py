def args_logger(*args: object, **kwargs: object) -> None:
    for i, arg in enumerate(args, start=1):
        print(f"{i}. {arg}")

    for kwarg in sorted(kwargs.items()):
        print(f"* {kwarg[0]}: {kwarg[1]}")
