// @TODO: YOUR CODE HERE!
var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
var svg = d3
  .select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append an SVG group
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);


//Import data
d3.csv("../data/data.csv")
  .then(function(healthData) {

    // Parse/Case as numbers
    healthData.forEach(function(data) {
      data.obesity = +data.obesity;
      data.income = +data.income;
    });

    //Create Scale Functions
    var xLinearScale = d3.scaleLinear()
      .domain([20, d3.max(healthData, d => d.obesity)])
      .range([0,width]);
    var yLinearScale = d3.scaleLinear()
      .domain([35000, d3.max(healthData, d => d.income)])
      .range([height, 0]);

    //Create axis Functions
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    //Append Axes
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(bottomAxis);
    chartGroup.append("g")
      .call(leftAxis);

    //Create circles
    var circlesGroup = chartGroup.selectAll("circle")
      .data(healthData)
      .enter()
      .append("circle")
      .attr("cx", d => xLinearScale(d.obesity))
      .attr("cy", d => yLinearScale(d.income))
      .attr("r", "15")
      .attr("fill", "blue")
      .attr("opacity", "0.5");

    //Add State labels
    //Add the SVG Text Element to the svgContainer
    

    //Initialize tool toolTip

    var toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([75,80])
      .html(function(d){
        return (`${d.abbr}<br>Percent Obese: ${d.obesity}<br>Average Income: ${d.income}`);
      });
    chartGroup.call(toolTip);

    //Event listeners
    circlesGroup.on("click", function(data) {
      toolTip.show(data, this);
    });
    circlesGroup.on("mouseout", function(data,index) {
      toolTip.hide(data);
    });
    // Create axes labels
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 40)
      .attr("x", 0 - (height / 2))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Average Income ($)");

    chartGroup.append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
      .attr("class", "axisText")
      .text("Percent Obese (%)");


  });
