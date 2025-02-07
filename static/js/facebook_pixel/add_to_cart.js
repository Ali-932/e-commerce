function trackAddToCart(
    contentIds = [1, 2, 3, 4],
    contentType = "product",
    contents = [{'id': 'ABC123', 'quantity': 2}, {'id': 'XYZ789', 'quantity': 2}],
    currency = "IQD",
    value = 30.00
) {
    fbq('track', 'AddToCart', {
        content_ids: contentIds,
        content_type: contentType,
        contents: contents,
        currency: currency,
        value: value
    });
}
