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


lidipy = Lidi()
# bind instance
lidipy.bind(Parent, Child())

# or bind a callable
lidipy.bind(Parent, Child)
```

### Singleton Binding

If you want to bind a class as a singleton, you can pass the `singleton` parameter as `True` when calling the `bind()` method:

```python
lidipy.bind(Parent, Child(), singleton=True)
```

With singleton binding, the same instance of the class will be returned every time it is resolved.

### Resolving Dependencies

To resolve a class and its dependencies, you can use the `resolve()` method of the Lidi class:

```python
instance = lidipy.resolve(Parent) # instance is Child()
```

If the class was bound as a singleton, the same instance will be returned each time it is resolved.

### Deferred Resolution

Lidi also supports deferred resolution using the resolve_defer() method. This method returns a callable that, when invoked, resolves the class:

```python
deferred_resolve = lidipy.resolve_defer(Parent)
instance = deferred_resolve()
```

Deferred resolution can be useful when you want to defer the instantiation of a class until it is actually needed.

### Handling Missing Bindings

If a binding is missing for a requested type, a `BindingMissing` exception will be raised.
You can handle this exception and provide appropriate error handling in your application.

```python
from lidipy import BindingMissing

try:
    instance = lidipy.resolve(Mother)
except BindingMissing as e:
    print(e)  # Outputs: "Binding missing for type: Mother"
```

### Usage with Dataclasses

Lidi can be used seamlessly with Python's dataclasses. Here's an example of how to use dataclasses with Lidi:

```python
from dataclasses import dataclass
from lidipy import Lidi

lidipy = Lidi()


@dataclass
class Config:
    db_url: str


@dataclass
class Database:
    config: Config = lidipy.resolve(Config)

    def connect(self):
        print(f"Connecting to database at {self.config.db_url}")


# Bind the dependencies
lidipy.bind(Config, Config(db_url="example.com:5432"))
lidipy.bind(Database, Database)

# Resolve the dataclass with dependencies
database = lidipy.resolve(Database)
database.connect()  # Output: Connecting to database at example.com:5432
```

## Contributing

Contributions are welcome! If you find a bug or want to suggest an improvement, please open an issue or submit a pull request on the GitHub repository.

## License

Lidi is licensed under the MIT License.
Feel free to use, modify, and distribute this project as per the terms of the license.
