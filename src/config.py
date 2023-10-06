import yaml

class Config:
    def __init__(self):
        self.items_shown = 5
        self.plex = None
        self.overseerr = None
        self.tautulli = None
        self.sonarr = None
        self.sonarr_4k = None
        self.radarr = None
        self.radarr_4k = None
        self.ignored_users = None

    @staticmethod
    def global_instance():
        if hasattr(Config, "instance"):
            return Config.instance

    @staticmethod
    def read_conf():
        if hasattr(Config, "instance"):
            return

        with open("config.yaml", "r") as f:
            conf = yaml.safe_load(f)

        Config.instance = Config()
        Config.instance.__dict__.update(conf)

        Config.clean_urls(Config.instance)

    @staticmethod
    def clean_urls(conf):
        conf.plex['url'] = conf.plex['url'].rstrip('/')
        conf.overseerr['url'] = conf.overseerr['url'].rstrip('/')
        conf.tautulli['url'] = conf.tautulli['url'].rstrip('/')

        if conf.radarr:
            conf.radarr['url'] = conf.radarr['url'].rstrip('/')
        if conf.radarr_4k:
            conf.radarr_4k['url'] = conf.radarr_4k['url'].rstrip('/')
        if conf.sonarr:
            conf.sonarr['url'] = conf.sonarr['url'].rstrip('/')
        if conf.sonarr_4k:
            conf.sonarr_4k['url'] = conf.sonarr_4k['url'].rstrip('/')


# Initialize Config
Config.read_conf()
