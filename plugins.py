from decorators import configure_plugin_decorator


@configure_plugin_decorator
def configure_backups(
    path: str = "~/backups", prefix: str = "copy_", extension: str = ".txt"
) -> dict[str, str | None]:
    return {
        "path": path,
        "prefix": prefix,
        "extension": extension,
    }


@configure_plugin_decorator
def configure_login(
    user: str | None = None, password: str | None = None, token: str | None = None
) -> dict[str, str | None]:
    return {
        "user": user,
        "password": password,
        "token": token,
    }
