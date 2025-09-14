alert("si esta enlazado");
let carrito = [];
let carritoAbierto = false;

const enviarPedido = (e) => {
  const card = e.target.closest(".card-body");
  const name = card.querySelector(".card-title").textContent;
  const priceText = card.querySelector(".card-price").textContent;
  const price = parseFloat(priceText);

  const productoExistente = carrito.find((item) => item.nombre === name);

  if (productoExistente) {
    productoExistente.cantidad++;
  } else {
    carrito.push({
      nombre: name,
      precio: price,
      cantidad: 1,
    });
  }

  actualizarCarrito();

  mostrarNotificacion(`${name} agregado al carrito`);
};

const actualizarCarrito = () => {
  const carritoLista = document.querySelector("#carrito-lista");

  if (carrito.length === 0) {
    carritoLista.innerHTML =
      '<p class="text-center text-muted">Tu carrito está vacío</p>';
    return;
  }

  let html = "";
  let total = 0;

  carrito.forEach((producto, index) => {
    const subtotal = producto.precio * producto.cantidad;
    total += subtotal;

    html += `
            <div class="border-bottom mb-3 pb-3">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${producto.nombre}</h6>
                        <small class="text-muted">$${producto.precio.toFixed(
                          2
                        )} c/u</small>
                    </div>
                    <div class="d-flex align-items-center">
                        <div class="btn-group btn-group-sm" role="group">
                            <button class="btn btn-outline-secondary" onclick="cambiarCantidad(${index}, -1)">-</button>
                            <button class="btn btn-outline-secondary disabled">${
                              producto.cantidad
                            }</button>
                            <button class="btn btn-outline-secondary" onclick="cambiarCantidad(${index}, 1)">+</button>
                        </div>
                        <button class="btn btn-sm btn-danger ms-2" onclick="eliminarProducto(${index})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="text-end mt-2">
                    <small class="fw-bold">Subtotal: $${subtotal.toFixed(
                      2
                    )}</small>
                </div>
            </div>
        `;
  });

  html += `
        <div class="mt-3 p-3 bg-light rounded">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Total:</h5>
                <h4 class="mb-0 text-success">$${total.toFixed(2)}</h4>
            </div>
        </div>
    `;

  carritoLista.innerHTML = html;

  actualizarContadorCarrito();
};

const cambiarCantidad = (index, cambio) => {
  carrito[index].cantidad += cambio;

  if (carrito[index].cantidad <= 0) {
    eliminarProducto(index);
  } else {
    actualizarCarrito();
  }
};

const eliminarProducto = (index) => {
  const producto = carrito[index];
  carrito.splice(index, 1);
  actualizarCarrito();
  mostrarNotificacion(`${producto.nombre} eliminado del carrito`);
};

const toggleCarrito = () => {
  const carritoSidebar = document.querySelector("#carrito-sidebar");
  carritoAbierto = !carritoAbierto;

  if (carritoAbierto) {
    carritoSidebar.style.right = "0";
  } else {
    carritoSidebar.style.right = "-400px";
  }
};

const actualizarContadorCarrito = () => {
  const toggleBtn = document.querySelector("#toggle-carrito-btn");
  const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);

  if (totalItems > 0) {
    toggleBtn.innerHTML = `🛒 <span class="badge bg-danger">${totalItems}</span>`;
  } else {
    toggleBtn.innerHTML = "🛒";
  }
};

const confirmarPedido = () => {
  if (carrito.length === 0) {
    alert(
      "Tu carrito está vacío. Agrega productos antes de confirmar el pedido."
    );
    return;
  }

  let mensaje = "📋 RESUMEN DE TU PEDIDO:\n\n";
  let total = 0;

  carrito.forEach((producto) => {
    const subtotal = producto.precio * producto.cantidad;
    total += subtotal;
    mensaje += `${producto.nombre}\n`;
    mensaje += `  Cantidad: ${producto.cantidad} x $${producto.precio.toFixed(
      2
    )} = $${subtotal.toFixed(2)}\n\n`;
  });

  mensaje += `──────────────\n`;
  mensaje += `TOTAL: $${total.toFixed(2)}\n\n`;
  mensaje += "¿Confirmas tu pedido?";

  if (confirm(mensaje)) {
    alert(
      "¡Pedido confirmado! Te contactaremos pronto para coordinar la entrega."
    );

    carrito = [];
    actualizarCarrito();
    toggleCarrito();
  }
};

const mostrarNotificacion = (mensaje) => {
  let toastContainer = document.querySelector("#toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "toast-container";
    toastContainer.className =
      "position-fixed bottom-0 start-50 translate-middle-x p-3";
    toastContainer.style.zIndex = "11";
    document.body.appendChild(toastContainer);
  }

  // Crear toast
  const toastId = `toast-${Date.now()}`;
  const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-success border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${mensaje}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

  toastContainer.insertAdjacentHTML("beforeend", toastHTML);

  const toastElement = document.getElementById(toastId);
  const toast = new bootstrap.Toast(toastElement, {
    autohide: true,
    delay: 3000,
  });
  toast.show();

  toastElement.addEventListener("hidden.bs.toast", () => {
    toastElement.remove();
  });
};

document.addEventListener("DOMContentLoaded", () => {
  actualizarCarrito();

  const carritoSidebar = document.querySelector("#carrito-sidebar");
  if (carritoSidebar) {
    carritoSidebar.style.position = "fixed";
    carritoSidebar.style.right = "-400px";
    carritoSidebar.style.top = "0";
    carritoSidebar.style.width = "400px";
    carritoSidebar.style.height = "100vh";
    carritoSidebar.style.backgroundColor = "white";
    carritoSidebar.style.boxShadow = "-2px 0 10px rgba(0,0,0,0.1)";
    carritoSidebar.style.transition = "right 0.3s ease";
    carritoSidebar.style.zIndex = "1050";
    carritoSidebar.style.display = "flex";
    carritoSidebar.style.flexDirection = "column";
    carritoSidebar.style.maxWidth = "100%";
  }

  const toggleBtn = document.querySelector("#toggle-carrito-btn");
  if (toggleBtn) {
    toggleBtn.style.position = "fixed";
    toggleBtn.style.bottom = "30px";
    toggleBtn.style.right = "30px";
    toggleBtn.style.zIndex = "1040";
    toggleBtn.classList.add("rounded-circle", "shadow");
    toggleBtn.style.width = "60px";
    toggleBtn.style.height = "60px";
  }

  const categoryBtns = document.querySelectorAll(".category-btn");
  const productItems = document.querySelectorAll(".product-item");

  categoryBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      categoryBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const category = btn.getAttribute("data-category");

      productItems.forEach((item) => {
        if (
          category === "all" ||
          item.getAttribute("data-category") === category
        ) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  });

  const addToCartBtns = document.querySelectorAll(".add-to-cart-btn");
  addToCartBtns.forEach((btn) => {
    btn.onclick = enviarPedido;
  });

  if (window.innerWidth < 576) {
    if (carritoSidebar) {
      carritoSidebar.style.width = "100%";
      carritoSidebar.style.right = "-100%";
    }
  }
});
