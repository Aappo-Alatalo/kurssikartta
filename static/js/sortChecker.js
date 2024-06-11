// Function to retrieve the sort value from URL parameter
function getURLParameter(name) {
    return new URLSearchParams(window.location.search).get(name);
}

// Function to set the radio button checked based on the sort value from URL
function setSortFromURL() {
    var sortValue = getURLParameter('sort');
    if (sortValue) {
        document.getElementById(sortValue).checked = true;
    }
}

// Call the function on page load to set the radio button based on URL parameter
window.onload = function() {
    setSortFromURL();
}