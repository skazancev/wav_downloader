import os

from django.conf import settings


class WAVConfig(object):
    def __init__(self):
        self.config_name = settings.CONFIG_NAME
        self.config = ''

    def render_str(self, number, filename):
        return 'exten=> {0} ,1,Noop(Plya background )\n' \
               'exten=> {0} ,n,Background(custom/{1})\n' \
               'exten=> {0} ,n,GoTo(from-trunk)\n'\
            .format(number, filename)

    def build(self, objects):
        configs = []

        for obj in objects:
            if os.path.exists(obj.file.path):
                configs.append(self.render_str(obj.number, obj.filename))

        self.config = '[from-trunk-custom-ivr]\n'
        self.config += '\n'.join(configs)
        self.save()

    def save(self):
        if not os.path.exists(settings.CONFIG_PATH):
            os.makedirs(settings.CONFIG_PATH)

        with open('%s/%s' % (settings.CONFIG_PATH, self.config_name), 'w') as f:
            f.write(self.config)
            f.close()

build_config = WAVConfig().build
