import spynach
from controllers import RootController
from spynach_ming import MingPlug

app = spynach.Application(root=RootController, templates_path='views', config={'autoreload': True,
                                                                               'plugs': [MingPlug('test_spynach')]})

if __name__ == '__main__':
    from spynach.server import serve
    serve(app)
