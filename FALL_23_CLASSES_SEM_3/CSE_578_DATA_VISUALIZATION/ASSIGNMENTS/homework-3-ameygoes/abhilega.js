// UTILITY FUNCTION: SELECT ALL - DESLECT ALL
document.getElementById("selectAll").addEventListener("change", function () {
    const checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });
});

// GET ALL BUTTONS / VALUES FROM INDEX HTML
const yearSelect = document.getElementById("yearSelect");
const animateButton = document.getElementById("animateButton");

// GLOABAL VARIABLES:
const startYear = 1960;
const endYear = 2013;
let currentYear = startYear;
let height = 1080;
let width = 1700;
let margin = ({top: 140, right: 10, bottom: 140, left: 10});
let checkedBoxes = ["South Asia", "Sub-Saharan Africa", "Latin America & Caribbean", "Europe & Central Asia", "East Asia & Pacific", "Middle East & North Africa", "North America"];
let animationInterval;
let circleSizeRange = [3, 20];
let fontSize = 26;
let fontSize2 = 20;

// CREATE YEAR DROP DOWN VALUES DYANMICALLY
for (let year = startYear; year <= endYear; year++) {
    const option = document.createElement("option");
    option.value = year;
    option.text = year;
    yearSelect.appendChild(option);
}


// DEFAULT PARAMETERS FOR GRAPH WHEN PAGE IS LOADED FOR THE FIRST TIME
let xAxisParameter = "Cellular Subscriptions"
let yAxisParameter = "Death Rate"
let year = String(yearSelect.value);
let regionParam = "World bank region"
let fileName = "merged_file.csv"
let minYAxisParam = "3.312"
let maxYAxisParam = "48.922"
// REGION WISE COLORING
let colors = d3.scaleOrdinal(d3.schemeSet3)
    .domain(["South Asia", "Sub-Saharan Africa", "Latin America & Caribbean", "Europe & Central Asia", "East Asia & Pacific", "Middle East & North Africa", "North America"]);

// CREATE DYNAMIC LEGENDS
function createLegends(selectedRegions) {
    svg.selectAll(".legend").remove();
    const legendGroup = svg.append("g")
        .attr("class", "legend")
        .attr("transform", "translate(" + (width - 200) +", "+ (margin.top - 90) + ")"); 

    if (selectedRegions != null) {
        const regionColors = selectedRegions.map(region => colors(region));
        
        const verticalSpacingBetweenLegends = 25;
        const legendItems = legendGroup.selectAll(".legend-item")
            .data(selectedRegions)
            .enter()
            .append("g")
            .attr("class", "legend-item")
            .attr("transform", function(d, i) {
                return "translate(0, " + (i * verticalSpacingBetweenLegends) + ")";
            });

        legendItems.append("rect")
            .attr("width", 18)
            .attr("height", 18)
            .attr("fill", function(d, i) {
                return regionColors[i];
            });

        legendItems.append("text")
            .attr("x", 24)
            .attr("y", 15) 
            .text(d => d);

        legendItems.style("font-size", "20px");
    }
}

// APPEND SVG ELEMENT TO DIV
let svg = d3.select("#beeswarm_svg")
            .append("svg")
            .attr("width", width ) 
            .attr("height", height)
            .classed("svg-border", true); 

// APPEND GRAPH ELEMENT TO SVG 
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + (height - margin.bottom - margin.top)  + ")")

// ADD X AXIS LABEL
svg.append("text")
    .attr("class", "x-axis-label")
    .attr("text-anchor", "middle")
    .attr("x", width / 2)
    .attr("y", height - margin.bottom - margin.top + 60)
    .text("X-Axis: " + xAxisParameter)
    .style("font-size", fontSize);

// ADD SIZE AXIS LABEL
svg.append("text")
    .attr("class", "y-axis-label")
    .attr("text-anchor", "middle")
    .attr("x", (width / 2))
    .attr("y", height / 3.5 - margin.bottom - margin.top + 60)
    .text("Circle Size: "+ yAxisParameter)
    .style("font-size", fontSize);

