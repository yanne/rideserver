import os
import sys

from flask import Flask, render_template, request
from flask.ext.restful import Resource, Api

from data.data import load_data, get_project
from representation import (project_as_dict, libraries_as_dict, tests_as_dict,
                            keywords_as_dict)
from search import search_tests_by_tag, search_keywords_by_pattern


app = Flask(__name__)
api = Api(app)


class Project(Resource):
    def get(self):
        return project_as_dict(get_project())


class Libraries(Resource):
    def get(self):
        return libraries_as_dict(get_project().libraries.values())


class SearchTests(Resource):
    def get(self, tag):
        suite = get_project().suite
        return tests_as_dict(search_tests_by_tag(suite, tag))


class SearchKeywords(Resource):
    def get(self, pattern):
        return keywords_as_dict(
            search_keywords_by_pattern(get_project().get_all_keywords(), pattern)
        )


api.add_resource(Project, '/project')
api.add_resource(Libraries, '/libraries')
api.add_resource(SearchTests, '/search/tests/<tag>')
api.add_resource(SearchKeywords, '/search/keywords/<pattern>')


if __name__ == "__main__":
    load_data(sys.argv[1])
    app.run(debug=True)
