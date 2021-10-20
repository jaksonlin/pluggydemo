from pluggy import HookspecMarker, PluginManager
from .config import hookspec

@hookspec(historic=True)
def configure_plugin(pluginmanager:PluginManager)->None:
    """ custom specs into the system

    Args:
        plugin_manager (BasedPluginManager): [description]
    """
    

@hookspec(historic=True)
def configure_config(config) -> None:
    """configure the config content, internal use only

    Args:
        config (Config): [description]
    """


@hookspec
def api_post_pre_hook(addr: str, payload: dict, header: dict) -> dict:
    """ pre post hook

        Args:
            addr (str):  operation url
            payload (dict): operation payload
            header (dict, optional): operation header

        Returns:
            dict: {"addr":str, "payload":dict, "header":dict}
    """


@hookspec
def api_patch_pre_hook(addr: str, payload: dict, header: dict) -> dict:
    """ pre patch hook 

        Args:
            addr (str):  operation url
            payload (dict): operation payload
            header (dict, optional): operation header

        Returns:
            dict: {"addr":str, "payload":dict, "header":dict}
    """


