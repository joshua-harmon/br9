"""
Radiant

"""
import sys
import shutil
import inspect

try:
    # Prevent this file to be imported from Brython
    import browser

    sys.exit()
except:
    pass

import os
import json
import jinja2
import pathlib
import importlib.util
from xml.etree import ElementTree
from typing import Union, List, Tuple, Optional

from tornado.web import Application, url, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

DEBUG = True
PATH = Union[str, pathlib.Path]
URL = str
DEFAULT_IP = 'localhost'
DEFAULT_PORT = '5000'
DEFAULT_BRYTHON_VERSION = '3.10.7'
DEFAULT_BRYTHON_DEBUG = 0
DEFAULT_PYSCRIPT_VERSION = '2022.06.1'
AUTO_PYSCRIPT = False

PYSCRIPT_FUNCTIONS = os.path.join(os.path.dirname(sys.argv[0]), 'pyscript_fn.py')
if os.path.exists(PYSCRIPT_FUNCTIONS):
    os.remove(PYSCRIPT_FUNCTIONS)

# with open(PYSCRIPT_FUNCTIONS, 'w') as file:
# file.write('import asyncio')


# ----------------------------------------------------------------------
def pyscript(
    output=None, inline=False, plotly_out=None, callback=None, ignore=False, **kwargs
):
    """"""
    global AUTO_PYSCRIPT

    def wrapargs(fn):

        if not inline:
            sourcecode = f'\n\n# {"-" * 70}\n'
            sourcecode += '\n'.join(
                inspect.getsource(fn).replace('\n    ', '\n').split('\n')[1:]
            )

            sourcecode = sourcecode.replace('(self)', '()')
            sourcecode = sourcecode.replace('(self, ', '(')
            sourcecode = sourcecode.replace('(self,', '(')
            sourcecode = sourcecode.replace('self.', '')

            with open(PYSCRIPT_FUNCTIONS, 'a+') as file:
                file.write(sourcecode)

        return fn

    if not ignore:
        AUTO_PYSCRIPT = True
    return wrapargs


# # ----------------------------------------------------------------------
# def brython_serializer(fn):
    # """"""
    # def inset(*args, **kwargs):
        # return json.dumps(fn)
    # return inset

# ----------------------------------------------------------------------
def delay(fn):
    """"""

    def wrap(t):
        return None

    return wrap


# ----------------------------------------------------------------------
def _get_source_code(fn):
    """"""
    with open(PYSCRIPT_FUNCTIONS, 'r') as file:
        content = file.read()
    sourcecode = '\n'.join(
        inspect.getsource(fn).replace('\n        ', '\n').split('\n')[2:]
    )
    return content, sourcecode


# ----------------------------------------------------------------------
def pyscript_globals(fn):
    """"""
    content, sourcecode = _get_source_code(fn)
    with open(PYSCRIPT_FUNCTIONS, 'w') as file:
        file.write(sourcecode + content)


# ----------------------------------------------------------------------
def pyscript_init(fn):
    """"""
    content, sourcecode = _get_source_code(fn)
    with open(PYSCRIPT_FUNCTIONS, 'w') as file:
        file.write(content + sourcecode)


########################################################################
class PyScriptAPI:
    """"""

    # ----------------------------------------------------------------------
    @pyscript(ignore=True)
    def render_plotly_fig__(self, fig, chart):
        import json
        import plotly
        import js

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        js.Plotly.newPlot(chart, js.JSON.parse(graphJSON), {})

    # # ----------------------------------------------------------------------
    # @pyscript()
    # def brython_serializer(self, data):
    # """"""
    # return json.dumps(data)


########################################################################
class RadiantAPI:
    """Rename Randiant with a new class."""

    # ---------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----------------------------------------------------------------------
    def __new__(self):
        """"""
        RadiantServer(self.__name__)


########################################################################
class PythonHandler(RequestHandler):
    def post(self):
        name = self.get_argument('name')
        args = tuple(json.loads(self.get_argument('args')))
        kwargs = json.loads(self.get_argument('kwargs'))

        if v := getattr(self, name, None)(*args, **kwargs):
            if v is None:
                data = json.dumps(
                    {
                        '__RDNT__': 0,
                    }
                )
            else:
                data = json.dumps(
                    {
                        '__RDNT__': v,
                    }
                )
        self.write(data)

    # ----------------------------------------------------------------------
    def test(self):
        """"""
        return True


