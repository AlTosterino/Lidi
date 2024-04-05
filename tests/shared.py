from dataclasses import dataclass


class SimpleClassA: ...


class SimpleClassB: ...


class SimpleClassC: ...


class SimpleBaseClass: ...


class SimpleInheritClassA(SimpleBaseClass): ...


class SimpleInheritClassB(SimpleBaseClass): ...


@dataclass
class SimpleDataclassA: ...


@dataclass
class SimpleDataclassB: ...


@dataclass
class SimpleDataclassC: ...


class ThreadService:
    def __init__(self) -> None:
        self.value = 0

    def increment(self) -> int:
        self.value += 1
        return self.value
