const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
});


document.getElementById('categorySelect').addEventListener('change', function () {
  var selectedValue = this.value;
  if (selectedValue !== "Categorías") {
      window.location.href = selectedValue;
  }
});