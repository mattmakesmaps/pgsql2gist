__author__ = 'matt'
__date__ = '11/10/13'

import urllib2

if __name__ == '__main__':

    import urllib2
    import urllib
    import json

    values = {
      "description": "the description for this gist",
      "public": "false",
      "files": {
        "test.geojson": {
          "content": "{\"type\":\"FeatureCollection\",\"features\":[{\"geometry\":{\"type\":\"MultiPolygon\",\"coordinates\":[[[[-122.27397895294,47.6952264726636],[-122.274091681305,47.6952639921772],[-122.274165961652,47.6953063675767],[-122.27422133446,47.6953259751011],[-122.274285476306,47.6953322762719],[-122.274359722826,47.6953368214951],[-122.274520579064,47.6953523533749],[-122.274627616748,47.6953677085436],[-122.274761546889,47.6954008462594],[-122.274864799559,47.6954261461133],[-122.274949827175,47.6954533042007],[-122.275042713998,47.6955075255289],[-122.275086522834,47.6955494718794],[-122.275056475713,47.6955643758536],[-122.27496776312,47.6955142147687],[-122.274883217898,47.6954678566781],[-122.274807651989,47.6954523606294],[-122.274697499836,47.6954345597865],[-122.274625690083,47.695408048267],[-122.274519392788,47.695382787048],[-122.274411415686,47.6953701854423],[-122.274340138384,47.6953628605742],[-122.274277101713,47.6953598017717],[-122.274210029086,47.6953576506778],[-122.274152740417,47.6953421800471],[-122.274072202465,47.6952938428247],[-122.27397895294,47.6952264726636]]]]},\"type\":\"Feature\",\"properties\":{\"gid\":1,\"s_hood\":\"OOO\"}}]}"
        }
      }
    }

    url = 'https://api.github.com/gists'
    #data = urllib.urlencode(json.dumps(values))
    req = urllib2.Request(url, json.dumps(values))
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

