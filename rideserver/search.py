def search_tests_by_tag(suite, tag):
    suites = [suite]
    matching_tests = []

    if _has_tag(suite, tag):
        matching_tests.extend(all_tests(suite))
    else:
        for test in suite.testcase_table:
            if test.tags.value and tag in test.tags.value:
                matching_tests.append(test)
        for child in suite.children:
            if _has_tag(child, tag):
                matching_tests.extend(all_tests(child))
            else:
                for test in child.testcase_table.tests:
                    if test.tags.value and tag in test.tags.value:
                        matching_tests.append(test)

    return matching_tests


def _has_tag(suite, tag_name):
    tags = (suite.setting_table.default_tags.value or []) + \
          (suite.setting_table.force_tags.value  or [])
    return tag_name in tags


def all_tests(suite):
    #TODO: move to data.py
    own_tests = [t for t in suite.testcase_table.tests]
    for s in suite.children:
        own_tests.extend(all_tests(s))
    return own_tests


def search_keywords_by_pattern(keywords, pattern):
    return [kw for kw in keywords
            if pattern.lower() in kw.name.replace(' ', '').lower()]
