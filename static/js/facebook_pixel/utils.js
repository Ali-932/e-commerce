function convertIQDtoUSD(iqdAmount) {
    const exchangeRate = 145000 / 100; // 145,000 IQD for 100 USD
    const usdAmount = iqdAmount / exchangeRate;
    return usdAmount.toFixed(3);
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
