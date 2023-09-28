// Hint: This is a good place to declare your global variables
const margin = { top: 80, right: 30, bottom: 50, left: 80 };
const width = 1000 - margin.left - margin.right;
const height = 600 - margin.top - margin.bottom;

var svg, selectedValue, x, y;

var male_country_wise_data = {};
var female_country_wise_data = {};
var male_data = {};
var female_data = {};

// STEP 4
var startYear = 1990;
var endYear = 2023;

// This function is called once the HTML page is fully loaded by the browser
document.addEventListener('DOMContentLoaded', function () {
   // Hint: create or set your svg element inside this function
    getBlankSVG()

   // This will load your two CSV files and store them into two arrays.
   Promise.all([d3.csv('data/females_data.csv'),d3.csv('data/males_data.csv')])
        .then(function (values) {
            console.log('loaded females_data.csv and males_data.csv');
            female_data = values[0];
            male_data = values[1];
            selectedCountry = document.getElementById('countries').value


            // Hint: This is a good spot for doing data wrangling
            // STEP 3   
            male_country_wise_data = getCountryWiseData(selectedCountry, male_data)
            female_country_wise_data = getCountryWiseData(selectedCountry, female_data)

            
            drawLolliPopChart();
        });
});

function getCountryWiseData(country, mapArgs){
    return mapArgs.map(function(d) { return [parseInt(d.Year), d[country]]; })
}

// Clear the SVG and set up a new one
function getBlankSVG() {
    // STEP 1
    d3.select('#myDataVis').selectAll('*').remove();


    svg = d3.select("#myDataVis")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

}

// Use this function to draw the lollipop chart.
// STEP 7
function drawLolliPopChart() {

    console.log('trace:drawLollipopChart()');

    // STEP 4
    addAxes()   
    
    addLabel()

    updateLollipops()
    
    addLegends()

}

// STEP 4
function addAxes(){
    // CREATE X - AXIS
    x = d3.scaleTime()
    .domain([new Date(startYear, 0, 1), new Date(endYear, 0, 1)])
    .range([0, width]);
    
    // ATTACH X AXIS
    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x)
        .ticks(d3.timeYear.every(5))
        .tickFormat(d3.timeFormat('%Y'))
        )
    .selectAll("text")
    .style("text-anchor", "center");

    
    // CREATE MAX VALUE FOR EACH COUNTRY FOR Y - AXIS
    const maxValue = Math.max(...male_country_wise_data.map(function(d) { return d[1]; }));


    // CREATE Y - AXIS

    y = d3.scaleLinear()
    .domain([0, maxValue])
    .range([ height, 0]);
    
    svg.select(".y-axis").remove();
    
    svg.append("g")
    .call(d3.axisLeft(y))
    .attr("class", "y-axis");

}

// ADDS LABELS TO GRAPH
function addLabel(){


    // ADD X - AXIS TEXT
    svg.append("text")
    .attr("class", "x-axis-title")
    .attr("text-anchor", "middle")
    .attr("x", width / 2)
    .attr("y", height + margin.top - 50)
    .style('font-weight', 'bold')
    .text("Year");


    // ADD Y - AXIS LABEL
    svg.append("text")
    .attr("class", "y-axis-title")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("x", 0 - height / 2)
    .attr("y", margin.left-120)
    .style('font-weight', 'bold') 
    .text("Employment Rate");
}

// HANDLES CHANGE IN SELECT DROPDOWN
function handleSelectChange(){
    
    selectedCountry = document.getElementById("countries").value;
    male_country_wise_data = getCountryWiseData(selectedCountry, male_data)
    female_country_wise_data = getCountryWiseData(selectedCountry, female_data)

    drawLolliPopChart();
    // updateLollipops();
}

