<h2>Background</h2>
This application helps investors research stocks based on their stagnancy. Stagnancy in stocks is how little activity or movement there is. As parameters, this application takes the ticker symbol of the stock the investor is interested in and the number of past months they want the application to use to assess the stock’s stagnancy. To assess the stock’s stagnancy the application calculates a stagnancy index. This index represents how stagnant a stock is during the past months the investor gave. The lower the stagnancy index, the more stagnant the stock is. The application also shows general statistics and graphs to aid the investor with their research.
<br>
Github Repository: https://github.com/saltekar/stock-stagnancy-measure 

<h2>Purpose</h2>
This application is used primarily for the short-term trading of stagnant stocks. The underlying concept behind this researcher is that stocks that are stagnant will eventually become volatile again. This takes advantage of the idea of implied volatility (IV). The longer a stock has little movement, the higher its implied volatility rises. In principle, this means that stagnant stocks will never stay stagnant. This application calculates a stagnancy index as a measure of a stock’s stagnancy. Of course, this concept does not guarantee positive movement in the future. Stagnant stocks may eventually fall. However, this application does provide a useful way for investors to short list stocks for further research.

<h2>Quick Guide</h2>
Ticker Symbol: ticker symbol of the stock the investor wants to research
Past Months: number of months investor wants the application to go back in data to base its stagnancy index
Stagnancy: very little or no movement
Stagnancy Index: a measure to define the stagnancy of a stock calculated by the application based on investor input. Lower the stagnancy index, the more stagnant the stock is.

<h2>FAQ</h2>
<h4>1. What is the difference between stagnancy and volatility?</h4>
  
A stock is stagnant when it has little or no movement. This application would give a stock like this a low stagnancy index.
  
Volatility is the liability to change rapidly and unpredictably. In terms of the stock market, it refers to the amount of uncertainty or risk investing in that stock brings. A stock is considered to have a high volatility when the price of that stock spreads out over a range of values. The price dramatically changes in either direction. A stock has a low volatility when there is no fluctuation and is steady. This means that a stock growing or falling at a constant rate would be considered to have a low volatility and at the same time not be stagnant.

<h4>Does a lower stagnancy always suggest more volatility in that stock in the future?</h4>
  
Short answer is no. Generally, stocks with a lower stagnancy are more likely to be volatile in the future. But, I have found that at a certain point if the stagnancy index for a stock is too low, it will most likely stay in the stagnant phase for a prolonged period. There is a range of the stagnancy index that investors should look for. This range of stagnancy indexes is roughly around 2-6. After further research, I will add a feature to the result page to help investors more accurately short list stocks for further research.


For additional questions/concerns feel free to contact saltekar@ucsd.edu
