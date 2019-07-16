$('#map').on('load', function () {
    mapboxgl.accessToken = 'pk.eyJ1IjoibWFob29seSIsImEiOiJjankxbnY2OXAwZXJvM25wY2pxb2cxaml2In0.pPibyeH8fp9snLodRu9QQg';
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(initMap);
    }

    function initMap(position) {
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [position.coords.longitude, position.coords.latitude],
            zoom: 15,
            hash: true
        });
        mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.1.0/mapbox-gl-rtl-text.js');
        map.addControl(new MapboxLanguage({
            defaultLanguage: 'ar'
        }));

        var marker = new mapboxgl.Marker({
            draggable: true,
            color: '#488f3e'
        }).setLngLat({
            lng: position.coords.longitude,
            lat: position.coords.latitude
        }).addTo(map);

        function onDragEnd() {
            var lngLat = marker.getLngLat();
            $('#latitude').val(lngLat.lat);
            $('#longitude').val(lngLat.lng);
        }

        marker.on('dragend', onDragEnd);
    }
});

function load_map_from_location(long, lat) {
    mapboxgl.accessToken = 'pk.eyJ1IjoibWFob29seSIsImEiOiJjankxbnY2OXAwZXJvM25wY2pxb2cxaml2In0.pPibyeH8fp9snLodRu9QQg';

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [long, lat],
        zoom: 15,
        hash:
            true
    });
    mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.1.0/mapbox-gl-rtl-text.js');
    map.addControl(new MapboxLanguage({
        defaultLanguage: 'ar'
    }));

    var marker = new mapboxgl.Marker({
        draggable: true,
        color: '#488f3e'
    }).setLngLat({lng: long, lat: lat}).addTo(map);
}