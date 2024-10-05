document.getElementById('categorySelect').addEventListener('change', function () {
  var selectedValue = this.value;
  if (selectedValue !== "Categorías") {
      window.location.href = selectedValue;
  }
});


const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
});


document.addEventListener('DOMContentLoaded', function () {
  // Main banner carousel
  var mainCarousel = new bootstrap.Carousel(document.getElementById('mainCarousel'), {
    interval: 10000
  });

  // Product carousel
  var productCarousel = new bootstrap.Carousel(document.getElementById('productCarousel'), {
    interval: false
  });
});


$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})


function agregarProductoKit(precio) {
  let totalPriceElement = document.getElementById("total-price");
  let totalPrice = parseFloat(totalPriceElement.textContent);

  totalPrice += precio;

  totalPriceElement.textContent = totalPrice.toFixed(2);

  $('#exampleModalCenter').modal('hide');
}

function agregarProductoKit(precio) {
  let totalPriceElement = document.getElementById("total-price");
  let totalPrice = parseFloat(totalPriceElement.textContent);

  totalPrice += precio;

  totalPriceElement.textContent = totalPrice.toFixed(2);

  $('#exampleModalFunda').modal('hide');
}

function agregarProductoKit(precio) {
  let totalPriceElement = document.getElementById("total-price");
  let totalPrice = parseFloat(totalPriceElement.textContent);

  totalPrice += precio;

  totalPriceElement.textContent = totalPrice.toFixed(2);

  $('#exampleModalAudi').modal('hide');
}


/*FUNCIONALIDAD*/
function displayProducts(products, containerId) {
  const productContainer = document.getElementById(containerId);
  productContainer.innerHTML = '';
  products.forEach(product => {
    const productDiv = document.createElement('div');
    productDiv.className = 'col-md-4';
    productDiv.innerHTML = `
          <div class="product card">
              <img src="${product.image}" alt="${product.name}" class="card-img-top">
              <div class="card-body">
                  <h5 class="card-title">${product.name}</h5>
                  <p class="card-text">${product.price}</p>
              </div>
          </div>
      `;
    productContainer.appendChild(productDiv);
  });
}

document.querySelectorAll('.category-checkbox').forEach(checkbox => {
  checkbox.addEventListener('change', showRelatedProducts);
});

function showRelatedProducts() {
  const selectedCategories = Array.from(document.querySelectorAll('.category-checkbox:checked')).map(cb => cb.value);
  const related = products.filter(product => selectedCategories.includes(product.category));
  const relatedContainer = document.getElementById('relatedProducts');
  displayProducts(related, 'relatedProducts');
  document.querySelector('.related-products').classList.toggle('hidden', related.length === 0);
}


/*Hacer el corazón rojo*/
function toggleFavorite(element) {
  element.classList.toggle("filled");
  alert("Producto agregado a favoritos");
  // Aquí puedes agregar la funcionalidad para manejar favoritos
}