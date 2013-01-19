import spynach
from controllers import RootController

app = spynach.Application(root=RootController, templates_path='views', config={'mongo_url': 'test_spynach'})

if __name__ == '__main__':
    from spynach.server import serve
    serve(app)
