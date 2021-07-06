window.addEventListener("submit", (e) => {
  e.stopPropagation()
  console.log(this)
  const loader = document.getElementById("loader");
  loader.classList.remove("hidden"); // class "loader hidden"
});
