import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_weather(data):
    """
    Analyze weather data and return basic statistics and plots.
    
    Parameters:
    data (pandas.DataFrame): DataFrame with columns: date, temperature, rainfall, humidity
    """
    # Convert date and add month column
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.month
    
    # Calculate basic statistics
    stats = {
        'temperature': {
            'mean': data['temperature'].mean(),
            'max': data['temperature'].max(),
            'min': data['temperature'].min()
        },
        'rainfall': {
            'mean': data['rainfall'].mean(),
            'max': data['rainfall'].max(),
            'total': data['rainfall'].sum()
        },
        'humidity': {
            'mean': data['humidity'].mean(),
            'max': data['humidity'].max(),
            'min': data['humidity'].min()
        }
    }
    
    # Find unusual weather days (beyond 2 standard deviations)
    unusual_temp = data[abs(data['temperature'] - data['temperature'].mean()) > 
                       2 * data['temperature'].std()]
    
    # Create visualizations
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
    
    # Plot 1: Monthly temperature trends
    sns.boxplot(data=data, x='month', y='temperature', ax=ax1)
    ax1.set_title('Monthly Temperature Distribution')
    
    # Plot 2: Correlation heatmap
    correlation = data[['temperature', 'rainfall', 'humidity']].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax2)
    ax2.set_title('Weather Parameters Correlation')
    
    # Plot 3: Temperature histogram
    sns.histplot(data['temperature'], bins=20, kde=True, ax=ax3, color='skyblue')
    ax3.set_title('Temperature Distribution')
    ax3.set_xlabel('Temperature')
    ax3.set_ylabel('Frequency')
    
    plt.tight_layout()
    
    return stats, unusual_temp, fig

# Example usage:
if _name_ == "_main_":
    # Create sample data
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    sample_data = pd.DataFrame({
        'date': dates,
        'temperature': np.random.normal(20, 5, len(dates)),
        'rainfall': np.random.exponential(5, len(dates)),
        'humidity': np.random.normal(70, 10, len(dates))
    })
    
    # Run analysis
    stats, unusual_days, plots = analyze_weather(sample_data)
    
    # Print results
    print("\nWeather Statistics:")
    print("-" * 20)
    for param, values in stats.items():
        print(f"\n{param.capitalize()}:")
        for stat, value in values.items():
            print(f"{stat}: {value:.2f}")
    
    print("\nUnusual Temperature Days:")
    print(unusual_days[['date', 'temperature']].to_string())
    
    plt.show()
