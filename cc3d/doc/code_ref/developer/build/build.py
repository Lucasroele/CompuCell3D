from os import mkdir
from os.path import abspath, dirname, isdir, join

api_source_dir = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))
api_build_dir = join(dirname(abspath(__file__)), "api")
man_source_dir = dirname(abspath(__file__))
man_build_dir = dirname(man_source_dir)


def build(builder: str = 'html'):
    """
    Builds documentation using Sphinx

    :param str builder: Sphinx builder
    :return: None
    """
    from sphinx.cmd import build as sphinx_build
    from sphinx.cmd.make_mode import BUILDERS

    if builder not in [x[1] for x in BUILDERS]:
        raise EnvironmentError("Builder not supported")

    build_dir = join(man_build_dir, builder)

    if not isdir(build_dir):
        mkdir(build_dir)

    argv = [man_source_dir, build_dir,
            '-b', builder]

    sphinx_build.main(argv)


def build_api():
    """
    Auto-generates API documentation source code and stores it in ./api

    :return: None
    """
    if not isdir(api_build_dir):
        mkdir(api_build_dir)

    exclude_pattern = ['doc', "experimental", "gui_plugins", "player5", "tests", "twedit5", 'version_fetcher.py',
                       'core/envVarSanitizer.py', 'core/param_scan', 'core/Validation',
                       "cpp/bin", "cpp/CompuCell3DPlugins", "cpp/CompuCell3DSteppables",
                       "cpp/lib", "cpp/PlayerPython*", "cpp/SerializerDE*"]
    source_prefix = "../../../../"
    exclude_pattern = [source_prefix + x for x in exclude_pattern]
    argv = [api_source_dir, *exclude_pattern,
            '-o', api_build_dir,
            '--implicit-namespaces',
            '--separate']

    from sphinx.ext import apidoc
    apidoc.main(argv)


def main():
    build_api()
    build()


if __name__ == '__main__':
    main()
