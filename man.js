
document.addEventListener("DOMContentLoaded", () => {
    syncCartBadge();
    initArchiveFilters();
});

function getCart() {
    return JSON.parse(localStorage.getItem("boutique_v4_cart")) || [];
}

function syncCartBadge() {
    const badge = document.querySelector(".cart-badge");
    if (!badge) return;
    const cart = getCart();
    badge.textContent = cart.reduce((sum, item) => sum + item.qty, 0);
}

function addToCart(id, name, price, img, color) {
    let cart = getCart();
    let existing = cart.find(item => item.id === id);
    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ id, name, price, img, qty: 1, color });
    }
    localStorage.setItem("boutique_v4_cart", JSON.stringify(cart));
    syncCartBadge();
    alert(`محصول "${name}" با موفقیت اضافه شد.`);
}

function initArchiveFilters() {
    const checkboxes = document.querySelectorAll(".filter-sidebar input[type='checkbox']");
    const cards = document.querySelectorAll(".archive-content .product-card");
    if(cards.length === 0) return;

    checkboxes.forEach(box => {
        box.addEventListener("change", () => {
            let activeCats = Array.from(document.querySelectorAll("input[data-filter='cat']:checked")).map(b => b.value);
            cards.forEach(card => {
                let cardCat = card.getAttribute("data-category");
                if(activeCats.length === 0 || activeCats.includes(cardCat)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
}

function renderCartTable() {
    const tbody = document.getElementById("cart-tbody");
    const totalAmountEl = document.getElementById("cart-total-amount");
    if(!tbody) return;

    let cart = getCart();
    if(cart.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding:50px; color:var(--text-muted);">سبد سفارشات شما خالی است.</td></tr>`;
        if(totalAmountEl) totalAmountEl.textContent = "۰";
        return;
    }

    let html = "";
    let total = 0;
    cart.forEach((item) => {
        let rowTotal = item.price * item.qty;
        total += rowTotal;
        html += `
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                <td style="padding:18px 0; display:flex; align-items:center; gap:15px;">
                    <img src="${item.img}" style="width:60px; height:60px; object-fit:cover; border-radius:12px;">
                    <div><strong>${item.name}</strong></div>
                </td>
                <td style="padding:18px 0;">${item.price.toLocaleString()} تومان</td>
                <td style="padding:18px 0;">${item.qty} عدد</td>
                <td style="padding:18px 0; color:${item.color}; font-weight:700;">${rowTotal.toLocaleString()} تومان</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
    if(totalAmountEl) totalAmountEl.textContent = total.toLocaleString() + " تومان";
}

function clearCart() {
    localStorage.removeItem("boutique_v4_cart");
    renderCartTable();
    syncCartBadge();
}
