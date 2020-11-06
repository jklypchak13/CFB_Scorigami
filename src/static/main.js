console.log("Hi")

for (let i = 0; i < 300; i++) {
  for (let j = 0; j < 300; j++) {
    let current = document.getElementById(i + "_" + j)
    current.addEventListener("onclick", function() {
      console.log(i + " " + j)
    })
  }
}
