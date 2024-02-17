import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from statsmodels.tsa.arima.model import ARIMA

class KeywordTrendAnalyzer:
    def get_keyword_trend(self, keyword):
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='', gprop='')

        trend_data = pytrends.interest_over_time()
        return trend_data

    def predict_trend(self, trend_data, forecast_steps=6):
        trend_data.reset_index(inplace=True)
        trend_data.rename(columns={'date': 'ds', trend_data.columns[1]: 'y'}, inplace=True)

        # Prepare ARIMA model
        model = ARIMA(trend_data['y'], order=(5, 1, 0))  # Replace with appropriate ARIMA order
        model_fit = model.fit()

        # Forecast next steps
        forecast_steps = max(forecast_steps, 1)  # Ensure a positive number of forecast steps
        forecast_index = pd.date_range(start=trend_data['ds'].iloc[-1], periods=forecast_steps+1, freq='M')[1:]
        forecast = model_fit.forecast(steps=forecast_steps)
        
        forecast_df = pd.DataFrame({'ds': forecast_index, 'predicted_mean': forecast})

        return forecast_df

# Usage
if __name__ == "__main__":
    keyword = input("Enter a Keyword: ")

    trend_analyzer = KeywordTrendAnalyzer()
    trend_data = trend_analyzer.get_keyword_trend(keyword)
    
    if not trend_data.empty:
        print("Keyword Trend Data:")
        print(trend_data)

        # Predict the next 1 months' trend
        forecast_steps = 1
        forecast = trend_analyzer.predict_trend(trend_data, forecast_steps)

        print(trend_data)

        print("Forecast:")
        print("by "+ forecast['ds'].to_string().replace("89   ", "") +", --- "+ keyword +" --- is expected to reach "+ forecast['predicted_mean'].to_string().replace("89    ", ""))

        # Plot historical data and forecast start line
        plt.figure(figsize=(10, 6))
        plt.plot(trend_data['ds'], trend_data['y'], label='Historical Trend', color='blue')

        # Calculate and plot the moving average
        moving_avg = trend_data['y'].rolling(window=4).mean()  # Change window size as needed
        plt.plot(trend_data['ds'], moving_avg, label='Moving Average', color='green', linestyle='dashed')

        plt.title(f"Trends for '{keyword}' with Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Interest over Time")
        
        # Set y-axis limits to ensure scale from 0 to 100
        plt.ylim(0, 100)
        
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("No trend data available.")