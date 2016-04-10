/*
====================
generates charts
====================
*/


/*################### Bullet Chart #####################*/
d3.json("/getchartdata", function(error, json) {
    if (error) return console.warn(error);

    var data;
    data = [{'name' : 'Hist. Avg',         'class' : "avg_b",     'height' : 40, 'top' : 15, 'count' : json['histAvg']},
            {'name' : json['websiteName'], 'class' : "current_b", 'height' : 16, 'top' : 27, 'count' : json['totalCount']}];

    if (window.innerWidth < 1200) {
        var width = 400;
    } else {
        var width = 600;
    };

    var height = 70;

    var x = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.count })])
        .range([0, width - 40 ]);

    var chart = d3.select(".bulletchart")
        .attr("width", width)
        .attr("height", height);

    var bar = chart.selectAll("g")
        .data(data)
       .enter().append("g")
        .attr("transform", function(d) { return "translate(0," + d.top + ")"});

    bar.append("rect")
        .attr("class", function(d) { return d.class })
        .attr("height", function(d) { return d.height })
        .attr("width", 0)
       .transition()
        .delay(function(d, i) { return i * 100 })
		.duration(1000)
		.ease("elastic")
        .attr("width", function(d) { return x(d.count) });

    bar.append("text")
        .attr("x", 2)
        .attr("y", 12)
        .text(function(d) { return d.name });

    bar.append("text")
        .attr("x", function(d) { return x(d.count) - (d.count.toString().length * 7) })
        .attr("y", 12)
        .text(function(d) { return d.count });

    // Adjust Avg label + count
    bar.select("rect.avg_b + text")
        .attr("y", -5);
    bar.select("rect.avg_b + text + text")
        .attr("y", -4);

    // Adjust Current label
    bar.select("rect.current_b + text")
        .attr("x", 5);

});



/*################### Bar Chart #####################*/
d3.json("/getchartdata", function(error, json) {
    if (error) return console.warn(error);

    var data;
    data = json['list'];

    var width = 300,
        barHeight = 280 / data.length;

    var x = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.count })])
        .range([0, width - 30]);

    var chart = d3.select(".barchart")
        .attr("width", width)
        .attr("height", barHeight * data.length);

    var bar = chart.selectAll("g")
        .data(data)
      .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")" });

    bar.append("rect")
        .attr("height", barHeight - 1)
        .attr("width", 0)
       .transition()
        .delay(function(d, i) { return i * 100 })
		.duration(1000)
		.ease("elastic")
        .attr("width", function(d) {return x(d.count) });

    bar.append("text")
        .attr("x", 4)
        .attr("dy", ".9em")
        .attr("class", "count")
        .text(function(d) { return d.count; });

    bar.append("text")
        .attr("x", 0)
       .transition()
        .delay(function(d, i) { return i * 100 })
		.duration(1000)
		.ease("elastic")
        .attr("x", function(d) { return x(d.count) + 5; })
        .attr("y". barHeight / 2)
        .attr("dy", ".9em")
        .text(function(d) { return d.name; });


});

/*################### Checks Donut Chart #####################*/

/* Frequency Donut Chart - ToolTip */
    var tooltip = d3.select('#frequencychart')
      .append('div')
      .attr('class', 'tooltip_v');
    tooltip.append('div')
      .attr('class', 'label_v');
    tooltip.append('div')
      .attr('class', 'count');
    tooltip.append('div')
      .attr('class', 'percent');

/* Frequency Donut Chart - Rendering */
d3.json("/getchartdata", function(error, json) {
    if (error) return console.warn(error);

    var w = 250;
    var h = 250;
    var r = h/2;
    var donutWidth = 40;
    var legendRectSize = 12;
    var legendSpacing = 4;
    var color = d3.scale.category20c();

    var data;
    data = json['list'];

    var vis = d3.select('#frequencychart').append("svg:svg").data([data]).attr("width", w).attr("height", h).append("svg:g").attr("transform", "translate(" + r + "," + r + ")");
    var pie = d3.layout.pie().value(function(d){return d.count;});

    // declare an arc generator function
    var arc = d3.svg.arc()
        .innerRadius(r - donutWidth)
        .outerRadius(r);

    // select paths, use arc generator to draw
    var arcs = vis.selectAll("g.slice").data(pie).enter().append("svg:g").attr("class", "slice");
    arcs.append("svg:path")
        .attr("fill", function(d, i){
            return color(i);
        })
        .on("mouseenter", function(d) {
            var arcOver = d3.svg.arc()
                .innerRadius(r - donutWidth + 5)
                .outerRadius(r);
            d3.select(this)
               .transition()
               .duration(100)
               .ease("elastic")
               .attr("d", arcOver)
               .attr("stroke-width",6);
        })
        .on("mouseleave", function(d) {
            d3.select(this).transition()
               .attr("d", arc)
               .attr("stroke","none");
        })
        .attr("opacity", function (d) {
            return 0;
        })
        .transition()
        .delay(function(d, i) { return i * 50 })
		.duration(500)
		.ease("bounce")
		.attr("opacity", function (d) {
            return 1;
        })
        .attr("d", function (d) {
            return arc(d);
        });


    //Frequency Donut Chart - Mouse-over Pop-up
    var svg = arcs

    arcs.on('mouseover', function(d) {
      var total = d3.sum(data.map(function(d) {
        return d.count;
      }));
      var percent = Math.round(1000 * d.data.count / total) / 10;
      tooltip.select('.label_v').html("<strong>" + d.data.name + "</strong>");
      tooltip.select('.count').html("Volume: " + String(d.data.count));
      tooltip.select('.percent').html("Percent: " + String(percent + '%'));
      tooltip.style('display', 'block');
    });

    arcs.on('mouseout', function() {
      tooltip.style('display', 'none');
    });

    arcs.on('mousemove', function(d) {
      var pos = $(".frequency_chart").position();
      tooltip.style('top', (d3.event.pageY - pos.top - 65) + 'px')
        .style('left', (d3.event.pageX - pos.left - 80) + 'px');
    });

});