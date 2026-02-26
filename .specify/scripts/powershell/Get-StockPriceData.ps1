# Get-StockPriceData.ps1

# Script to fetch the latest company stock price and historical data for the last 5 days using Alpha Vantage API.

param(
    [string]$apiKey = "YOUR_API_KEY",
    [string]$symbol = "AAPL"  # Default to Apple Inc.
)

function Get-StockPrice {
    param(
        [string]$symbol
    )

    $url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=$symbol&interval=5min&apikey=$apiKey"
    $response = Invoke-RestMethod -Uri $url -Method Get
    return $response
}

function Get-HistoricalData {
    param(
        [string]$symbol
    )

    $url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=$symbol&apikey=$apiKey"
    $response = Invoke-RestMethod -Uri $url -Method Get

    # Get data for the last 5 days
    $dates = $response.'Time Series (Daily)'.PSObject.Properties | Sort-Object -Property Name -Descending | Select-Object -First 5
    $historicalData = @{}
    foreach ($date in $dates) {
        $historicalData[$date.Name] = $date.Value
    }
    return $historicalData
}

# Main execution
$latestData = Get-StockPrice -symbol $symbol
$historicalData = Get-HistoricalData -symbol $symbol

# Output the data
Write-Output "Latest Price Data:" 
$latestData

Write-Output "Historical Data for the Last 5 Days:"  
$historicalData
