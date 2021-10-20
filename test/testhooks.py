import pluggy
hookspec = pluggy.HookspecMarker("pconfigs")

@hookspec(historic=True)
def my_historic_hook(data:str):
    """ this is a demo spec for historic spec

    Args:
        data (str): [description]
    """
    
