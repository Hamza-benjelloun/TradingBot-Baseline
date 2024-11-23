# TradingBot-Baseline

A baseline Python bot for trading.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hamza-benjelloun/TradingBot-Baseline.git
   ```
2. Install the required packages in your virtual environement:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Pre Commit Hooks:
   ```bash
   pre-commit install
   ```
4. Run tests (Make sure you are using Bash):
   ```bash
   chmod +x run_test.sh && alias test="./run_test.sh"
   ```
   ```bash
   test [base_file_name]
   ```
   or
   ```bash
   test all
   ```

## Trading Strategies

### 1. Stochastic RSI and EMA Crossover Strategy

This strategy combines the Stochastic RSI, an oscillator that measures the level of RSI relative to its high-low range over a set time period, with Exponential Moving Averages (EMAs) to determine trend direction.

#### Indicators

- **Stochastic RSI (14 periods)**
- **Short EMA (9 periods)**
- **Long EMA (50 periods)**

#### Rules

**Buy Signal:**

- The Stochastic RSI crosses above 20, signaling increasing momentum.
- The 9-period EMA crosses above the 50-period EMA, indicating an upward trend.

**Sell Signal:**

- The Stochastic RSI crosses below 80, signaling decreasing momentum.
- The 9-period EMA crosses below the 50-period EMA, indicating a downward trend.

### 2. Bollinger Bands and MACD Strategy

This strategy utilizes Bollinger Bands to identify volatility and price levels relative to moving averages, combined with the MACD to confirm the trend and momentum.

#### Indicators

- **Bollinger Bands (20 periods, 2 standard deviations)**
- **MACD (12, 26, 9 periods)**

#### Rules

**Buy Signal:**

- Price touches or crosses the lower Bollinger Band.
- MACD line crosses above the signal line.

**Sell Signal:**

- Price touches or crosses the upper Bollinger Band.
- MACD line crosses below the signal line.

### 3. Parabolic SAR and ADX Strategy

The Parabolic SAR provides potential reversals in the market price direction, while the Average Directional Index (ADX) helps determine the strength of the trend.

#### Indicators

- **Parabolic SAR (0.02 step, 0.2 maximum)**
- **ADX (14 periods)**
- **Plus Directional Indicator (+DI, 14 periods)**
- **Minus Directional Indicator (-DI, 14 periods)**

#### Rules

**Buy Signal:**

- Parabolic SAR dots appear below the price, indicating an uptrend.
- ADX is above 25, indicating a strong trend.
- +DI crosses above -DI, confirming bullish strength.

**Sell Signal:**

- Parabolic SAR dots appear above the price, indicating a downtrend.
- ADX is above 25, indicating a strong trend.
- -DI crosses above +DI, confirming bearish strength.

## Implementation Tips for Scalping

- Scalping requires quick decision-making and fast execution, so ensure your trading platform can handle rapid trades.
- Test and adjust the parameters of the indicators to match the specific characteristics of the market and the assets you are trading.
- Set tight stop-loss orders to limit potential losses, as the fast-paced nature of scalping can lead to significant losses quickly.
- Consider the trading costs, as frequent trading can rack up high transaction fees.

## Roadmap

- **Core Development:**
  - [x] Main Class for the Strategy
  - [x] Main Trading Class
  - [x] Main Broker Class
  - [ ] Main Backtesting Class
  - [x] Implement RSI Strategy
  - [x] Implement Stochastic RSI Strategy
  - [ ] Implement EMA Strategy
  - [ ] Implement Bollinger Bands Strategy
  - [ ] Implement MACD Strategy
  - [ ] Implement Parabolic SAR Strategy
  - [ ] Implement ADX Strategy
  - [ ] Implement Stochastic RSI and EMA Crossover Strategy
  - [ ] Implement Bollinger Bands and MACD Strategy
  - [ ] Implement Parabolic SAR and ADX Strategy

- **Backtesting:**
  - [ ] Backtesting RSI Strategy
  - [ ] Backtesting Stochastic RSI Strategy
  - [ ] Backtesting EMA Strategy
  - [ ] Backtesting Bollinger Bands Strategy
  - [ ] Backtesting MACD Strategy
  - [ ] Backtesting Parabolic SAR Strategy
  - [ ] Backtesting ADX Strategy
  - [ ] Backtesting Stochastic RSI and EMA Crossover Strategy
  - [ ] Backtesting Bollinger Bands and MACD Strategy
  - [ ] Backtesting Parabolic SAR and ADX Strategy

- **Optimization and Improvements:**
  - [ ] Optimize Execution Speed for Scalping Strategies
  - [ ] Parameter Tuning for Each Strategy
  - [x] Implement Risk Management Rules (e.g., Stop Loss, Take Profit)
  - [ ] Add Performance Metrics and Reporting

- **User Interface (Optional):**
  - [ ] Develop Interactive UI for Strategy Management
  - [ ] Visualization of Strategy Performance
  - [ ] Real-time Monitoring Dashboard

- **Documentation:**
  - [ ] Detailed Documentation for Each Strategy
  - [ ] User Guide for Running the Bot
  - [ ] API Documentation for Broker Integration
  - [ ] Tutorials and Examples

- **Testing:**
  - [x] Unit Tests for Core Components
  - [ ] Integration Tests for Strategies
  - [ ] End-to-End Tests for Trading Bot

- **Deployment:**
  - [ ] Setup Continuous Integration and Deployment (CI/CD) Pipeline
  - [ ] Cloud Deployment (e.g., AWS, Azure)
  - [ ] Scalability and Load Testing
