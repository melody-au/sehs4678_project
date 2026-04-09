"""Plugin registry for runtime flow handlers.

Each handler file registers one or more functions using `@register(name)`.
At import time, `_autoload_plugins()` imports all modules in this package so
decorators execute and handlers become available via `require(name)`.
"""

import importlib
import pkgutil


__registry__ = {}
def register(name):
    """Decorator that stores a handler function under a public handler name."""
    # using a decorator allows a function to be passed directly without needing to call a registration function separately, e.g.
    # @register("handler_name")
    # in another file;
    # runtimeFlowPlugins.get("handler_name") to retrieve the function later.
    def decorator(func):
        __registry__[name] = func
        return func
    return decorator
# Example usage:
#@register("example_function")
#def example_function():
#    print("This is an example function.")

def require(name):
    """Return a registered handler by name or raise a clear error if missing."""
    if name not in __registry__:
        raise ValueError(f"RuntimeFlowPlugins Error: Function '{name}' is not registered.")
    return __registry__[name]

def list_registered():
    """Return all currently registered handler names."""
    return list(__registry__.keys())


def _autoload_plugins():
    """Import each plugin module so decorator-based registration runs."""
    # Import every module in this package so @register decorators run.
    package_name = __name__
    for module_info in pkgutil.iter_modules(__path__):
        module_name = module_info.name
        if module_name.startswith("_"):
            continue
        importlib.import_module(f"{package_name}.{module_name}")


_autoload_plugins()

