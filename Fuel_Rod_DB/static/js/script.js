// When the user clicks on div, open the popup
function myFunction(pk) {
    var popup = document.getElementById(`myPopup${pk}`);
    popup.classList.toggle("show");
}