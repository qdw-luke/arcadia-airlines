var margin = { top: 90, right: 50, bottom: 100, left: 100 },
  width = 960 - margin.left - margin.right,
  height = 960 - margin.top - margin.bottom,
  gridSize = Math.floor(width / 80),
  legendElementWidth = gridSize*2,
  buckets = 9,
  colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], 
  datasets = ["./assets/data.csv"];
//create graph canvas
var svg = d3.select("#chart").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//add tooltip for hovering capability
var tooltip = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

var heatmapChart = function(tsvFile) {
d3.csv(tsvFile, //build in csv parsing!  
    function(d) {
      return {
        originState: d.OriginState,
        destState: d.DestState,
        value: +d.AvgFare
      };
    },
function(error, data) {
    //get unique originStates from csvFile
    var origStates = data.map(function(d) { return d.originState; });
    origStates = origStates.filter(function(v,i) { return origStates.indexOf(v) == i; });   
    //get unique destination states from CSV file
    var destStates = data.map(function(d) { return d.destState; });
    destStates = destStates.filter(function(v,i) { return destStates.indexOf(v) == i; });     
    
    //create axisLabels based on origStates & destStates arrays
    svg.selectAll(".yLabel")
        .data(origStates)
        .enter().append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return i * gridSize; })
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
            .attr('class', 'y-axis');
    svg.selectAll(".xLabel")
        .data(destStates)
        .enter().append("text")
            .text(function(d) { return d; })
            .attr("x", function(d, i) { return i * gridSize; })
            .attr("y", 9)
            .style("text-anchor", "start")
            .attr("transform", function(d,i){return "translate(" + gridSize / 2 + ", -15)rotate(-90," + i*gridSize + ",9)"})
            .attr('class', 'x-axis');
    //colorScale is interpolated from color values. d3 does interpolation!
    var colorScale = d3.scale.quantile()
      .domain([0, buckets - 1, d3.max(data, function (d) { return d.value; })])
      .range(colors);
    var cards = svg.selectAll(".hour")
      .data(data, function(d) {return d.originState+':'+d.destState;});

 //MAGIC HERE
 //one rectangle is created for each data point that we bound 
    cards.enter().append("rect")
      .attr("x", function(d) {return origStates.indexOf(d.originState) * gridSize; })
      .attr("y", function(d) { return destStates.indexOf(d.destState) * gridSize; })
    //      .attr("rx", 7)
    //      .attr("ry", 7)
      .attr("class", "hour bordered")
      .attr("width", gridSize)
      .attr("height", gridSize)
      .style("fill", colors[0])
     .on("mouseover", function(d) {	
            tooltip.transition()		
                .duration(200)		
                .style("opacity", .9);		
            tooltip.html(d.originState + ' -> ' + d.destState + "<br/> $"  + Math.round(d.value))	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 28) + "px");	
            })					
        .on("mouseout", function(d) {		
            tooltip.transition()		
                .duration(500)		
                .style("opacity", 0);	
    });

  //NOTE: D3 has transition capability! very useful for animating and changing content of data
  cards.transition().duration(1000)
      .style("fill", function(d) { return colorScale(d.value); });
  cards.select("title").text(function(d) { return d.value; });
  cards.exit().remove();

});  
};

heatmapChart(datasets[0]);