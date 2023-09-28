    var charCounts = {};
    var charList =  {};
    var color = d3.scaleOrdinal(d3.schemeSet3);
    // HANDLES CHANGE IN SELECT DROPDOWN
    function submitText(){
        
        essay = document.getElementById("wordbox").value;
        calculateVowelsConsonantsAndPunctuations(essay);
        d3.select("#bar_svg").selectAll("*").remove();
    }

    // ============ UTILITY FUNCTIONS =================
    function addMissingCharacters(charCountDict, alphabet) {
    
        // Loop through the alphabet and add missing characters with a frequency of 0
        for (var i = 0; i < alphabet.length; i++) {
            var character = alphabet.charAt(i);
            
            if (!(character in charCountDict)) {
                charCountDict[character] = 0;
            }
        }
    
        return charCountDict;
    }
    
    function processCharacterData(data, alphabet) {
        var processedData = [];
    
        // Convert data object to an array of objects
        var dataArray = Object.keys(data).map(function (label) {
            return { label: label, count: data[label] };
        });
    
        // Loop through the alphabet and set counts to 0 for missing characters
        for (var i = 0; i < alphabet.length; i++) {
            var character = alphabet.charAt(i);
            var foundItem = dataArray.find(function (item) {
                return item.label === character;
            });
            processedData.push(foundItem || { label: character, count: 0 });
        }
    
        return processedData;
    }

    function calculateVowelsConsonantsAndPunctuations(inputString){

        // Initialize counters
        let vowelCount = {};
        let consonantCount = {};
        let punctuationCount = {};

        let numberOfVowels = 0
        let numberOfConsonants = 0
        let numberOfPunctuations = 0
    
        // Convert the input string to lowercase to make it case-insensitive
        const lowerCaseString = inputString.toLowerCase();
    
        // Define regular expressions for vowels, consonants, and punctuation
        const vowelRegex = /[aeiouy]/g; // Matches all vowels
        const consonantRegex = /[bcdfghjklmnpqrstvwxz]/g; // Matches all consonants
        const punctuationRegex = /[.,?!:;]/g; // Matches common punctuation characters
    
        // Use the regular expressions to find matches in the string
        const vowels = lowerCaseString.match(vowelRegex);
        const consonants = lowerCaseString.match(consonantRegex);
        const punctuation = inputString.match(punctuationRegex);
    
        // Count the matches found for vowels
        if (vowels) {
            vowels.forEach((vowel) => {
                vowelCount[vowel] = (vowelCount[vowel] || 0) + 1;
                numberOfVowels += 1;
            });
        }
    
        // Count the matches found for consonants
        if (consonants) {
            consonants.forEach((consonant) => {
                consonantCount[consonant] = (consonantCount[consonant] || 0) + 1;
                numberOfConsonants += 1;
            });
        }
    
        // Count the matches found for punctuation
        if (punctuation) {
            punctuation.forEach((punctuationChar) => {
                punctuationCount[punctuationChar] = (punctuationCount[punctuationChar] || 0) + 1;
                numberOfPunctuations += 1;
            });
        }
        
        vowelCount = addMissingCharacters(vowelCount, "aeiouy");
        consonantCount = addMissingCharacters(consonantCount, "bcdfghjklmnpqrstvwxz");
        punctuationCount = addMissingCharacters(punctuationCount, ".,?!:;");

        var vowelList = processCharacterData(vowelCount, "aeiouy");
        var consonantList = processCharacterData(consonantCount, "bcdfghjklmnpqrstvwxz");
        var punctuationList = processCharacterData(punctuationCount, ".,?!:;");
        
        // Create objects to hold the counts
        charList = [
            {label: "vowels", count: vowelList},
            {label: "consonants", count: consonantList},
            {label: "punctuation", count: punctuationList}
        ];
        charCounts= [
            {label: "vowels", count: vowelCount},
            {label: "consonants", count: consonantCount},
            {label: "punctuation", count: punctuationCount}
        ];

        // Create objects to hold the counts
        const totalCharCounts = [
            {label: "vowels", count: numberOfVowels},
            {label: "consonants", count: numberOfConsonants},
            {label: "punctuation", count: numberOfPunctuations}
        ];

        
        DonutChart(totalCharCounts)
        return charCounts;
    }
        
