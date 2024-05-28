document.addEventListener('DOMContentLoaded', () => {
    const cart = [];
    const products = document.querySelectorAll('.product');
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalContainer = document.getElementById('cart-total');
    const checkoutButton = document.getElementById('checkout-button');

    products.forEach(product => {
        product.querySelector('.add-to-cart').addEventListener('click', () => {
            const id = product.getAttribute('data-id');
            const name = product.getAttribute('data-name');
            const basePrice = parseFloat(product.getAttribute('data-price'));

            const addOns = Array.from(product.querySelectorAll('.addon:checked')).map(addon => {
                return {
                    name: addon.getAttribute('data-addon-name'),
                    price: parseFloat(addon.getAttribute('data-addon-price'))
                };
            });

            const choices = Array.from(product.querySelectorAll('.choice:checked')).map(choice => {
                return {
                    name: choice.getAttribute('data-choice-name'),
                    price: parseFloat(choice.getAttribute('data-choice-price'))
                };
            });

            addToCart({ id, name, basePrice, addOns, choices });
        });
    });

    function addToCart(product) {
        const existingProductIndex = cart.findIndex(item => 
            item.id === product.id && 
            JSON.stringify(item.addOns) === JSON.stringify(product.addOns) &&
            JSON.stringify(item.choices) === JSON.stringify(product.choices)
        );

        if (existingProductIndex > -1) {
            cart[existingProductIndex].quantity += 1;
        } else {
            cart.push({ ...product, quantity: 1 });
        }
        renderCart();
    }

    function renderCart() {
        cartItemsContainer.innerHTML = '';
        let total = 0;

        cart.forEach(item => {
            let itemTotal = item.basePrice;
            let addOnsText = '';
            item.addOns.forEach(addon => {
                itemTotal += addon.price;
                addOnsText += `, ${addon.name} (+$${addon.price.toFixed(2)})`;
            });
            let choicesText = '';
            item.choices.forEach(choice => {
                itemTotal += choice.price;
                choicesText += `, ${choice.name} (+$${choice.price.toFixed(2)})`;
            });
            total += itemTotal * item.quantity;

            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
                <span>${item.name} - $${item.basePrice.toFixed(2)}${addOnsText}${choicesText} x ${item.quantity}</span>
                <button class="remove-from-cart" data-id="${item.id}" data-addons='${JSON.stringify(item.addOns)}' data-choices='${JSON.stringify(item.choices)}'>Remove</button>
            `;
            cartItemsContainer.appendChild(cartItem);
        });

        cartTotalContainer.textContent = total.toFixed(2);
        attachRemoveButtons();
    }

    function attachRemoveButtons() {
        const removeButtons = document.querySelectorAll('.remove-from-cart');
        removeButtons.forEach(button => {
            button.addEventListener('click', () => {
                const id = button.getAttribute('data-id');
                const addOns = JSON.parse(button.getAttribute('data-addons'));
                const choices = JSON.parse(button.getAttribute('data-choices'));
                removeFromCart(id, addOns, choices);
            });
        });
    }

    function removeFromCart(id, addOns, choices) {
        const productIndex = cart.findIndex(item => 
            item.id === id && 
            JSON.stringify(item.addOns) === JSON.stringify(addOns) &&
            JSON.stringify(item.choices) === JSON.stringify(choices)
        );

        if (productIndex > -1) {
            cart[productIndex].quantity -= 1;
            if (cart[productIndex].quantity === 0) {
                cart.splice(productIndex, 1);
            }
        }
        renderCart();
    }

    checkoutButton.addEventListener('click', () => {
        localStorage.setItem('cart', JSON.stringify(cart));
        window.location.href = 'checkout';
    });
});
