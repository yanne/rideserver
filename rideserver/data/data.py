import os

from robot.libdocpkg import LibraryDocumentation
from robot.parsing.model import TestDataDirectory, ResourceFile
from robot.running import TestLibrary


DATA = None

def report_error(error):
    #FIXME: some implementation
    pass


def get_project():
    return DATA


def load_data(root_path):
    global DATA
    if DATA is None:
        suite = TestDataDirectory(source=root_path)
        suite.populate()
        resource_files = load_resource_files(suite)
        libraries = load_libraries(suite, resource_files)
        DATA = Project(suite, resource_files, libraries)
    return DATA


def load_resource_files(suite):
    resource_files = _load_resource_files(suite)
    for c in suite.children:
        resource_files.extend(load_resource_files(c))
    return resource_files

def _load_resource_files(suite):
    resource_files = []
    for resource_import in [imp for imp in suite.imports if imp.type is 'Resource']:
        try:
            dirname = os.path.dirname(suite.source)
            resource = ResourceFileWrapper(os.path.join(dirname, resource_import.name))
            resource_files.append(resource)
        except Exception as err:
            report_error(err)
    return resource_files


def load_libraries(suite, resource_files):
    libraries = {}
    _load_libraries_from_suite(suite, libraries)
    for resource in resource_files:
        _load_libraries(resource.datafile, libraries)
    return libraries

def _load_libraries_from_suite(suite, libraries):
    _load_libraries(suite, libraries)
    for c in suite.children:
        _load_libraries(c, libraries)

def _load_libraries(datafile, libraries):
    for imp in [i for i in datafile.setting_table.imports if i.type is 'Library']:
        name = imp.name
        if name not in libraries:
            try:
                libraries[name] = Library(LibraryDocumentation(name))
            except Exception as error:
                report_error(error)
                pass


class Project(object):
    def __init__(self, suite, resource_files, libraries):
        self.suite = suite
        self.resource_files = resource_files
        self.libraries = libraries
        self.root_dir = os.path.dirname(suite.source)

    def get_all_keywords(self):
        resource_keywords = [res.doc.keywords for res in self.resource_files]
        kwlists = [lib.keywords for lib in self.libraries.values()]
        total_kws = resource_keywords + kwlists
        return [kw for kwlist in total_kws for kw in kwlist]


class ResourceFileWrapper(object):

    def __init__(self, path):
        self.datafile = ResourceFile(path).populate()
        self.doc = LibraryDocumentation(path)


class Library(object):
    def __init__(self, libdoc):
        self.name = libdoc.name
        self.keywords = libdoc.keywords
        self.keyword_names = [kw.name for kw in libdoc.keywords]
