# Homework #3: Global Developments

In this homework, you'll apply knowledge about D3 animations and joins to create an animated [beeswarm chart](https://appsource.microsoft.com/en-us/product/power-bi-visuals/excelnaccesscom1597493022219.beeswarm_id?tab=overview). A beeswarm chart shows the distribution of data points along an attribute, but instead of binning or aggregating the points together (e.g., like a histogram), it emphasizes individual data points by showing them as circles. A beeswarm is an interesting chart because, while the x-axis will show the values of the selected attribute, the specific positioning of the circles does not correspond to their _exact values_. Beeswarm charts "pack" the points together to save space (like a "swarm" of bees), but they do so in a way that the points do not overlap like they would in a scatter plot. This means that the x-positions of the circles will usually be _close_ to their actual values, but not necessarily _exact_.

**Note**: The above link to the Microsoft website shows several beeswarms (one per world region). In this homework, you'll only be making one beeswarm that potentially contains multiple regions.

Your beeswarm will interactively update as countries and attributes for the dataset are changed. This assignment is worth 10 points. It will include the following aspects:

- Download the Global Development dataset (`global_development.csv`) from the CORGIS website for use in your visualization. Select ten attributes of interest that you want to visualize in your beeswarm.
- Draw a beeswarm chart on your webpage that shows a user-selected set of countries for the currently selected year (each country = one circle, the x-position of the circle is based on a user selected attribute, and the size of each circle based on a second selected attribute).
- Using HTML controls, the user can change (1) which countries are shown in the chart, (2) which global development attribute is being visualized along the x-axis, and (3) which attribute is used for circle sizes. When countries are added/removed, or when the attribute is changed, you will use D3 joins and transitions to animate the chart from the "previous state" to the updated one.
- Additionally, the user should be able to invoke a "playback" option, which will iterate through the years of your dataset. Whenever the year changes, you'll use animated transitions to update the positions of the circles in the beeswarm to the next year.

We don't give you any starter code for this assignment: you'll have to create everything from scratch, including downloading the the dataset and making the `index.html` page. You have the freedom to stylize your chart (and webpage) as desired, though points will be deducted for sloppy design.

> ❗️ This homework asks you to perform very specific animations and interactions. Be sure to carefully read the steps below! 

> ❗️ **As always, the sharing and copying code with other students is considering cheating, as is using ChatGPT, Coding co-pilots, or other generative AI. Passing off (part of) a codebase from someone else as your own is also plagiarism.**  

## Step 1: Create your dataset and initial webpage


