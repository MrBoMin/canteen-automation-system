// to get current year
function getYear() {
  var currentDate = new Date();
  var currentYear = currentDate.getFullYear();
  document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// isotope js
$(document).ready(function () {
  // Isotope filter
  var $grid = $(".grid").isotope({
    itemSelector: ".all",
    layoutMode: "fitRows",
  });

  $(".filters_menu li").click(function () {
    $(".filters_menu li").removeClass("active");
    $(this).addClass("active");

    var filterValue = $(this).attr("data-filter");
    $grid.isotope({ filter: filterValue });
  });
});

// nice select
$(document).ready(function () {
  $("select").niceSelect();
});

/** google_map js **/
function myMap() {
  var mapProp = {
    center: new google.maps.LatLng(40.712775, -74.005973),
    zoom: 18,
  };
  var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// client section owl carousel
// client section owl carousel
$(".client_owl-carousel").owlCarousel({
  loop: true,
  margin: 0,
  dots: true, // Enable dots for navigation
  nav: true,
  navText: [],
  autoplay: true,
  autoplayHoverPause: true,
  navText: [
    '<i class="fa fa-angle-left" aria-hidden="true"></i>',
    '<i class="fa fa-angle-right" aria-hidden="true"></i>',
  ],
  responsive: {
    0: {
      items: 1, // Show one item on small screens
    },
    768: {
      items: 1, // Show one item on medium screens
    },
    1000: {
      items: 1, // Show one item on large screens
    },
  },
});
