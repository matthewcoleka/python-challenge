// from data.js
var tableData = data;

// YOUR CODE HERE!


//Get reference to table body
var tbody = d3.select("tbody");
//Select the filter date button
var date_btn = d3.select("#filter-btn");



date_btn.on("click", function() {
  //Prevent Refresh
  d3.event.preventDefault();
  //Show Input date
  var input_date = d3.select("#datetime").property("value");
  console.log(input_date);
  //Filtered data
  var filteredData = tableData.filter(tableData => tableData.datetime === input_date);
  //Populate Table Data
  filteredData.forEach((ufo) => {
    var row = tbody.append("tr");
    Object.entries(ufo).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
  });
});
