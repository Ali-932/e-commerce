function trackAddToCart(
    contentIds = [1, 2, 3, 4],
    contentType = "product",
    currency = "IQD",
    value
) {
    const valueUSD = convertIQDtoUSD(value);
    fbq("track", "AddToCart", {
        content_ids: contentIds,
        content_type: contentType,
        currency: "USD",
        value: valueUSD,
    });
}

function CompletePurchase(totalValue, totalQuantity) {
    const totalValueUSD = convertIQDtoUSD(totalValue);
    fbq("track", "Purchase", {
        currency: "USD",
        value: totalValueUSD,
        num_items: totalQuantity,
    });
}

function InitalCheckout(totalValue) {
    const totalValueUSD = convertIQDtoUSD(totalValue);
    fbq("track", "InitiateCheckout", {
        currency: "USD",
        value: totalValueUSD,
    });
}

function MadeSearch(searchString) {
    fbq("track", "Search", {
        search_string: searchString,
    });
}

function ViewContent(contentId, contentType) {
    fbq("track", "ViewContent", {
        content_id: contentId,
        content_type: contentType,
    });
}

function RegisterForm() {
    fbq("track", "CompleteRegistration", {});
    fbq("track", "Lead", {});

}


document.body.addEventListener('htmx:afterRequest', function (event) {
    const triggerHeader = event.detail.xhr.getResponseHeader('HX-Trigger');
    if (triggerHeader) {
        try {
            const triggerData = JSON.parse(triggerHeader);
            // Get the element that initiated the htmx request
            // Extract the value of the hx-post attribute
            // Check if the hx-post attribute exists and matches the pattern, e.g. starts with "/products/"
            if (triggerData.ProductPostSuccess) {
                trackAddToCart(
                    [triggerData.params.volume_id],
                    'product',
                    'IQD',
                    triggerData.params.volume_price
                );
            }
            if (triggerData.ProductView) {
                ViewContent(triggerData.params.volume_id, 'product');
            }
            if (triggerData.SearchView) {
                MadeSearch(triggerData.params.q);
            }
            if (triggerData.InitalCheckout) {
                InitalCheckout(triggerData.params.totalCost);
            }
        } catch (error) {
            console.error('Error parsing HX-Trigger header:', error);
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    if (document.cookie.split(';').some((item) => item.trim().startsWith('registered='))) {
        RegisterForm();
        // Optionally, delete the cookie by setting its expiry in the past.
        document.cookie = 'registered=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    } else if (document.cookie.split(';').some((item) => item.trim().startsWith('ordered='))) {
        const cookieRaw = getCookie('ordered');
        orderedValue = cookieRaw.replace(/\\054/g, ',');
        const data = JSON.parse(orderedValue);
        const parsedData = JSON.parse(data);
        CompletePurchase(parsedData.total_price, parsedData.number_items);
        // Optionally, delete the cookie by setting its expiry in the past.
        document.cookie = 'ordered=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    }
});