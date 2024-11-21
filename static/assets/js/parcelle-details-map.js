let map;
let pointsToBeDrawed;
let points_parcelles_map;

window.onload = function () {
  let data = document.getElementById("data-id").value;
  let d = JSON.parse(data);
 
  let points = JSON.parse(d.points);
  pointsToBeDrawed = JSON.parse(points.points);
  // Map initialization
  var mapcenter = [
    pointsToBeDrawed[0].fields.latt,
    pointsToBeDrawed[0].fields.long,
  ];
  map = L.map("map", { zoomControl: false}).setView(mapcenter, 12);
  let type = points.type;
  if (type === "polyline") {
    var latlngs = [];
    for (let i = 0; i < pointsToBeDrawed.length; i++) {
      latlngs.push([
        pointsToBeDrawed[i].fields.latt,
        pointsToBeDrawed[i].fields.long,
      ]);
    }
    var polyline = L.polyline(latlngs, { color: "red" });
    polyline.addTo(map);
  }
  /// POLYGON DRAW METHOD ///
  if (type === "polygon") {
    var latlngs = [];
    for (let i = 0; i < pointsToBeDrawed.length; i++) {
      latlngs.push([
        pointsToBeDrawed[i].fields.latt,
        pointsToBeDrawed[i].fields.long,
      ]);
    }
    var polygon = L.polygon(latlngs, { fillOpacity: 0});
    polygon.addTo(map);
  }
  /// POLYGON DRAW METHOD ///
  if (type === "rectangle") {
    var latlngs = [];
    for (let i = 0; i < pointsToBeDrawed.length; i++) {
      //console.log(pointsToBeDrawed[i].fields);
      latlngs.push([
        pointsToBeDrawed[i].fields.latt,
        pointsToBeDrawed[i].fields.long,
      ]);
    }
    var rectangle = L.polygon(latlngs, { color: "red" });
    rectangle.addTo(map);
  }
  /// CIRCLE DRAW METHOD ///
  if (type === "circle") {
    let radius = d.radius;
    var circleCenter = [
      pointsToBeDrawed[0].fields.latt,
      pointsToBeDrawed[0].fields.long,
    ];
    var circle = L.circle(circleCenter, radius, { color: "red" });
    circle.addTo(map);
  }
  /// POINT METHOD ///
  if (type === "marker") {
    var marker = L.marker([
      pointsToBeDrawed[0].fields.latt,
      pointsToBeDrawed[0].fields.long,
    ]);
    marker.addTo(map);
  }
  showFormData();
  //google satellite
  googleSat = L.tileLayer("http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", {
    maxZoom: 30,
    subdomains: ["mt0", "mt1", "mt2", "mt3"],
  });
  googleSat.addTo(map);
  // Zoom Control
  var zoomControl = L.control.zoom({
    position: "topleft",
  });
  zoomControl.addTo(map);
  // google street
  googleStreets = L.tileLayer(
    "http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    {
      maxZoom: 30,
      subdomains: ["mt0", "mt1", "mt2", "mt3"],
    }
  );
  var baselayer = {
    Satellite: googleSat,
    Street: googleStreets,
    Street: googleStreets,
  };
  L.control.layers(baselayer).addTo(map);
  getRasterImage()
};
function showFormData() {
  let data = document.getElementById("data-id").value;
  let d = JSON.parse(data);
  let parcelleDetails = JSON.parse(d.form);
  let parcelleDetailsToBePrinted = JSON.parse(parcelleDetails.form);
  let client = parcelleDetailsToBePrinted[0].fields.client;
  let department = parcelleDetailsToBePrinted[0].fields.department;
  let geozone = parcelleDetailsToBePrinted[0].fields.geozone;
  let parcelle_category = parcelleDetailsToBePrinted[0].fields.parcelle_category;
  let parcelle_date = parcelleDetailsToBePrinted[0].fields.parcelle_date;
  let parcelle_name = parcelleDetailsToBePrinted[0].fields.parcelle_name;
  var parcelle_name_text = document.createTextNode(parcelle_name);
  var parcelle_name_text_2 = document.createTextNode(parcelle_name);
  var parcelle_name_element = document.getElementById("parcelle-name-id");
  parcelle_name_element.appendChild(parcelle_name_text);
  var parcelle_name_element_2 = document.getElementById("parcelle-name-id-2");
  parcelle_name_element_2.appendChild(parcelle_name_text_2);
  var parcelle_date_text = document.createTextNode(parcelle_date);
  var parcelle_date_text_2 = document.createTextNode(parcelle_date);
  var parcelle_date_element = document.getElementById("parcelle-date-id");
  parcelle_date_element.appendChild(parcelle_date_text);
  var parcelle_date_element_2 = document.getElementById("parcelle-date-id-2");
  parcelle_date_element_2.appendChild(parcelle_date_text_2);
  var client_text = document.createTextNode(client);
  var client_element = document.getElementById("client-id");
  client_element.appendChild(client_text);
}


var container = document.getElementById('reference-card');
container.addEventListener('wheel', function(event) {
   var delta = event.deltaY || event.detail || event.wheelDelta;
   // Move the scroll position based on the wheel delta
   container.scrollTop += delta;
   // Prevent the default scrolling behavior of the page
   event.preventDefault();
});
container.addEventListener('wheel', function(event) {
   var delta = event.deltaY || event.detail || event.wheelDelta;

   // Scroll to the top when the wheel is scrolled up and the container is already at the top
   if (delta < 0 && container.scrollTop === 0) {
      event.preventDefault();
      // Scroll to the top
      container.scrollTop = 0;
      return;
   }
   // Scroll to the bottom when the wheel is scrolled down and the container is already at the bottom
   if (delta > 0 && container.scrollTop + container.clientHeight >= container.scrollHeight) {
      event.preventDefault();
      // Scroll to the bottom
      container.scrollTop = container.scrollHeight;
      return;
   }
});
