
from plugconfig import hookimpl, get_config

class StatusPrinter(object):
    @hookimpl(hookwrapper=True)
    def api_post_pre_hook(self, addr:str, payload:dict, header:dict)->dict:
        # 使用hookwrapper实现打印各个阶段的plugin调整payload的效果. hookwrapper无返回值,因其本质是一个迭代器
        outcome = yield
        final_result = {}
        for item in outcome.get_result():
            final_result.update(item)
        print(final_result)
        return final_result # this won't return out

class TestPlugin1(object):
    @hookimpl
    def api_post_pre_hook(self, addr:str, payload:dict, header:dict)->dict:
        payload['meta']="author"
        return {"addr":f"{addr}/v2", # this change will be override by next plugin
        "payload":payload, 
        "header":header}

def test_last_update_of_payload():
    config = get_config()
    config.register(StatusPrinter(), "demo")
    config.register(TestPlugin1(), "demo2")
    result = config.hook.api_post_pre_hook(addr="/1/1/2/2/", payload={"1234":"123"}, header={})
    assert result[-1]["addr"].endswith('v2')

class HistoricPlugin1(object):
    @hookimpl
    def my_historic_hook(self, data:str):
        """ this is a demo spec for historic spec

        Args:
            data (str): [description]
        """
        print("this is the first plugin processing data: ", data)

class HistoricPlugin2(object):
    @hookimpl
    def my_historic_hook(self, data:str):
        """ this is a demo spec for historic spec

        Args:
            data (str): [description]
        """
        print("this is the second plugin processing data: ", data)

class HistoricPlugin3(object):
    def __init__(self):
        self.collected_data = []
    @hookimpl
    def my_historic_hook(self, data:str):
        """ this is a demo spec for historic spec

        Args:
            data (str): [description]
        """
        print("this is the third plugin processing data: ", data)
        self.collected_data.append(data)

class AddSpecPlugin():
    
    @hookimpl
    def configure_plugin(self, pluginmanager)->None:
        # add customize hooks
        from . import testhooks
        pluginmanager.add_hookspecs(testhooks)
        # register plugins
        pluginmanager.register(HistoricPlugin1(), "demo1")
        pluginmanager.register(HistoricPlugin2(), "demo2")
    
def test_historic_plugins():
    config = get_config()
    # register customize specs, note the customize specs is a historic spec, 
    # and it has already been called in init of config.
    # on registration of plugins impl add_customize_specs will automatically get called
    config.register(AddSpecPlugin(), "demobase")
    
    # call with historic
    config.hook.my_historic_hook.call_historic(kwargs=dict(data="data1"))
    config.hook.my_historic_hook.call_historic(kwargs=dict(data="data2"))
    # on registration, it get the _call_history and run
    plugin = HistoricPlugin3()
    config.register(plugin, "demo3")
    assert len(plugin.collected_data) == 2 and plugin.collected_data[-1] == "data2"

