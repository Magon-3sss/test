let map;
let pointsToBeDrawed;
let raster_image_url;
let imageUrl;
let points_parcelles_map;

window.onload = function () {
  let data = document.getElementById("data-id").value;
  let d = JSON.parse(data);
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
  let points = JSON.parse(d.points);
   pointsToBeDrawed = JSON.parse(points.points);
  // Map initialization
  var mapcenter = [
    pointsToBeDrawed[0].fields.latt,
    pointsToBeDrawed[0].fields.long,
  ];
  map = L.map("map", { zoomControl: false }).setView(mapcenter, 12);
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
    let points_parcelle = JSON.parse(points_parcelles_map[i]);
    console.log(points_parcelle);
    var latlngs = [];
    for (let i = 0; i < points_parcelle.length; i++) {
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
function showFormData(){
    let data = document.getElementById('data-id').value;
    let d = JSON.parse(data);
    let projectDetails = JSON.parse(d.form);
    let projectDetailsToBePrinted = JSON.parse(projectDetails.form);
    let client = projectDetailsToBePrinted[0].fields.client;
    let department = projectDetailsToBePrinted[0].fields.department;
    let geozone = projectDetailsToBePrinted[0].fields.geozone;
    let project_category = projectDetailsToBePrinted[0].fields.project_category;
    let project_date = projectDetailsToBePrinted[0].fields.project_date;
    let project_name = projectDetailsToBePrinted[0].fields.project_name;
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
    var department_text = document.createTextNode(department);
    var department_element = document.getElementById("department-id");
    department_element.appendChild(department_text);
    var project_category_text = document.createTextNode(project_category);
    var project_category_element = document.getElementById("project-category-id");
    project_category_element.appendChild(project_category_text);
}
    function btn1(){
      document.getElementById("btn1").style.opacity = "0.4";
      document.querySelector('#btn1').disabled = true;
      document.querySelector('#btn2').disabled = false;
      document.getElementById("btn2").style.opacity = "1";
      document.getElementById("irrig").style.display = "inline";
  }
  function btn2(){
      document.getElementById("btn2").style.opacity = "0.4";
      document.querySelector('#btn2').disabled = true;
      document.querySelector('#btn1').disabled = false;
      document.getElementById("btn1").style.opacity = "1";
      document.getElementById("irrig").style.display = "none";
      document.getElementById("reference-card").style.display = "none";
  }
  function pixelToLatLng(x, y, bounds) {
    const [[minLat, minLon], [maxLat, maxLon]] = bounds;
    const lat = minLat + (y / imageHeight) * (maxLat - minLat);
    const lon = minLon + (x / imageWidth) * (maxLon - minLon);
    return [lat, lon];
  }
  
  
  function showAnomaliesOnMap(anomalies) {
    const anomalyIconUrl = "{% static 'assets/images/icons/detection.png' %}"; // Le chemin de l'icône
  
    anomalies.forEach(anomaly => {
      // Utilisez les coordonnées d'anomalie dans le système de coordonnées de l'image raster
      const [lat, lon] = pixelToLatLng(anomaly.x, anomaly.y, imageBounds);
  
      if (!lat || !lon) {
        console.error(`Erreur lors de la conversion des coordonnées pour l'anomalie: ${anomaly}`);
        return;
      }
  
      // Créer un marqueur pour l'anomalie
      const anomalyMarker = L.marker([lat, lon], {
        icon: L.icon({
          iconUrl: anomalyIconUrl,
          iconSize: [25, 25],
          iconAnchor: [12, 25]
        })
      }).addTo(map);
  
      // Optionnel : Ajouter un popup pour chaque anomalie
      anomalyMarker.bindPopup(`Anomalie détectée : ${lat.toFixed(5)}, ${lon.toFixed(5)}`).openPopup();
    });
  }  
  
  

  async function getRasterImage() {
    // Récupérer les IDs des parcelles sélectionnées
    let selectedParcelles = Array.from(
        document.querySelectorAll('input[name="parcelle"]:checked')
    ).map(checkbox => checkbox.value);

    console.log("Parcelles sélectionnées :", selectedParcelles);  // Vérifiez que les IDs sont capturés

    // Vérification si aucune parcelle n'est sélectionnée
    if (!selectedParcelles.length) {
        alert("Veuillez sélectionner au moins une parcelle.");
        return;
    }

    let data = {
        date: document.getElementById("datepicker").value,
        parcelle_ids: selectedParcelles,  // Ajout des parcelle_ids
        filtre: document.getElementById("filtre-select").value,
    };

    try {
        const response = await fetch('/sentinelhub-raster-image/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            showOverLay(responseData.image_url, selectedParcelles);
        } else {
            console.error("Erreur lors de la récupération de l'image raster :", await response.text());
        }
    } catch (error) {
        console.error("Erreur :", error);
    }
}

function showOverLay(imageUrl, parcelleIds) {
  fetch('/get/points/multiple', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ parcelle_ids: parcelleIds }),
  })
  .then(response => response.json())
  .then(points => {
      const bounds = points.map(p => [p.latt, p.long]);
      const imageBounds = L.latLngBounds(bounds);
      
      if (window.imageOverlay) {
          map.removeLayer(window.imageOverlay);
      }
      
      window.imageOverlay = L.imageOverlay(imageUrl, imageBounds, { opacity: 0.8 }).addTo(map);
      map.fitBounds(imageBounds);
  });
}

  
   
  /* function showOverLay(imageUrl, coordinates) {
    console.log('Showing overlay with image URL:', imageUrl);
    const imageUrlWithCacheBuster = imageUrl;
    //const imageUrlWithCacheBuster = imageUrl + '?_t=' + new Date().getTime();
    var bounds = coordinates.map(coord => [coord[1], coord[0]]);
    var imageBounds = L.latLngBounds(bounds);
    console.log('Image bounds for overlay:', imageBounds);
    // Si un overlay existait déjà, retirez-le
    if (window.imageOverlay) {
      map.removeLayer(window.imageOverlay);
    }
    // Créer un nouveau overlay et l'ajouter à la carte
    window.imageOverlay = L.imageOverlay(imageUrlWithCacheBuster, imageBounds, {opacity: 1, interactive: true}).addTo(map);
    // Ajoutez ces lignes pour que la carte s'adapte aux limites de l'image
    map.fitBounds(imageBounds);
  } */ 

  /* function showOverLay(imageUrl, coordinates) {
    const imageUrlWithCacheBuster = imageUrl + '?_t=' + new Date().getTime(); 
    var bounds = coordinates.map(coord => [coord[1], coord[0]]);
    var imageBounds = L.latLngBounds(bounds);

    // Assurez-vous que la bordure bleue est appliquée aux coordonnées du polygone tracé
    var blueBorder = L.polygon(bounds, {color: 'blue', weight: 2, fillOpacity: 0, interactive: false}).addTo(map);
    
    // Si un overlay existait déjà, retirez-le
    if (window.imageOverlay) {
      map.removeLayer(window.imageOverlay);
    }
    // Créer un nouveau overlay avec l'image et la bordure bleue, puis l'ajouter à la carte
    window.imageOverlay = L.imageOverlay(imageUrlWithCacheBuster, imageBounds, {opacity: 1, interactive: true}).addTo(map);
    // Ajoutez ces lignes pour que la carte s'adapte aux limites de l'image et de la bordure bleue
    map.fitBounds(imageBounds);
  } */
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





//...

// Appelez cette fonction lorsque le filtre est sélectionné
document.getElementById('filtre-select').addEventListener('change', updateColorReferenceTable);

document.addEventListener("DOMContentLoaded", function() {
  // Récupérer les données de colorReference depuis le contexte Django
  const data = JSON.parse(document.getElementById('data-id').value);
  const colorReferences = JSON.parse(data.filters_colors).colors;

  // Sélectionnez le tableau de références de couleurs
  const referenceTable = document.getElementById("reference-table");

  // Ajoutez l'en-tête du tableau
  const headerRow = document.createElement("tr");
  headerRow.innerHTML = `
      <th>Value</th>
      <th>Color</th>
      <th>Description</th>
  `;
  referenceTable.appendChild(headerRow);

  // Ajoutez les lignes du tableau
  colorReferences.forEach(ref => {
      const row = document.createElement("tr");
      row.innerHTML = `
          <td>${ref.value}</td>
          <td style="background-color: ${ref.color_css}; width: 30px;"></td>
          <td>${ref.description}</td>
      `;
      referenceTable.appendChild(row);
  });
});
//...