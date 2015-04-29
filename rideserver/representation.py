def project_as_dict(project):
    return {
        'suite': _suite_as_dict(project.suite),
        'resource_files': [res.datafile.source for res in project.resource_files]
    }


def _suite_as_dict(suite):
    return {
        'name': suite.name,
        'children': [_suite_as_dict(c) for c in suite.children],
        'path': suite.source
    }


def libraries_as_dict(libraries):
    return {
        'libraries': [{'name': lib.name, 'keywords': lib.keyword_names}
                      for lib in libraries]
    }


def tests_as_dict(tests):
    return {
        'tests': [{'name': t.name, 'suite': t.parent.parent.source}
                  for t in tests]
    }


def keywords_as_dict(keywords):
    return {
        'keywords': [{'name': kw.name, 'arguments': kw.args, 'doc': kw.doc}
                     for kw in keywords]
    }