########################################################################
class ThemeHandler(RequestHandler):

    # ----------------------------------------------------------------------
    def get(self):
        theme = self.get_theme()
        loader = jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')
        )
        env = jinja2.Environment(autoescape=True, loader=loader)
        env.filters['vector'] = self.hex2vector
        stylesheet = env.get_template('theme.css.template')
        self.write(stylesheet.render(**theme))

    # ----------------------------------------------------------------------
    @staticmethod
    def hex2vector(hex_: str):
        return ', '.join([str(int(hex_[i: i + 2], 16)) for i in range(1, 6, 2)])

    # ----------------------------------------------------------------------
    def get_theme(self):
        theme = self.settings['theme']

        if (not theme) or (not os.path.exists(theme)):
            theme = os.path.join(
                os.path.dirname(__file__), 'templates', 'default_theme.xml'
            )

        tree = ElementTree.parse(theme)
        theme_css = {child.attrib['name']: child.text for child in tree.getroot()}
        return theme_css


# ########################################################################
# class ManifestHandler(RequestHandler):

# # ----------------------------------------------------------------------
# def get(self):

# with open('/home/yeison/Development/BCI-Framework/brython-radiant/examples/pwa/manifest.json', 'r') as file:
# content = file.read()

# self.write(content)


########################################################################
class RadiantHandler(RequestHandler):

    # ----------------------------------------------------------------------
    def initialize(self, **kwargs):
        self.initial_arguments = kwargs

    # ----------------------------------------------------------------------
    def get(self):
        variables = self.settings.copy()
        variables.update(self.initial_arguments)

        variables['argv'] = json.dumps(variables['argv'])

        if variables['static_app']:
            html = self.render_string(
                f"{os.path.realpath(variables['template'])}", **variables
            )
            if os.path.exists('static'):
                shutil.rmtree('static')
            shutil.copytree(os.path.join(os.path.dirname(__file__), 'static'), 'static')

            with open('index.html', 'wb') as file:
                file.write(html)

        self.render(f"{os.path.realpath(variables['template'])}", **variables)

    # ----------------------------------------------------------------------
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


# ----------------------------------------------------------------------
def make_app(
    class_: str,
    /,
    brython_version: str,
    pyscript_version: str,
    debug_level: int,
    pages: Tuple[str],
    template: PATH = os.path.join(os.path.dirname(__file__), 'templates', 'index.html'),
    environ: dict = {},
    mock_imports: Tuple[str] = [],
    handlers: Tuple[URL, Union[List[Union[PATH, str]], RequestHandler], dict] = (),
    python: Tuple[PATH, str] = (),
    theme: PATH = None,
    path: PATH = None,
    autoreload: bool = False,
    static_app: bool = False,
    templates_path: PATH = None
    # pyscript=False,
):
    """
    Parameters
    ----------
    class_ :
        The main class name as string.
    template :
        Path for HTML file with the template.
    environ :
        Dictionary with arguments accessible from the template and main class.
    mock_imports :
        List with modules that exist in Python but not in Brython, this prevents
        imports exceptions.
    handlers :
        Custom handlers for server.
    python :
        Real Python scripting handler.
    theme :
        Path for the XML file with theme colors.
    path :
        Custom directory accesible from Brython PATH.
    autoreload :
        Activate the `autoreload` Tornado feature.
    """

    settings = {
        "debug": DEBUG,
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'static_url_prefix': '/static/',
        "xsrf_cookies": False,
        'autoreload': autoreload,
    }

    if templates_path:
        settings['template_path'] = templates_path

    with open(sys.argv[0], 'r') as f:
        l = f.readline()
        requirements = ''
        radiant_mode_brython = None
        radiant_mode_pyscript = None
        if l.strip() == '#!pyscript' or AUTO_PYSCRIPT:
            radiant_mode_pyscript = 'pyscript'
            reqs = os.path.join(sys.path[0], 'requirements.txt')
            if os.path.exists(reqs):
                with open(reqs, 'r') as r:
                    requirements = r.read()
                requirements = [
                    r.strip() for r in requirements.split('\n') if r.strip()
                ]
        else:
            radiant_mode_brython = 'brython'
        # pyscript will always True for Brython
        if AUTO_PYSCRIPT:  # l.strip() == '#!brython':
            radiant_mode_brython = 'brython'

        if os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), 'pyscript_fn.py')):
            pyscript_fn = os.path.join('/root', 'pyscript_fn.py')
        else:
            pyscript_fn = None

    environ.update(
        {
            'class_': class_,
            'python_': python if python else (None, None),
            'module': os.path.split(sys.path[0])[-1],
            'file': os.path.split(sys.argv[0])[-1].replace('.py', ''),
            # 'file': os.path.split(sys.argv[0])[-1].removesuffix('.py'),
            'file_path': os.path.join('/root', os.path.split(sys.argv[0])[-1]),
            'pyscript_fn': pyscript_fn,
            'theme': theme,
            'argv': sys.argv,
            'template': template,
            'mock_imports': mock_imports,
            'path': path,
            'brython_version': brython_version,
            'pyscript_version': pyscript_version,
            'debug_level': debug_level,
            'radiant_mode_brython': radiant_mode_brython,
            'radiant_mode_pyscript': radiant_mode_pyscript,
            'requirements': requirements,
            'static_app': static_app,
        }
    )

    app = []
    if class_:
        app += [url(r'^/$', RadiantHandler, environ)]

    app += [
        url(r'^/theme.css$', ThemeHandler),
        url(r'^/root/(.*)', StaticFileHandler, {'path': sys.path[0]}),
        # url(r'^/manifest.json$', ManifestHandler),
    ]

    if isinstance(pages, str):
        *package, module_name = pages.split('.')
        module = importlib.import_module('.'.join(package))
        pages = getattr(module, module_name)

    for url_, module in pages:
        *file_, class_ = module.split('.')
        environ_tmp = environ.copy()
        file_ = '.'.join(file_)
        environ_tmp['file'] = file_
        environ_tmp['class_'] = class_
        app.append(
            url(url_, RadiantHandler, environ_tmp),
        )

    if python:

        if not os.path.isabs(python[0]):
            python_path = os.path.join(sys.path[0], python[0])
        else:
            python_path = python[0]

        print('*' * 40)
        print(python_path)
        print('*' * 40)

        spec = importlib.util.spec_from_file_location(
            '.'.join(python).replace('.py', ''), python_path
        )
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        app.append(url(r'^/python_handler', getattr(foo, python[1])))

    for handler in handlers:
        if isinstance(handler[1], tuple):
            spec = importlib.util.spec_from_file_location(
                '.'.join(handler[1]).replace('.py', ''),
                os.path.abspath(handler[1][0]),
            )
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            app.append(url(handler[0], getattr(foo, handler[1][1]), handler[2]))
        else:
            app.append(url(*handler))

    if path:
        app.append(
            url(r'^/path/(.*)', StaticFileHandler, {'path': path}),
        )

    settings.update(environ)

    return Application(app, **settings)


