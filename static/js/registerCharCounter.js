let passwordTextbox = document.getElementById("passwordtextbox");
let passwordCount = document.getElementById("passwordcount");
function updatePasswordCount() {
    passwordCount.innerHTML = passwordTextbox.value.length;
    if(passwordTextbox.value.length < 8) {
      passwordCount.style.color = "red";
    } else {
      passwordCount.style.color = "green";
    }
}
passwordCount.style.color = "red";
passwordTextbox.oninput = updatePasswordCount;