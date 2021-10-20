import sys
from typing import List
from pluggy import HookimplMarker
from pluggy import HookspecMarker
from pluggy import PluginManager

project_name = "pconfigs"

hookimpl = HookimplMarker(project_name)
hookspec = HookspecMarker(project_name)

builtin_plugins:List[str] = [] # these are not historic plugins

class BasedPluginManager(PluginManager):

    def __init__(self):
        # init the plugin system
        super().__init__(project_name)
        from .. import hookspecs
        self.add_hookspecs(hookspecs)

    def import_plugin(self, modname: str, consider_entry_points: bool = False) -> None:
        """Import a plugin with ``modname``.

        modified from _pytest
        """
        assert isinstance(modname, str), f"module name must be str, not {modname}"
        
        if self.is_blocked(modname) or self.get_plugin(modname) is not None:
            return

        importspec = f"{project_name}.plugins." + modname if modname in builtin_plugins else modname

        if consider_entry_points:
            loaded = self.load_setuptools_entrypoints(
                project_name, name=modname)
            if loaded:
                return

        try:
            __import__(importspec)
        except ImportError as e:
            raise ImportError(
                'Error importing plugin "{}": {}'.format(
                    modname, str(e.args[0]))
            ).with_traceback(e.__traceback__) from e
        else:
            mod = sys.modules[importspec]
            self.register(mod, modname)

class Config(object):

    def __init__(self, pluginmanager:BasedPluginManager):
        self.pluginmanager = pluginmanager
        self.hook = pluginmanager.hook
        self.register = pluginmanager.register
        self.import_plugin = pluginmanager.import_plugin
        self.builtin_plugin_configure()

    def builtin_plugin_configure(self):
        """ init plugin in tpautosdk
        """
        # 初始化默认
        self.hook.configure_plugin.call_historic(
            kwargs=dict(pluginmanager=self.pluginmanager)
        )
        self.hook.configure_config.call_historic(
            kwargs=dict(config=self)
        )
        
        for item in builtin_plugins:
            self.import_plugin(item)

def get_config()->Config:
    #TODO feed other infos
    pm = BasedPluginManager()
    return Config(pm)
