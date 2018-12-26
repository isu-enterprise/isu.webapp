from .views import FileUploadEvent

def includeme(config, **settings):
    # from .pyramid import configurator

    # storage = config.registry.getUtility(IFileStorage)
    # try:
    #     static_dir = config.registry.settings["storage.static"]
    # except KeyError:
    #     raise RuntimeError("storage.static settings needed")

    # static_dir = os.path.join(storage.base_path, static_dir)
    # static_dir = os.path.abspath(static_dir)

    config.load_zcml("isu.webapp.storage.file:configure.zcml")
