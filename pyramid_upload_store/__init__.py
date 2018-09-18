from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings = {'storage.base_path': 'upload_dir'} #my_dir is directory to store file
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_storage')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('upload', '/upload')
    config.scan()
    return config.make_wsgi_app()


