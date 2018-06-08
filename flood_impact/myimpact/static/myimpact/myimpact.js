mapboxgl.accessToken = 'pk.eyJ1IjoiY21vbGxldC1wbGFubmluZyIsImEiOiJjamg2YnNxd3UxamEwMndvMnJ3b2QyZ3luIn0.m57kzLgcEBAbAQz1BfKw8w';

var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/satellite-streets-v9",
    center: [-90.062, 29.9604],
    zoom: 10
});


// names of "layers" we want to use
// The "name" value used as ids for Mapbox sources and layers,
// and correspond to top-level keys in the `geojson` object
// in the response from /myimpact/address
// The "type" value is the Mapbox Style type to use
// "paint" controls how the layer is drawn, see:
// https://www.mapbox.com/mapbox-gl-js/style-spec/#layers
var layerNames = [
    {
        name: "parcel",
        type: "line",
        paint: {
            "line-color": "red",
            "line-width": 2.5
        }
    },
    {
        name: "building",
        type: "fill",
        paint: {
            "fill-color": "#222",
            "fill-opacity": 0.9,
        }
    },
    {
        name: "nonbuilding",
        type: "fill",
        paint: {
            "fill-color": "green",
            "fill-opacity": 0.7
        }
    }
];

// https://docs.djangoproject.com/en/2.0/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-is-false
// FIXME: Sometimes document.cookie is an empty string,
// need to figure out why
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var csrftoken = getCookie('csrftoken');

var form = document.getElementsByTagName('form')[0];
var input = document.getElementById("address-search");
var dataList = document.getElementById('address-list');

form.onsubmit = function(e) {
    e.preventDefault();
    getImpact(input.value);
}

var delayTimer = null;
function delaySearch(text) {

    // clear out the existing datalist
    while (dataList.firstChild) {
        dataList.removeChild(dataList.firstChild)
    }

    clearTimeout(delayTimer);

    delayTimer = setTimeout(function() {

        var post_data = {
            query: form[0].value
        };

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                var response = JSON.parse(xhr.response);
                for (var i = 0; i < response.length; i++) {
                    var option = document.createElement('option');
                    option.value = response[i];
                    dataList.appendChild(option);
                }
            }
        }

        xhr.open("POST", "/myimpact/address_search/", true);
        // FIXME: Occasionally document.cookie is an empty string,
        // need to figure out why. Making this view CSRF-exempt in
        // Django for now.
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.send(JSON.stringify(post_data));

    }, 100);
}


function addMapboxLayers(address_response) {

    layerNames.forEach(function(layer) {
        // remove existing layers and sources first
        if (map.getLayer(layer.name)) {
            map.removeLayer(layer.name);
        }
        if (map.getSource(layer.name)) {
            map.removeSource(layer.name);
        }

        data = address_response.result.geojson[layer.name];
        // don't add empty geometries
        if (Object.keys(data.geometry).length > 0) {
            map.addLayer({
                id: layer.name,
                source: {
                    type: 'geojson',
                    data: data
                },
                type: layer.type,
                paint: layer.paint
            });
        }
    });
}


function getImpact(address) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            var resp = JSON.parse(xhr.response);
            if (resp.success) {
                // populate the table with data
                for (var k in resp.result) {
                    var elem = document.getElementById(k);
                    if (elem) {
                        elem.innerHTML = resp.result[k];
                    }
                }

                addMapboxLayers(resp);

                // move and zoom the map to the parcel
                var options = {
                    center: resp.result.center,
                    zoom: 18
                };
                map.jumpTo(options);

            }
        }
    }

    xhr.open("GET", "/myimpact/address/" + address + "/", true);
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhr.setRequestHeader("Accept", "application/json");
    xhr.send();

}

