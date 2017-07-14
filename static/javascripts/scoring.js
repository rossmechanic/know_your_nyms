/**
 * Created by rossmechanic on 4/5/17.
 */
$(document).ready(function () {
    function draw(data) {
        var $parent = $('svg').parent();
        var parent_width = $parent.width();
        var parent_height = $parent.siblings().first().height() > 400 ? $parent.siblings().first().height() : 400;

        var svg = d3.select("svg")
                .attr('width', parent_width)
                .attr('height', parent_height),
            margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = +svg.attr("width") - margin.left - margin.right,
            height = +svg.attr("height") - margin.top - margin.bottom;


        var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
            y = d3.scaleLinear().rangeRound([height, 0]);

        var g = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        x.domain(data.map(function (d) {
            return d.word;
        }));
        y.domain([0, d3.max(data, function (d) {
            return d.percentage;
        })]);

        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        g.append("g")
            .attr("class", "axis axis--y")
            .call(d3.axisLeft(y).ticks(10, "%"))
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Frequency");

        g.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return x(d.word);
            })
            .attr("y", function (d) {
                return y(d.percentage);
            })
            .attr("width", x.bandwidth())
            .attr("height", function (d) {
                return height - y(d.percentage);
            });
    }

    var data = window.percentages['data'];
    var timesPlayed = window.timesPlayed;
    console.log(timesPlayed);
    if (data.length > 0 && timesPlayed >= 5) {
        draw(data);
        $(window).resize(function () {
            $('svg').empty();
            draw(data);
        });
    } else {
        $('#score-report-div').removeClass('col-md-5 col-md-offset-1')
            .addClass('col-md-6 col-md-offset-3')
    }
});
