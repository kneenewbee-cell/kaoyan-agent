__all__ = ["filter_tools_for_request", "select_tools"]


def __getattr__(name: str):
    if name in __all__:
        from qa import agent_runtime

        return getattr(agent_runtime, name)
    raise AttributeError(name)
