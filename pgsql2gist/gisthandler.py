__author__ = 'matt'
__date__ = '11/24/13'

import simplejson as json
import urllib2


class GistAPIHandler(object):
    """
    Provides methods for interacting with the Github Gist API.

    Required parameters:
    file (STRING) - File name. Required to be in extension '.geojson' OR '.topojson'
    description (STRING) - A brief description of the gist contents
    content (STRING) - Implied to be Valid GeoJSON or TopoJSON, but not required.
    """
    def __init__(self, filename, description, content, public="false"):
        self.content = content
        self.description = description
        self.file = filename
        self.public = public
        self.response_content = None
        self.response_headers = None
        self.url = 'https://api.github.com/gists'

    def _build_request(self):
        """
        Given instance attributes, generate a properly formatted
        JSON request for the gist API.
        """
        data = {
            "description": self.description,
            "public": self.public,
            "files": {
                self.file: {
                    "content": self.content
                }
            }
        }
        return json.dumps(data)

    def _submit_request(self, json_data):
        """
        Given a JSON object properly formatted for the gist API
        Submit via http POST.
        """
        request = urllib2.Request(self.url, json_data)
        try:
            response = urllib2.urlopen(request)
        # Catch URL/HTTP errors, then abort script.
        except urllib2.HTTPError as e:
            print 'ERROR: Server returned HTTP Error Code:', e.code
            raise e
        except urllib2.URLError as e:
            print 'ERROR: Server Could Not Be Reached.'
            print 'REASON: ', e.reason
            raise e
        else:
            return response

    def create(self):
        """
        Execute a series of internal class methods responsible for processing
        the request/response interaction between the client and the github API.

        This method updates the class instance's response_content attribute, which
        contains the gist url.
        """

        data_as_json = self._build_request()
        response = self._submit_request(data_as_json)
        self.response_headers = response.headers.dict

        # Populate instance attribute with JSON response from github.
        if response.code == 201:
            self.response_content = json.loads(response.read())
            return True
        else:
            print "Gist creation failed. Server returned HTTP code: ", response.code
            raise urllib2.HTTPError