Download the Global Development dataset from the [CORGIS website](https://corgis-edu.github.io/corgis/csv/) and pick ten attributes that you would like to visualize.

There's a `data` folder in this repository where you should place the downloaded CSV file. The data folder contains a `country_regions.csv` file which you will use to map the countries to their geographic regions (Europe & Central Asia, Latin America & Caribbean, etc.). 

> ❗️ If a country is in the CORGIS dataset, but NOT in the country regions file, or if there's a mismatch between a country in the two files (e.g., the names are spelled differently), you can either ignore it (i.e., not visualize it in your webpage) or you can manually add/fix it in the `country_regions.csv`.


Create an `index.html` page for your interface in the root directory of this assignment repository. Link to the D3 library (remember, you must use D3 v7!). You should put your Javascript code inside an external file named after your ASURITE (e.g., mine would be `cbryan16.js`). You can also create an external CSS file if you'd like, or put that code inside your `index.html`. You may also use Bootstrap if you like, though this is not required.

The exact design of your webpage is up to you, but it should include the following.

- Simlar to previous homeworks, at the top of the page, title your page and add your name and email.
- You'll need an SVG to hold your chart. Your chart should go left-to-right (not vertically) on the page. The width of the chart should be between ~800-1600 pixels; it is up to you how tall you'd like to make your SVG, so think about what makes sense based on how you size your circles. 🤔
- You'll need a control panel to hold the HTML elements for manipulating your visualization. The control panel should have the following controls (with text labels):
    - **X-axis:**: A `select` dropdown listing your ten selected attributes. The selected attribute will be what is mapped along the x-axis in the beeswarm.
    - **Size:**: A `select` dropdown listing your ten selected attributes. The selected attribute will be what is mapped to the circle size in the beeswarm.
    - **Regions**: You should have a way to select one or more regions (the `World bank region` column in the `country_regions.csv` file). There are seven regions here. The countries for the currently selected regions wil be what is shown in the chart. You should also add controls or widgets that let you do "Select All" and "Deselect All" actions which will select (or deselect) all seven regions. It is up to you exactly how you want to implement this Regions functionality, though my suggestion would be something like organizing the set of checkboxes inside a `div` or a `select` dropdown ([here's an example](https://stackoverflow.com/questions/25016848/bootstrap-putting-checkbox-in-a-dropdown) of the latter).
    - **Year**: Year: An `<input type='number'>` element ([link](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number)) that denotes the currently selected year. The selected year will be what is shown in the chart. Optionally, you can also add a range slider beside this element that lets the user modify the year by scrubbing along the slider. If you do this, make sure both elements update to show the same values.
    - **Play**: A control that lets the user animate the years in the beeswarm. One way to do this is with an `<input type='button'>` element. When pressed, the chart will begin animating through the years. If pressed again, the animation will stop on the current year. When the playback is paused, the button's text should read "Play". When playback is currently happening, the button's text should read "Pause" or "Stop". Alternatively, instead of a "Play" button, you could add an icon or image looks like a play button. 

My suggestion is to place these elements in a control panel area, either to the side of the chart or above or below it, so they can be organized in a way that makes sense. Controls should use consistent styling/theme. Feel free to use Bootstrap or custom CSS to do this.


## Step 2: Import (and wrangle?) your dataset

Import the two CSV files into your page: the CORGIS `global_development.csv` file and the `countries_regions.csv` file. You may do any data wrangling you feel is necessary, either before or after importing your csv files. The point of this step is to get the dataset to a point where, based on the user interacting with the HTML controls, the beeswarm chart can update appropriately.

> 🔍 The dataset goes from 1980-2013, though some countries may be missing data for certain years. If a country attribute starts after 1980, or stops prior to 2013, you can stop drawing it in the chart at that point. If a country has a "gap" year (e.g., say there's data for 1990 and 1992, but not 1991), you can remove the country when you go to 1991, and re-add it for 1992.

## Step 3: Beeswarm chart encodings and interactions

The default encodings for your beeswarm chart should be the following:
- Put an x-axis at the bottom of your SVG (the beeswarm plot will go above it). The min/max of the x-axis will be the min/max values for the selected attribute from the **X-axis** dropdown, for the selected set of countries (chosen from the **Regions** part of your control panel), over the entire timeline (i.e., 1980-2013). You should have an axis label somewhere on this beeswarm, labeling the currently selected attribute.
- For each selected region, the countries from that region will be displayed in the beeswarm chart. Each country should be drawn using a circle with a dark (black or dark gray) border 1px thick. The size of the circles should correspond to the **Size** dropdown. You're allowed to choose how small/big you want to draw the circles on the SVG based on the min/max values. (I'd suggest values between ~4-60 px, but you may choose what you think looks good.)
- The circles for each region should have their own distinct color hue (e.g., all Latin America & Caribbean countries are color A, while Europe & Central Asia countries are color B, etc.). You can use one of D3's predefined color scales for this, or create your own. Note that we only want you to draw one beeswarm that contains ALL of the circle countries, not one beeswarm for each region.

As discussed above, beeswarm charts "pack" their circles together, meaning that circles will be "close" to their attribute values on the x-axis, though they might not be exact.
One challenge then, is how to accomplish this packing without making the circles overlap each other. If the circles are the same size, this is not a difficult algorithm to implement (the D3 documentation for a beeswarm does this: [link](https://observablehq.com/@d3/beeswarm/2)), but this solution does not work well in practice when circle sizes vary a lot ([example](https://observablehq.com/@yurivish/building-a-better-beeswarm)) because it results in a lot of whitespace.

A better solution is to use D3's force layout to compute the positioning ([example1](https://www.chartfleau.com/tutorials/d3swarm), [example2](https://observablehq.com/@harrystevens/force-directed-beeswarm)). To do this, each circle will be attracted to its appropriate x-position along the x-axis, and all circles will be attracted to the same vertical position (e.g., y = 0). To prevent circles from overlapping, D3's force layout simulator provides a collision force detector, that will push circles off each other if they overlap. You can set the radius of the collision force equal to the size of each individual circle to do this, or add a couple of pixels extra if you'd like some padding. 

> ❗️ You are not **required** to use D3's force layout to lay out the circle positions in the beeswarm 

Your beeswarm should support the following interactions:
- When the **Year** changes, animate each country from its current position to its new position based on their attribute values for the new year. Importantly, circles should ONLY move once: from their "old" position to the "updated" position. If you are using D3's force layout to compute this, you should not show the x/y positions at every "tick" of the force layout simulator. Instead, compute the finalized x/y position (i.e., after the layout simulator stops), and only then animate the circles. Moreover, instead of moving all of the circles at the same time, you should perform a **staggered transition** that delays the starting times of the animations of some points ([see this page for an example](https://d3-graph-gallery.com/graph/interactivity_transition.html)). (I'd suggest delaying the start times of each data point between 0-500 ms, either randomly or based on some logical function.) Then, the duration of the actual transition for each point should be between 500-1000 ms. 
- When the **X-Axis** value is updated, perform the following actions: 
    - First, compute your new min/max based on the new attribute.
    - Then, remove the current x-axis label by fading out its opacity from 100% to 0%.
    - Once this is done, then animate the x-axis from the old to the new values (i.e., from the old min/max to the new min/max: [example](https://observablehq.com/@jonhelfman/data-and-axes-transitions)).
    - Once the axis transition completes, fade in the updated axis label (going from 0% to 100% opacity to be visible).
    - Once this is done, transition the country circles to their new x/y positions. This transition should use the same staggered-style animation like when the **Year** is changed (i.e., delaying the start of some points, and using the same transition durations).
- When the **Size** axis is changed, you'll need to adjust the sizes of the circles, but this will also require you to update the x/y positions the circles to make sure they're "packed" correctly. Move the circles by performing a staggered animation (like what is done when the **Year** is changed, with similar delay and duration behavior), except now as you the move the circles, you should also resize them from their old to new sizes during the transition.
- When the **Region** selections are changed (e.g., you click or de-click a checkbox in this panel), you'll either add or remove countries to the beeswarm. Do this by performing the following actions: 
    - First, recompute your x-axis min/max, and update the x-axis by animating from the old to new min/max values. 
    - Once this is done, if you are **removing** countries from the beeswarm, remove these countries by animating their circles using an animated transition that either animates their opacity to 0%, or shrinks their size to 0 (and then removes them from the DOM).
    - Once any outgoing countries are removed, use a second staggered transition to move the remaining countries to their correct (updated) x/y positions. Keep in mind, when countries are added/removed, you might need to recompute the circle min/max sizes; if so, transition the sizes of the circles as they are moved. Also remember, you should ONLY do one animation, from the "old" to "new" x/y positions, and not show every "tick" of the force layout. 
    - Finally, if you are **adding** new countries, once the current countries have finished their animations, use a final transition to fade in these countries, either transitioning their opacity from 0% to 100%, or growing their size from 0 px to the appropriate size. (Depending on how you implement this actoin, your new countries will either likely "fill in" gaps in the beeswarm layout that the current countries are positioned around, or they will be added to the outside "edges" of the beeswarm. Either approach is allowed.)
- If the user hovers over a country's circle, show a tooltip that shows the full name of the country as well as its values for the x-axis attribute and size attribute. (Consider re-using/modifying your tooltip code from Assignment #2 for this requirement.)
- Finally, if the **Play** button is clicked, begin iterating through years. The circles in the beeswarm should fully animate for each year they update using the staggered animation described when the **Year** control is updated. Each year should fully finish its animation before the next year's animation begin, and likewise the **Year** control's text should likewise update with each increment. If you reach the last year of the dataset, stop the animation. Likewise, if the user clicks the **Play** button again to stop the playback, then stop the animation on that year. It's up to you how fast you want to animate (though don't go "too fast" and zip right to the end; pick a reasonable speed), but the countries should reach their value at each timestep before the next year is called (i.e., don't change transitions half-way through, let the countries finish animating). 

> 🔍 Use [D3 joins](https://observablehq.com/@d3/selection-join) to control how countries change positions and appear/disappear. When animating countries to new positions (via year changes or via selecting a new X-axis or Size attribute), you can use the update functionality of D3 joins. When adding new countries to the chart (when the region is updated to a new set of countries), use the enter functionality of D3 joins. When removing countries (when the region is updated and the current set of countries needs to be removed), use the exit functionality of D3 joins.

## Grading 

This assignment is worth 10 points.
- Step 1 is worth 1 point.
- Step 2 is worth 2 points.
- Step 3 is worth 7 points.

## Extra Credit Opportunities

There are four ways you can potentially receive extra credit for this assignment. A maximum of 5 extra credit points can be added to this assignment.

- If your webpage is designed/styled in an especially attractive way that the grader likes. (+1)
- If your interface supports more than the minimum number of four GapMinder attributes/indicators. (+1)
- If you add a key for your beeswarm indicating the circle sizes. This key should update appropriately based on user actions and data updates. (+1)
- When the tooltip is displayed, in addition to showing the country being hovered over (and its values), also show a picture or icon that represents that country inside the tooltip. (+1)
- Alongside the beeswarm (either to the side or below), implement a [box plot](https://d3-graph-gallery.com/graph/boxplot_basic.html) that aggregates the information about the selected regions for a user selected attribute, for the currently selected year. The countries for a region should be summarized using one box (meaning that if you have X regions selected in the beeswarm, you'll be showing X boxes in the box plot). You'll need to add an extra drop down in your control panel to let the user select the attribute they want shown in the box plot. When the **Year** or **Regions** are updated, the box plot should likewise be updated. The specifics of the design and how it's updated (e.g., via animations or by simply redrawing) are up to you; use your own intuition about how to make it look nice, label your data points, and fit its interactions into the larger user interface and user experience of the overall application. (up to +4)




