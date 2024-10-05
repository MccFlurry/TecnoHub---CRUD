document.addEventListener('DOMContentLoaded', function () {
    // Obtener los productos del carrito desde localStorage
    function obtenerCarrito() {
        let carrito = localStorage.getItem('carrito');
        return carrito ? JSON.parse(carrito) : [];
    }

    // Calcular y actualizar el resumen de la compra
    function actualizarResumenCompra() {
        let carrito = obtenerCarrito();
        let subtotal = 0;

        carrito.forEach(producto => {
            subtotal += producto.precio * producto.cantidad;
        });

        document.getElementById('subtotal').textContent = `S/${subtotal.toFixed(2)}`;
        let envio = 5; // Costo de envío fijo
        document.getElementById('envio').textContent = `S/${envio.toFixed(2)}`;
        let total = subtotal + envio;
        document.getElementById('total').textContent = `S/${total.toFixed(2)}`;
    }

    actualizarResumenCompra();

    // Manejar el cambio de método de pago
    document.querySelectorAll('input[name="paymentMethod"]').forEach(input => {
        input.addEventListener('change', function () {
            let cardDetails = document.getElementById('cardDetails');
            if (this.value === 'debit' || this.value === 'credit') {
                cardDetails.style.display = 'block';
            } else {
                cardDetails.style.display = 'none';
            }
        });
    });

    // Guardar la nueva tarjeta
    document.getElementById('saveCard').addEventListener('click', function () {
        let cardNumber = document.getElementById('cardNumber').value;
        let cardName = document.getElementById('cardName').value;
        let cardExpiry = document.getElementById('cardExpiry').value;
        let cardCVC = document.getElementById('cardCVC').value;

        if (cardNumber && cardName && cardExpiry && cardCVC) {
            // Guardar la tarjeta en localStorage (o en una base de datos en un caso real)
            let savedCards = JSON.parse(localStorage.getItem('savedCards')) || [];
            savedCards.push({ number: cardNumber, name: cardName, expiry: cardExpiry, cvc: cardCVC });
            localStorage.setItem('savedCards', JSON.stringify(savedCards));

            // Mostrar la tarjeta guardada en la lista
            let savedCardContainer = document.getElementById('savedCardContainer');
            savedCardContainer.innerHTML += `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="paymentMethod" value="saved">
                    <label class="form-check-label">
                        ${cardName} ****${cardNumber.slice(-4)}
                    </label>
                </div>
            `;
            savedCardContainer.style.display = 'block';

            // Limpiar los campos
            document.getElementById('cardNumber').value = '';
            document.getElementById('cardName').value = '';
            document.getElementById('cardExpiry').value = '';
            document.getElementById('cardCVC').value = '';
            document.getElementById('cardDetails').style.display = 'none';
        } else {
            alert('Por favor, completa todos los campos de la tarjeta.');
        }
    });

    // Manejar el envío del formulario de pago
    document.getElementById('paymentForm').addEventListener('submit', function (event) {
        event.preventDefault();

        let selectedMethod = document.querySelector('input[name="paymentMethod"]:checked');
        if (!selectedMethod) {
            alert('Por favor, selecciona un método de pago.');
            return;
        }

        // Borrar los productos del carrito
        localStorage.removeItem('carrito');

        // Mostrar mensaje de confirmación
        let confirmationMessage = document.getElementById('confirmationMessage');
        confirmationMessage.innerHTML = '<i class="fa fa-check-circle"></i><p>Pago confirmado. ¡Gracias por tu compra!</p><img src="img/pago.jpg" alt="" class="img-fluid">';
        confirmationMessage.style.display = 'block';

        // Ocultar secciones de pago y resumen
        document.getElementById('paymentSection').style.display = 'none';
        document.getElementById('summarySection').style.display = 'none';

        setTimeout(function() {
            window.location.href = 'index.html';
        }, 5000);
    });

    // Simulación de tarjeta guardada
    let hasSavedCard = true;
    if (hasSavedCard) {
        document.getElementById('savedCardContainer').style.display = 'block';
    }
});