//  DEFINE X SCALE
let xScale = d3.scaleLinear()
               .range([margin.left, width - margin.right]);


// CREATE A TOOLTIP
let tooltip = d3.select("#beeswarm_svg").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);


// LOAD CSV AND PROCESS IT
d3.csv(fileName).then(function (data) {

    // FILTER DATA FOR THE FIRST TIME
    let dataSet = data.filter((row) => row.Year === year);
    let filteredData = dataSet;

    // THIS THING DECIDES THE SIZE OF THE CIRLCES
    let size = d3.scaleLinear()
                .domain(d3.extent(dataSet, function(d) {return +d[yAxisParameter]}))
                .range(circleSizeRange);
    
    
    // SET MIN AND MAX DOMAIN ACCORDINGLY RANGE WILL BE SCALED
    xScale.domain(d3.extent(data, function (d) {
                return +d[xAxisParameter];
            }));

    // DRAW THE CHART FOR THE FIRST TIME.
    plotBeeSwarm();

    // TRIGGER FUNCTIONS FOR CHANGING BUTTON STATES FOR EACH OF THE DROPDOWNS
    d3.selectAll("#region_dropdown").on("change", handleChangeInRegion);
        // HANDLE DATA FROM REGION BUTTION
    function handleChangeInRegion() {
        function selectTickedBox(regionSeletTickBoxClass) {

            let checkboxes = d3.selectAll(regionSeletTickBoxClass).nodes();
            let checkboxesChecked = [];
            for (let i = 1; i < checkboxes.length; i++) {
                if (checkboxes[i].checked) {
                    checkboxesChecked.push(checkboxes[i].defaultValue);
                }
            }
            return checkboxesChecked.length > 0 ? checkboxesChecked : null;
        }
        
        checkedBoxes = selectTickedBox(".region");
        let dataToPlotFromCheckBox = [];
        if (checkedBoxes == null) {
            dataSet = dataToPlotFromCheckBox;
            plotBeeSwarm();
            return;
        }

        for (let i = 0; i < checkedBoxes.length; i++){
            let dataForCheckedBox = filteredData.filter(function(d) {
                return d[regionParam] === checkedBoxes[i];
            });
            Array.prototype.push.apply(dataToPlotFromCheckBox, dataForCheckedBox);
        }
        dataSet = dataToPlotFromCheckBox;
        plotBeeSwarm();

    }

    // HANDLE X-AXIS BUTTON CHANGES AND RE-DRAW PLOT
    d3.selectAll("#xAxis .dropdown-item").on("click", handleChangeInxAxis);
    function handleChangeInxAxis() {
        xAxisParameter = d3.select(this).text();
        xScale.domain(d3.extent(data, function (d) {
            return +d[xAxisParameter];
        }));
        plotBeeSwarm();
        svg.select(".x-axis-label").text(xAxisParameter);
    }

    // BONUS ASSIGNMENT #3 - ADD MIN AND MAX SIZES OF CIRCLE SIZES
    svg.append("text")
        .attr("class", "minMaxCircle")
        .attr("text-anchor", "middle")
        .attr("x", (width / 2))
        .attr("y", height / 3.2 - margin.bottom - margin.top + 60)
        .html("Min Circle Size: <tspan font-weight='bold'>" + minYAxisParam + "</tspan>  Max Circle Size: <tspan font-weight='bold'>" + maxYAxisParam +"</tspan>")
        .style("font-size", fontSize2);

    // HANDLE CIRCLE SIZE BUTTON CHANGES AND RE-DRAW PLOT
    d3.selectAll("#circleSize .dropdown-item").on("click", handleChangeIncircleSize);
    function handleChangeIncircleSize() {
        yAxisParameter = d3.select(this).text();
        minMaxValues = d3.extent(dataSet, function(d) {return +d[yAxisParameter]});
        size = d3.scaleLinear().domain(minMaxValues).range(circleSizeRange);
        plotBeeSwarm();
        svg.select(".y-axis-label").text(("Circle Size: "+ yAxisParameter));
        svg.select(".minMaxCircle")
            .html("Min Circle Size: <tspan font-weight='bold'>" + minMaxValues[0] + "</tspan>  Max Circle Size: <tspan font-weight='bold'>" + minMaxValues[1] +"</tspan>")
            .style("font-size", fontSize2);
        
    }

    // HANDLE CHANGE IN THE YEAR BUTTON
    yearSelect.addEventListener("change", () => {
        year = yearSelect.value;
        dataSet = data.filter((row) => row.Year === year);
        filteredData = dataSet;
        plotBeeSwarm();
    });
    
    // ANIMATE BUTTION TOGGLE BEHAVIOUR
    animateButton.addEventListener("click", function () {
        if (animateButton.textContent === "Play") {
            animateButton.textContent = "Pause";
            startAnimation();
        } else {
            animateButton.textContent = "Play";
            pauseAnimation();
        }
    });

    // START ANIMATION
    function startAnimation() {
        currentYear = yearSelect.value;
        animationInterval = setInterval(function () {
        
            console.log(currentYear);
            if (currentYear > endYear) {
                currentYear = 1980;
            }
            yearSelect.value = currentYear;
            year = currentYear;
            dataSet = data.filter((row) => row.Year === String(year));
            plotBeeSwarm();
            currentYear++;
        }, 1500); 
    }
    
    // PAUSE ANIMATION
    function pauseAnimation() {
        clearInterval(animationInterval);
    }

    // FUNCTION THAT DRAWS PLOT
    function plotBeeSwarm() {
        createLegends(checkedBoxes);
        
        xScale = d3.scaleLinear().range([100, 1600 ])
        xScale.domain(d3.extent(dataSet, function(d) {
            return +d[xAxisParameter];
        }));

        let xAxis;
        xAxis = d3.axisBottom(xScale)
                .ticks(10, ".1f")
                .tickSizeOuter(0);

        d3.transition(svg).select(".x.axis")
            .transition()
            .duration(1000)
            .call(xAxis);

        // CREATES SIMULATION
        let simulation = d3.forceSimulation(dataSet)
            .force("x", d3.forceX(function(d) {
                return xScale(+d[xAxisParameter]); 
            }).strength(2))
            .force("y", d3.forceY(450))
            .force("collide", d3.forceCollide().radius(d => size(d[yAxisParameter])).strength(1))
            .stop();
        
        simulation.tick(300);


        // Create country circles
        let countriesCircles = svg.selectAll(".countries")
            .data(dataSet, function(d) { return d.CountryName });

        countriesCircles.exit()
            .transition()
            .duration(500)
            .attr("cx", 0)
            .attr("cy", 450)
            .remove();

        countriesCircles.enter()
            .append("circle")
            .attr("class", "countries")
            .attr("cx", 0)
            .attr("cy", 450)
            .attr("r", function(d){ return size(d[yAxisParameter])})
            .attr("stroke", "black")
            .attr('stroke-width', '1px') 
            .attr("fill", function(d){return colors(d[regionParam])})
            .merge(countriesCircles)
            .transition()
            .duration(1500)
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
            .attr("r", function(d) { return size(d[yAxisParameter]); });

        // TOOLTIP
        svg.selectAll(".countries").on("mouseover", function(event, d) {  
            tooltip.html(`Country: <img src="/data/flags/${d["alpha2"]}.png" alt="Flag" />
                        <strong>${d["CountryName"]}</strong><br>
                        ${xAxisParameter} : 
                        <strong>${d3.format(",")(d[xAxisParameter])}</strong>
                       `)
            .style('top', event.pageY - 12 + 'px')
            .style('left', event.pageX + 25 + 'px')
            .style("opacity", 0.9);

            d3.select(this) 
            .style('stroke-width', '4px') 
            .style('stroke', 'black');

            })       
            .on("mouseout", function(_) {
                tooltip.style("opacity", 0);
                d3.select(this) 
                .style('stroke-width', '1px') 
                .style('stroke', 'black');
            });
    }
}).catch(function (error) {
    if (error) throw error;
});