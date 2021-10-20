import json
from typing import Union
from ..config import hookimpl
from ..config import Config
from ..config import BasedPluginManager, project_name

@hookimpl
def configure_config(config: Config) -> None:
    # register and pass in the config for config pass through
    config.register(DemoPlugin(config), "demo-plugin")

class DemoPlugin(object):
    """ Enahance the api operation and """

    def __init__(self, config:Config):
        self._config = config

    @hookimpl(tryfirst=True)
    def api_post_pre_hook(self, addr:str, payload:dict, header:dict)->dict:
        """ pre post hook 

        Args:
            addr (str):  operation url 
            payload (dict): operation payload
            header (dict, optional): operation header

        Returns:
            dict: {"addr":str, "payload":dict, "header":dict}
        """
        result = {"addr":addr, "payload":payload, "header":header}
        print(result)
        return result
        
    @hookimpl(tryfirst=True)
    def api_patch_pre_hook(self, addr:str, payload:dict, header:dict)->dict:
        """ pre post hook 

        Args:
            addr (str):  operation url
            payload (dict): operation payload
            header (dict, optional): operation header

        Returns:
            dict: {"addr":str, "payload":dict, "header":dict}
        """
        result = {"addr":addr, "payload":payload, "header":header}
        return result
