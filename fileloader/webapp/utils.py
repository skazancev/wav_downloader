import os

from django.conf import settings


class WAVConfig(object):
    def __init__(self):
        self.filename = settings.CONFIG_NAME
        self.config = ''

    def render_str(self, number, file_path):
        return 'exten=> {0} ,1,Noop(Plya background )\n' \
               'exten=> {0} ,n,Background({1})\n' \
               'exten=> {0} ,n,GoTo(from-trunk)\n'\
            .format(number, file_path)

    def build(self, objects):
        configs = []

        for obj in objects:
            if os.path.exists(obj.file.path):
                configs.append(self.render_str(obj.number, obj.file.path))

        self.config = '\n'.join(configs)
        self.save()

    def save(self):
        if not os.path.exists(settings.CONFIG_PATH):
            os.makedirs(settings.CONFIG_PATH)

        with open('%s/%s' % (settings.CONFIG_PATH, self.filename), 'w') as f:
            f.write(self.config)
            f.close()

build_config = WAVConfig().build
