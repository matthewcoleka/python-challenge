function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel
  var url ="/metadata/"+ sample;
  // Use `d3.json` to fetch the metadata for a sample
  d3.json(url).then(function(data) {
    // Use d3 to select the panel with id of `#sample-metadata`
    var selection = d3.select("#sample-metadata");
    var panel;
    // Use `.html("") to clear any existing metadata
    selection.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data).forEach(([key,value]) => {
      panel = selection.append("div").classed("panel-body", true);
      panel.text(`${key}: ${value}`);
    })
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata
    // BONUS: Build the Gauge Chart
    buildGauge(data.WFREQ);
  });
}
function buildCharts(sample) {
  var url = "/samples/"+sample;
  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(url).then(function(data) {
    // @TODO: Build a Bubble Chart using the sample data
    var max_marker_size = 100;
    var bubble_trace = {
      x:data.otu_ids,
      y:data.sample_values,
      text:data.otu_labels,
      mode: 'markers',
      marker: {
        color: data.otu_ids,
        size: data.sample_values,
        sizeref:2.0*Math.max(...data.sample_values) /
        (max_marker_size**2),
        sizemode: 'area'
      }
    };
    var bubble_data = [bubble_trace];
    var bubble_layout = {
      xaxis: {title:"OTU ID"}
    };
    Plotly.newPlot("bubble", bubble_data, bubble_layout);
    // @TODO: Build a Pie Chart
    data.sample_values.sort(function(a,b) {
      return b - a;
    });
    var pie_data = [{
      values: data.sample_values.slice(0,10),
      labels: data.otu_ids.slice(0,10),
      type: 'pie',
      hovertext: data.otu_labels.slice(0,10)
    }];
    // var pie_layout = {
    //
    // }
    Plotly.newPlot('pie', pie_data);
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}



// Initialize the dashboard
init();
