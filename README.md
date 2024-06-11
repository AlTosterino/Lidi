[![Build status](https://github.com/altosterino/lidi/actions/workflows/push-test.yml/badge.svg)](https://github.com/altosterino/lidi/)
[![Coverage Status](https://coveralls.io/repos/github/AlTosterino/Lidi/badge.svg?branch=main)](https://coveralls.io/github/AlTosterino/Lidi?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

# Lidi (LIghtweight Dependency Injector)

Lidi is a lightweight dependency injector designed to simplify dependency management in your Python projects.
It provides a simple and intuitive API for binding classes and resolving dependencies.

## Installation

You can install Lidi using pip:

```bash
pip install lidipy
```

## Usage

### Basic Binding

To bind a class to an instance or a callable, you can use the `bind()` method of the `Lidi` instance:

```python
from lidipy import Lidi


class Parent:
    pass


class Child:
    pass


lidi = Lidi()
# bind instance
lidi.bind(Parent, Child())

# or bind a callable
lidi.bind(Parent, Child)
```

### Singleton Binding

If you want to bind a class as a singleton, you can pass the `singleton` parameter as `True` when calling the `bind()` method:

```python
lidi.bind(Parent, Child(), singleton=True)
```

With singleton binding, the same instance of the class will be returned every time it is resolved.

### Resolving Dependencies

To resolve a class and its dependencies, you can use the `resolve()` method of the Lidi class:

```python
instance = lidi.resolve(Parent) # instance is Child()
```

If the class was bound as a singleton, the same instance will be returned each time it is resolved.

### Deferred Resolution

Lidi also supports deferred resolution using the `resolve_defer()` method. This method returns a callable that, when invoked, resolves the class:

```python
deferred_resolve = lidi.resolve_defer(Parent)
instance = deferred_resolve()
```

### Class Attribute Resolution

Class attributes are often services or repositories. Lidi supports resolution of bindings using the `resolve_attr` method.

```python
lidi.bind(Parent, Child)

class Repository:
    service: Parent = lidi.resolve_attr(Parent) # instance is Child()
```

### Handling Missing Bindings

If a binding is missing for a requested type, a `BindingMissing` exception will be raised.
You can handle this exception and provide appropriate error handling in your application.

```python
from lidipy import BindingMissing

try:
    instance = lidi.resolve(Mother)
except BindingMissing as e:
    print(e)  # Outputs: "Binding missing for type: Mother"
```

### Usage with Dataclasses

Lidi can be used seamlessly with Python's dataclasses. Here's an example of how to use dataclasses with Lidi:

```python
from dataclasses import dataclass
from lidipy import Lidi

lidi = Lidi()


@dataclass(frozen=True)
class Config:
    db_url: str
    
# Bind Config
lidi.bind(Config, Config(db_url="example.com:5432"))

@dataclass
class Database:
    config: Config = lidi.resolve(Config) # or lidi.resolve_defer(Config)

    def connect(self):
        print(f"Connecting to database at {self.config.db_url}")


# Bind Database
lidi.bind(Database, Database)

# Resolve the dataclass with dependencies
database = lidi.resolve(Database)
database.connect()  # Output: Connecting to database at example.com:5432
```

## Dynamic binds on runtime

Lidi supports bindings change on runtime, here's an example:

```python
from dataclasses import dataclass, field
from lidipy import Lidi

lidi = Lidi()


@dataclass
class Config:
    db_url: str


@dataclass
class Database:
    config: Config = field(default_factory=lidi.resolve_defer(Config))

    def connect(self):
        print(f"Connecting to database at {self.config.db_url}")


# Bind the initial dependencies
lidi.bind(Config, Config(db_url="example.com:5432"))
lidi.bind(Database, Database)

# Initial resolve
database = lidi.resolve(Database)
database.connect()  # Output: Connecting to database at example.com:5432

# Dynamically change binding
lidi.bind(Config, Config(db_url="other-example.com:5432"))

# Second resolve
database = lidi.resolve(Database)
database.connect()  # Output: Connecting to database at other-example.com:5432
```
## Contributing

Contributions are welcome! If you find a bug or want to suggest an improvement, please open an issue or submit a pull request on the GitHub repository.

## License

Lidi is licensed under the MIT License.
Feel free to use, modify, and distribute this project as per the terms of the license.
