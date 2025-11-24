import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('sample_weather.csv')

# plt.plot(data['Date'], data['Temperature'])
# plt.title('Temperature Over Time')
# plt.xlabel('Date')
# plt.ylabel('Temperature')

# data.plot(x='Date', y='Temperature', kind='line', figsize=(12,6))
# plt.title('Temperature Over Time')
# plt.xlabel('Date')
# plt.ylabel('Temperature')
# plt.tight_layout()
# plt.show()

data['Date'] = pd.to_datetime(data['Date'])    # Convert to datetime
plt.plot(data['Date'], data['Temperature'])
plt.gcf().autofmt_xdate()                     # Auto format dates for best appearance
plt.show()


# Show only every 30th date label (about one per month)
plt.xticks(ticks=range(0, len(data['Date']), 30), labels=data['Date'][::30], rotation=45)

plt.tight_layout()
plt.show()
