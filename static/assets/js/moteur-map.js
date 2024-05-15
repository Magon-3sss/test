let map;
let pointsToBeDrawed;
let raster_image_url;
let imageUrl;
let points_parcelles_map;
window.onload = function () {
  let data = document.getElementById("data-id").value;
  //console.log(data);
  let d = JSON.parse(data);
  //console.log(d);
  const filters_select = document.getElementById("filtre-select");
  var filters_colors = JSON.parse(d.filters_colors);
  console.log(filters_colors);
  var filters = JSON.parse(filters_colors.filters);
  console.log(filters);
  for (let i = 0; i < filters.length; i++) {
    const option = document.createElement("option");
    option.value = filters[i].fields.abreviation;
    option.text = filters[i].fields.abreviation;
    filters_select.add(option);
  }
  var colors = JSON.parse(filters_colors.colors);
  console.log(colors);

  const references_table = document.getElementById("reference_id");

  for (let i = 0; i < colors.length; i++) {
    const tr = references_table.insertRow(i);
    var button = document.createElement('button');
    button.style.backgroundColor = colors[i].fields.color_css;
    button.style.width = '20px';
    button.style.height = '20px';
    const color_td = tr.insertCell(0);
    const value_td = tr.insertCell(1);
    const desc_td = tr.insertCell(2);
    color_td.appendChild(button);
    value_td.innerHTML = colors[i].fields.value;
    desc_td.innerHTML = colors[i].fields.description;
  }
  //console.log(d.points_parcelles_map);
  
  let points = JSON.parse(d.points);
  //console.log(points);
   pointsToBeDrawed = JSON.parse(points.points);
  //console.log(pointsToBeDrawed);

  // Map initialization
  var mapcenter = [
    pointsToBeDrawed[0].fields.latt,
    pointsToBeDrawed[0].fields.long,
  ];
  map = L.map("map", { zoomControl: false }).setView(mapcenter, 12);

  let type = points.type;
  //console.log(type);
  //console.log(d.type);
  if (type === "polyline") {
    var latlngs = [];
    for (let i = 0; i < pointsToBeDrawed.length; i++) {
      //console.log(pointsToBeDrawed[i].fields);
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
      //console.log(pointsToBeDrawed[i].fields);
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

  points_parcelles_map = d.points_parcelles_map;
  console.log(points_parcelles_map);
  for(let i = 0; i< points_parcelles_map.length;i++){
    //console.log(points_parcelles_map[i]);
    let points_parcelle = JSON.parse(points_parcelles_map[i]);
    //console.log(points_parcelle);
    var latlngs = [];
    for (let i = 0; i < points_parcelle.length; i++) {
      //console.log(pointsToBeDrawed[i].fields);
      latlngs.push([
        points_parcelle[i].fields.latt,
        points_parcelle[i].fields.long,
      ]);
    }
    var polygon = L.polygon(latlngs, {color: "green", fillOpacity: 0});
    polygon.addTo(map);
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

  /* var imageUrl = 'https://gate.eos.com/api/render/S2/35/R/PJ/2023/4/1/0/NDVI/10/29.010269;29.016193;4326/25.416609;25.422462;4326?cropper_ref=78017e969ba0a42ddac4299787af6c05&CALIBRATE=1&COLORMAP=b4ba30aea7a40841c6f73a5bca2eca57&MIN_MAX=-1,1&MASKING=CLOUD&MASK_COLOR=fefefe&api_key=apk.e082b3cf24cb3231d18cd3cf7751f21fccb56092d089447939f66530a0a0d211';
var imageBounds = [[25.422462, 29.010269], [25.416609, 29.016193]];
L.imageOverlay(imageUrl, imageBounds).addTo(map);  */

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
    /*"water color": watercolor,*/

    Street: googleStreets,
  };

  L.control.layers(baselayer).addTo(map);
};

function showFormData(){
    let data = document.getElementById('data-id').value;
    //console.log(data);
    let d = JSON.parse(data);
    //console.log(d);
    let moteurMap = JSON.parse(d.form);
    //console.log(projectDetails);
    let moteurMapToBePrinted = JSON.parse(moteurMap.form);
    //console.log(projectDetailsToBePrinted);
    
    let client = moteurMapToBePrinted[0].fields.client;
    //console.log(client);
    let department = moteurMapToBePrinted[0].fields.department;
    //console.log(department);
    let geozone = moteurMapToBePrinted[0].fields.geozone;
    //console.log(geozone);
    let project_category = moteurMapToBePrinted[0].fields.project_category;
    //console.log(project_category);
    let project_date = moteurMapToBePrinted[0].fields.project_date;
    ///console.log(project_date);
    let project_name = moteurMapToBePrinted[0].fields.project_name;
    //console.log(project_name);
    var project_name_text =document.createTextNode(project_name);
    var project_name_text_2 =document.createTextNode(project_name);
    var project_name_element = document.getElementById("project-name-id");
    project_name_element.appendChild(project_name_text);
    var project_name_element_2 = document.getElementById("project-name-id-2");
    project_name_element_2.appendChild(project_name_text_2);

    var project_date_text =document.createTextNode(project_date);
    var project_date_text_2 =document.createTextNode(project_date);
    var project_date_element = document.getElementById("project-date-id");
    project_date_element.appendChild(project_date_text);
    var project_date_element_2 = document.getElementById("project-date-id-2");
    project_date_element_2.appendChild(project_date_text_2);

    var client_text =document.createTextNode(client);
    var client_element = document.getElementById("client-id");
    client_element.appendChild(client_text);
    }

    function btn1(){
      document.getElementById("btn1").style.opacity = "0.4";
      document.querySelector('#btn1').disabled = true;
      document.querySelector('#btn2').disabled = false;
      document.getElementById("btn2").style.opacity = "1";
      document.getElementById("irrig").style.display = "inline";
      //alert("hello");
  }
  
  function btn2(){
      document.getElementById("btn2").style.opacity = "0.4";
      document.querySelector('#btn2').disabled = true;
      document.querySelector('#btn1').disabled = false;
      document.getElementById("btn1").style.opacity = "1";
      document.getElementById("irrig").style.display = "none";
      document.getElementById("reference-card").style.display = "none";
      //alert("hello");
  }

// Récupérez l'élément select et ajoutez un événement "change" handler
var selectElement = document.getElementById('filtre-select');
selectElement.addEventListener('change', function() {
  
  var selectedValue = selectElement.value;
  var originalURL = 'https://gate.eos.com/api/render/{view_id}/filtre/10/{min_y};{max_y};4326/{min_x};{max_x};4326?cropper_ref={cropper}&CALIBRATE=1&COLORMAP=b4ba30aea7a40841c6f73a5bca2eca57&MIN_MAX=-1,1&MASKING=CLOUD&MASK_COLOR=fefefe&api_key=apk.e082b3cf24cb3231d18cd3cf7751f21fccb56092d089447939f66530a0a0d211';
  var modifiedURL = originalURL.replace('filtre', selectedValue);
  console.log(modifiedURL);
});

function getRasterImage() {
  
  let date = document.getElementById("datepicker").value;
  let filtreValue = document.getElementById("filtre-select").value; 
  for(let i = 0; i< points_parcelles_map.length;i++){
    //console.log(points_parcelles_map[i]);
    let points_parcelle = JSON.parse(points_parcelles_map[i]);
    let data = {
      "date": date,
      "filtre": filtreValue, 
      "points": points_parcelle
  };

  fetch('http://localhost:8000/api/eos-raster-image/', {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
      .then(response => response.json())
      .then(response => {
          console.log(JSON.stringify(response));
          var url = response.raster_image_url;
          var x = response.min_x;
          var y = response.min_y;
          var xx = response.max_x;
          var yy = response.max_y;
          showOverLay(url, x, y, xx, yy);
          document.getElementById("reference-card").style.display = "inline";
      });
  }
}

function showOverLay(url, x, y, xx, yy, filtreValue) {
    imageUrl = url.replace('filtre', filtreValue);
    var imageBounds = [[x, yy], [xx, y]];
    L.imageOverlay(imageUrl, imageBounds).addTo(map);
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