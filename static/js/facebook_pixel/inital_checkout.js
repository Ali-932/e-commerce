function InitalCheckout(
    totalValue = 30
) {
    fbq('track', 'InitiateCheckout', {
        currency: 'IQD',
        value: totalValue
    });
}