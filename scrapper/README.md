
# City Population Scrapper
If the population of the city is high an ad will be viewed by more times. <br>
Thus population of a city can be a factor which influences the probability of ad being clicked in that city. <br>
That is why I decided to scrap data from Wikipedia.<br>
All of the population counts are extracted from Russian Wikipedia site since all the cities don't have a page on the English Wikipedia website.
<br>

## Workflow
1. Get list of unique city names from training data.
2. Search for the city name on Russian Wikipedia.
3. Locate the infobox element.
4. Extract the population string within the infobox.
5. Append to the dataframe.