// ADDS LINES AND CIRCLES FOR DATA
// STEP 5 LOLLIPOP CHART
function updateLollipops() {
    const barGap = 10;

    var years = male_country_wise_data.map(function(d) { return new Date(d[0], 0, 1); });

    // // Update male lollipops
    var lineMale = svg.selectAll(".myline-male")
        .data(male_country_wise_data);

    // Enter
    lineMale.enter()
        .append("line")
        .attr("x1", function(d, i) { return x(years[i]) - barGap / 2; })
        .attr("x2", function(d, i) { return x(years[i]) - barGap / 2; })
        .attr("y1", y(0))
        .attr("y2", y(0))
        .attr("stroke", "#69b3a2")
        .attr("class", "myline-male")
        .merge(lineMale)
        .transition()
        .duration(1000)
        .attr("x1", function(d, i) { return x(years[i]) - barGap / 2; })
        .attr("x2", function(d, i) { return x(years[i]) - barGap / 2; })
        .attr("y1", function(d) { return y(d[1]); })
        .attr("y2", y(0));

    // Exit
    lineMale.exit()
        .transition()
        .duration(1000)
        .attr("y1", y(0))
        .attr("y2", y(0))
        .remove();

    var circleMale = svg.selectAll(".mycircle-male")
        .data(male_country_wise_data);

    // Enter
    circleMale.enter()
        .append("circle")
        .attr("cx", function(d, i) { return x(years[i]) - barGap / 2; })
        .attr("cy", y(0))
        .attr("r", "4")
        .style("fill", "#69b3a2")
        .attr("stroke", "black")
        .attr("class", "mycircle-male")
        .merge(circleMale)
        .transition()
        .duration(1000)
        .attr("cx", function(d, i) { return x(years[i]) - barGap / 2; })
        .attr("cy", function(d) { return y(d[1]); });

    // Exit
    circleMale.exit()
        .transition()
        .duration(1000)
        .attr("cy", y(0))
        .remove();


    // Update female lollipops
    var lineFemale = svg.selectAll(".myline-female")
        .data(female_country_wise_data);

    // Enter
    lineFemale.enter()
        .append("line")
        .attr("x1", function(d, i) { return x(years[i]) + barGap / 2; })
        .attr("x2", function(d, i) { return x(years[i]) + barGap / 2; })
        .attr("y1", y(0))
        .attr("y2", y(0))
        .attr("stroke", "pink")
        .attr("class", "myline-female")
        .merge(lineFemale)
        .transition()
        .duration(1000)
        .attr("x1", function(d, i) { return x(years[i]) + barGap / 2; })
        .attr("x2", function(d, i) { return x(years[i]) + barGap / 2; })
        .attr("y1", function(d) { return y(d[1]); })
        .attr("y2", y(0));

    // Exit
    lineFemale.exit()
        .transition()
        .duration(1000)
        .attr("y1", y(0))
        .attr("y2", y(0))
        .remove();

    var circleFemale = svg.selectAll(".mycircle-female")
        .data(female_country_wise_data);

    // Enter
    circleFemale.enter()
        .append("circle")
        .attr("cx", function(d, i) { return x(years[i]) + barGap / 2; })
        .attr("cy", y(0))
        .attr("r", "4")
        .style("fill", "#e0218a")
        .attr("stroke", "pink")
        .attr("class", "mycircle-female")
        .merge(circleFemale)
        .transition()
        .duration(1000)
        .attr("cx", function(d, i) { return x(years[i]) + barGap / 2; })    
        .attr("cy", function(d) { return y(d[1]); });

        // Exit
        circleFemale.exit()
            .transition()
            .duration(1000)
            .attr("cy", y(0))
            .remove();
}

// ADDS LEGENDS TO GRAPH
// STEP 6
function addLegends(){
        
    var legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", "translate("+ (width-190) + ", -80" + ")");

    legend.append("rect")
    .attr("x", 10)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", "#e0218a"); 

    legend.append("text")
    .attr("x", 40)
    .attr("y", 9)
    .attr("dy", "0.35em")
    .style("text-anchor", "start")
    .text("Female Employment Rate");

    legend.append("rect")
    .attr("x", 10)
    .attr("y", 25)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", "#69b3a2"); 

    legend.append("text")
    .attr("x", 40)
    .attr("y", 34)
    .attr("dy", "0.35em")
    .style("text-anchor", "start")
    .text("Male Employment Rate");

}