// Function to generate the donut chart
//  ============ STEP 1 ==============
    function DonutChart(dataset) {
        var width = 500;
        var height = 400;
        var margin = 50
        var radius = Math.min(width - margin, height - margin) / 2;
        var donutWidth = 50;
        console.log('Ahhh Gotcha! You came here, Welcome :)')
        console.log('Check out my LinkedIn: https://www.linkedin.com/in/amey-bhilegaonkar')
        d3.select('#pie_svg').selectAll('*').remove();
        var svg = d3.select('#pie_svg')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', 'translate(' + (width / 2) + ',' + ((height / 2) )  + ')');


        var arc = d3.arc()
            .innerRadius(radius - donutWidth)
            .outerRadius(radius);

        var pie = d3.pie()
            .value(function(d) { return d.count; })
            .sort(null);

        var path = svg.selectAll('path')
            .data(pie(dataset))
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', function(d, i) {
                return color(i);
            })
            .style('stroke-width', '1px')
            .style('stroke', 'black')
            .on('mouseover', function(eventt,d) {
                d3.select(this)
                .style('stroke-width', '4px')
                .style('stroke', 'black'); 
                svg.selectAll('#textMiddle').remove();
                svg.append('text')
                    .attr('text-anchor', 'middle')
                    .attr('dy', '.3em')
                    .attr('id', 'textMiddle')
                    .text(d.data.label + ': ' + d.data.count);

            })
            .on('mouseout', function() {
                d3.select(this) 
                .style('stroke-width', '1px') 
                .style('stroke', 'none');
                svg.selectAll('#textMiddle').remove();
            })

            .on("click", function(event, d) {
                var selectedColor = color(d.index);
                var selectedData = charList.find(item => item.label === d.data.label).count;
                createBarChart(selectedData, selectedColor);
            });

    }


    // Function to show the tooltip
    // ========== UTILITY FUNCTIONS FOR BAR CHART ================
    // ========== STEP 3 ==========
    function showTooltip(tooltip, event, d) {
        tooltip
            .html(
            `<div>Character: ${d.label} <br> Count: ${d.count}</div>`
            )
            .style('visibility', 'visible')
            .style('top', event.pageY - 10 + 'px')
            .style('left', event.pageX + 10 + 'px');
        d3.select(this).transition();
    }
    
    function moveTooltip(tooltip) {
        tooltip
        .style('top', event.pageY - 10 + 'px')
        .style('left', event.pageX + 10 + 'px');
    }
    
    function hideTooltip(tooltip) {
        tooltip.html(``).style('visibility', 'hidden');
            d3.select(this).transition();
    }
    
    // STEP 2
    function createBarChart(data, selectedColor) {

        var svgWidth = 500;
        var svgHeight = 400;
        var margin = { top: 20, right: 20, bottom: 30, left: 40 };

        var tooltip = d3
        .select('body')
        .append('div')
        .attr('class', 'd3-tooltip')
        .style('position', 'absolute')
        .style('z-index', '10')
        .style('visibility', 'hidden')
        .style('padding', '10px')
        .style('background', 'white')
        .style('border', '1px solid #ccc')
        .style('border-radius', '4px')
        .style('color', 'black');

        var width = svgWidth - margin.left - margin.right;
        var height = svgHeight - margin.top - margin.bottom;


        d3.select("#bar_svg").selectAll("*").remove();

        var svg = d3.select("#bar_svg")
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var xScale = d3.scaleBand()
            .domain(data.map(function (d) { return d.label; }))
            .range([0, width])
            .padding(0.1);

        var yScale = d3.scaleLinear()
            .domain([0, d3.max(data, function (d) { return d.count; })])
            .nice()
            .range([height, 0]);

        svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) { return xScale(d.label); })
            .attr("y", function (d) { return yScale(d.count); })
            .attr("width", xScale.bandwidth())
            .attr("height", function (d) { return height - yScale(d.count); })
            .attr("fill", selectedColor)
            // ======== STEP 3 ==========
            .on('mouseover', function (event, d) {
                showTooltip(tooltip, event, d);
                d3.select("#character-name").text(d.label);
                d3.select("#character-count").text(d.count);
            })
            .on('mousemove', function () {
                moveTooltip(tooltip);
            })
            .on('mouseout', function () {
                hideTooltip(tooltip)
                d3.select("#character-name").text("selected character");
                d3.select("#character-count").text("NONE");
            });

        svg.append("g")
            .attr("class", "x-axis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(xScale));

        svg.append("g")
            .attr("class", "y-axis")
            .call(d3.axisLeft(yScale));
    }
