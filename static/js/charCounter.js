let textbox = document.getElementById("textbox");
let count = document.getElementById("count");

function updateCount() {
  count.innerHTML = textbox.innerText.length;
  if(textbox.innerText.length > 500) {
    count.style.color = "red";
  } else {
    count.style.color = "black";
  }
}

textbox.oninput = updateCount;