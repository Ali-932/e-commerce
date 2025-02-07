function CompletePurchase(totalValue) {
    fbq('track', 'Purchase', {
        currency: 'IQD',
        value: totalValue
    });
}