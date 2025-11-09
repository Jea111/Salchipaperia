function confirmarPedido() {
  const carrito = localStorage.getItem("carrito");
  if (!carrito || carrito === "[]") {
    Toastify({
      text: "Tu carrito está vacío",
      backgroundColor: "red",
      duration: 2000,
    }).showToast();
    return;
  }

  window.location.href = "/pedidos/";
}

let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

function enviarPedido(event) {
  const card = event.target.closest(".card");
  const nombre = card.querySelector(".card-title").textContent;
  const precio = parseFloat(card.querySelector(".card-price").textContent);
  const id = card.dataset.productoId; // Necesitamos agregar este atributo al HTML

  const producto = {
    id: parseInt(id),
    nombre,
    precio,
    cantidad: 1,
  };

  carrito.push(producto);
  localStorage.setItem("carrito", JSON.stringify(carrito));

  Toastify({
    text: `${nombre} agregado al carrito`,
    backgroundColor: "green",
    duration: 2000,
  }).showToast();

  actualizarCarritoVisual();
}

document.addEventListener("DOMContentLoaded", function () {
  const carritoSidebar = document.getElementById("carrito-sidebar");
  const toggleBtn = document.getElementById("toggle-carrito-btn");

  if (!carritoSidebar || !toggleBtn) {
    console.warn("⚠️ No se encontró el carrito o el botón para abrirlo");
    return;
  }

  window.toggleCarrito = function () {
    console.log("Toggle carrito clicked");
    carritoSidebar.classList.toggle("active");
    console.log("Carrito classes:", carritoSidebar.classList.toString());
    actualizarCarritoVisual();
  };

  actualizarCarritoVisual();

  document.addEventListener("click", function (e) {
    if (
      !carritoSidebar.contains(e.target) &&
      !toggleBtn.contains(e.target) &&
      carritoSidebar.classList.contains("active")
    ) {
      carritoSidebar.classList.remove("active");
    }
  });
});

function actualizarCarritoVisual() {
  const contenedor = document.getElementById("carrito-lista");
  const badgeCarrito = document.querySelector("#toggle-carrito-btn .badge");

  if (!contenedor) return;

  contenedor.innerHTML = "";

  if (carrito.length === 0) {
    contenedor.innerHTML = `
      <div class="text-center p-3">
        <i class="fas fa-shopping-cart mb-3" style="font-size: 2em; color: #ccc;"></i>
        <p>Tu carrito está vacío</p>
      </div>`;
    badgeCarrito.textContent = "🛒";
    return;
  }

  let total = 0;

  carrito.forEach((item, index) => {
    const subtotal = item.precio * item.cantidad;
    total += subtotal;
    const div = document.createElement("div");
    div.classList.add("carrito-item");
    div.innerHTML = `
      <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
        <div>
          <h6 class="mb-0">${item.nombre}</h6>
          <small class="text-muted">
            $${item.precio.toFixed(2)} × ${item.cantidad}
            <br>
            <span class="badge bg-light text-dark">ID: ${item.id}</span>
          </small>
        </div>
        <div class="d-flex align-items-center">
          <button class="btn btn-sm btn-outline-secondary me-2" onclick="actualizarCantidad(${index}, -1)">-</button>
          <span class="mx-2">${item.cantidad}</span>
          <button class="btn btn-sm btn-outline-secondary me-2" onclick="actualizarCantidad(${index}, 1)">+</button>
          <button class="btn btn-sm btn-danger" onclick="eliminarDelCarrito(${index})">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    `;
    contenedor.appendChild(div);
  });

  // Agregar total
  const totalDiv = document.createElement("div");
  totalDiv.className = "p-3 bg-light mt-3";
  totalDiv.innerHTML = `
    <h5 class="mb-0 text-end">Total: $${total.toFixed(2)}</h5>
  `;
  contenedor.appendChild(totalDiv);

  badgeCarrito.textContent = `🛒 ${carrito.length}`;
}

function actualizarCantidad(index, delta) {
  carrito[index].cantidad = Math.max(1, carrito[index].cantidad + delta);
  localStorage.setItem("carrito", JSON.stringify(carrito));
  actualizarCarritoVisual();
}

function eliminarDelCarrito(index) {
  carrito.splice(index, 1);
  localStorage.setItem("carrito", JSON.stringify(carrito));
  actualizarCarritoVisual();

  if (carrito.length === 0) {
    const carritoSidebar = document.getElementById("carrito-sidebar");
    if (carritoSidebar) {
      carritoSidebar.classList.remove("open");
    }
  }
}
