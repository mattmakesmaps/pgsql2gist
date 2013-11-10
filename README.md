pgsql2gist
==========

Like pgsql2shp, but for gists.

## Objective

Create a command line utility similar to pgsql2shp, but the output of which should be a link to an anonymous private gist. The gist link should leverage github’s rendering of GeoJSON/TopoJSON, e.g. render a map.

## Criteria

- Should be able to pass in an arbitrary select statement with properties and a single geometry column.
- Should include a flag that allows a user to automatically convert their geometric data to a projection suitable for upload to gist (e.g. 900913/4326?)
- User should not have to explicitly wrap their geometry in an `ST_AsGeoJSON()`q call.

## Resources

Gist API: (http://developer.github.com/v3/gists/)
