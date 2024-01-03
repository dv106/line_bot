__all__ = ["Version", "InvalidVersion", "VERSION_PATTERN"]

class InvalidVersion(ValueError): ...

class _BaseVersion:
    def __hash__(self) -> int: ...
    def __lt__(self, other: _BaseVersion) -> bool: ...
    def __le__(self, other: _BaseVersion) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: _BaseVersion) -> bool: ...
    def __gt__(self, other: _BaseVersion) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

VERSION_PATTERN: str

class Version(_BaseVersion):
    def __init__(self, version: str) -> None: ...
    @property
    def epoch(self) -> int: ...
    @property
    def release(self) -> tuple[int, ...]: ...
    @property
    def pre(self) -> tuple[str, int] | None: ...
    @property
    def post(self) -> int | None: ...
    @property
    def dev(self) -> int | None: ...
    @property
    def local(self) -> str | None: ...
    @property
    def public(self) -> str: ...
    @property
    def base_version(self) -> str: ...
    @property
    def is_prerelease(self) -> bool: ...
    @property
    def is_postrelease(self) -> bool: ...
    @property
    def is_devrelease(self) -> bool: ...
    @property
    def major(self) -> int: ...
    @property
    def minor(self) -> int: ...
    @property
    def micro(self) -> int: ...