# ----------------------------------------------------------------------
def RadiantServer(
    class_: Optional[str] = None,
    host: str = DEFAULT_IP,
    port: str = DEFAULT_PORT,
    pages: Tuple[str] = (),
    # pyscript=False,
    brython_version: str = DEFAULT_BRYTHON_VERSION,
    pyscript_version: str = DEFAULT_PYSCRIPT_VERSION,
    debug_level: int = DEFAULT_BRYTHON_DEBUG,
    template: PATH = os.path.join(os.path.dirname(__file__), 'templates', 'index.html'),
    environ: dict = {},
    mock_imports: Tuple[str] = [],
    handlers: Tuple[URL, Union[List[Union[PATH, str]], RequestHandler], dict] = (),
    python: Tuple[PATH, str] = (),
    theme: Optional[PATH] = None,
    path: Optional[PATH] = None,
    autoreload: Optional[bool] = False,
    callbacks: Optional[tuple] = (),
    static_app: Optional[bool] = False,
    templates_path: PATH = None,
    **kwargs,
):
    """Python implementation for move `class_` into a Bython environment.

    Configure the Tornado server and the Brython environment for run the
    `class_` in both frameworks at the same time.

    Parameters
    ----------
    class_ :
        The main class name as string.
    host :
        The host for server.
    port :
        The port for server.
    template :
        Path for HTML file with the template.
    environ :
        Dictionary with arguments accessible from the template and main class.
    mock_imports :
        List with modules that exist in Python but not in Brython, this prevents
        imports exceptions.
    handlers :
        Custom handlers for server.
    python :
        Real Python scripting handler.
    theme :
        Path for the XML file with theme colors.
    path :
        Custom directory accesible from Brython PATH.
    autoreload :
        Activate the `autoreload` Tornado feature.

    """

    print("Radiant server running on port {}".format(port))
    application = make_app(
        class_,
        python=python,
        template=template,
        handlers=handlers,
        theme=theme,
        environ=environ,
        mock_imports=mock_imports,
        path=path,
        brython_version=brython_version,
        pyscript_version=pyscript_version,
        pages=pages,
        debug_level=debug_level,
        static_app=static_app,
        templates_path=templates_path,
        # pyscript=pyscript,
    )
    http_server = HTTPServer(
        application,
        # ssl_options={
        # 'certfile': 'host.crt',
        # 'keyfile': 'host.key',
        # },
    )
    http_server.listen(port, host)

    for handler in callbacks:
        if isinstance(handler, tuple):
            spec = importlib.util.spec_from_file_location(
                '.'.join(handler).replace('.py', ''),
                os.path.abspath(handler[0]),
            )
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            getattr(foo, handler[1])()
            # app.append(url(handler[0], getattr(foo, handler[1][1]), handler[2]))
        else:
            handler()

    IOLoop.instance().start()
