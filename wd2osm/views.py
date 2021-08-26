from django.shortcuts import render, get_object_or_404, get_list_or_404
from . import models
import requests
import json


def index(request):
    catalogs = get_list_or_404(models.Catalog)
    return render(request, 'wd2osm/index.html', {"catalogs": catalogs})


def catalog(request, catalog_id):
    cat = get_object_or_404(models.Catalog, pk=catalog_id)
    return render(request, 'wd2osm/catalog.html', {"catalog": cat})


def wikidata(request):
    # Trying out with forms
    return render(request, 'wd2osm/wikidata.html')


def wikidata_item(request):
    if request.POST:
        # Extract this from there
        WIKIDATA_IDS = ["Q22944537", "Q96590661", "Q22985219", "Q22964120", "Q22964115"]
        HEADERS = {'User-Agent': "Cartodata/0.0.1 @ https://github.com/Poslovitch/Cartodata"}
        wikidata_id = request.POST["wikidata_id"]
        WIKIDATA_ENTITY_LINK = "https://www.wikidata.org/wiki/Special:EntityData/$1.json"
        WIKIDATA_PROPERTY_COORDS = "P625"

        response = requests.get(WIKIDATA_ENTITY_LINK.replace("$1", wikidata_id), headers=HEADERS)

        data_object = json.loads(response.content)["entities"][wikidata_id]
        claims = data_object["claims"]

        coords = []

        if WIKIDATA_PROPERTY_COORDS in claims:
            coords_claim = claims[WIKIDATA_PROPERTY_COORDS][0]["mainsnak"]["datavalue"]["value"]

            coords.append(coords_claim["latitude"])
            coords.append(coords_claim["longitude"])

        OVERPASS_API_LINK = "https://overpass-api.de/api/interpreter"
        OVERPASS_QUERY = """[out:json][timeout:60];
        (
        way["building"](around:5.0, $lat, $lon);
        relation["building"](around:5.0, $lat, $lon);
        );
        out body;
        >;
        out skel qt;"""

        data = {
            "data": OVERPASS_QUERY.replace("$lat", str(coords[0])).replace("$lon", str(coords[1])),
            "headers": HEADERS
        }

        osm_contents = json.loads(requests.post(OVERPASS_API_LINK, data=data).content)
        osm_elements = osm_contents["elements"]

        osm_links = []
        osm_nodes = []
        for element in osm_elements:
            if element["type"] == "way":
                osm_links.append(element["id"])
            if element["type"] == "node":
                osm_nodes.append([element["lat"], element["lon"]])

        return render(request, 'wd2osm/wikidata_item.html', {'wikidata': wikidata_id, 'coordinates': coords, 'osm': osm_links, 'nodes': osm_nodes})
