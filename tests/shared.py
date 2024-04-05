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
