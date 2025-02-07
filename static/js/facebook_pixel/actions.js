function trackAddToCart(
  contentIds = [1, 2, 3, 4],
  contentType = "product",
  contents = [{ id: "ABC123", quantity: 2 }, { id: "XYZ789", quantity: 2 }],
  currency = "IQD",
  value = 30.00
) {
  const valueUSD = convertIQDtoUSD(value);
  fbq("track", "AddToCart", {
    content_ids: contentIds,
    content_type: contentType,
    contents: contents,
    currency: "USD",
    value: valueUSD,
  });
}

function CompletePurchase(totalValue) {
  const totalValueUSD = convertIQDtoUSD(totalValue);
  fbq("track", "Purchase", {
    currency: "USD",
    value: totalValueUSD,
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

// Complete Registration
["htmx:afterSwap", "DOMContentLoaded"].forEach((eventName) => {
  document.addEventListener(eventName, () => {
    let registrationForm = document.getElementById("registrationForm");
    if (registrationForm) {
      registrationForm.addEventListener("submit", (e) => {
        // Track the CompleteRegistration and Lead events upon form submission
        fbq("track", "CompleteRegistration", {});
        fbq("track", "Lead", {});
      });
    }
  });
});