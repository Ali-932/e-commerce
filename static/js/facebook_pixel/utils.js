function convertIQDtoUSD(iqdAmount) {
    const exchangeRate = 145000 / 100; // 145,000 IQD for 100 USD
    const usdAmount = iqdAmount / exchangeRate;
    return usdAmount.toFixed(3);
}