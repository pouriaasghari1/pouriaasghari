// =====================
// cart.js - kode sabad kharid
// =====================

var cart = JSON.parse(localStorage.getItem("pGames_cart")) || [];

// update badge
function upbadge() {
    var t = 0;
    for (var i = 0; i < cart.length; i++) {
        t += cart[i].qty;
    }
    var b = document.getElementById("cartBadge");
    if (b) b.textContent = t;
}

// add to cart
function addToCart(btn) {
    var item = btn.closest(".menu-item");
    if (!item) return;

    var id = item.getAttribute("data-id");
    var title = item.getAttribute("data-title");
    var price = parseInt(item.getAttribute("data-price"));
    var image = item.getAttribute("data-image");

    var found = false;
    for (var i = 0; i < cart.length; i++) {
        if (cart[i].id === id) {
            cart[i].qty += 1;
            found = true;
            break;
        }
    }
    if (!found) {
        cart.push({
            id: id,
            title: title,
            price: price,
            image: image,
            qty: 1
        });
    }

    localStorage.setItem("pGames_cart", JSON.stringify(cart));
    upbadge();
    window.location.href = "cart.html";
}

// render cart
function rendercart() {
    var emptyDiv = document.getElementById("cartEmpty");
    var itemsDiv = document.getElementById("cartItems");
    var totalSpan = document.getElementById("cartTotal");

    if (cart.length === 0) {
        if (emptyDiv) emptyDiv.style.display = "block";
        if (itemsDiv) itemsDiv.style.display = "none";
        return;
    }

    if (emptyDiv) emptyDiv.style.display = "none";
    if (itemsDiv) itemsDiv.style.display = "block";

    var html = "";
    var total = 0;
    for (var i = 0; i < cart.length; i++) {
        var item = cart[i];
        var itemTotal = item.price * item.qty;
        total += itemTotal;

        html += '<div class="cart-item">';
        html += '<img src="' + item.image + '" style="width:70px; height:70px; object-fit:cover; border-radius:8px;" alt="' + item.title + '">';
        html += '<div style="flex:1;">';
        html += '<h4>' + item.title + '</h4>';
        html += '<p>' + formatprice(item.price) + ' تومان</p>';
        html += '<div style="display:flex; gap:10px; align-items:center;">';
        html += '<button onclick="changeQty(\'' + item.id + '\', -1)" style="background:#8a2be2; color:#fff; border:none; border-radius:5px; padding:5px 10px;">-</button>';
        html += '<span>' + item.qty + '</span>';
        html += '<button onclick="changeQty(\'' + item.id + '\', 1)" style="background:#8a2be2; color:#fff; border:none; border-radius:5px; padding:5px 10px;">+</button>';
        html += '</div>';
        html += '</div>';
        html += '<button onclick="removeFromCart(\'' + item.id + '\')" class="btn-remove"><i class="fas fa-trash"></i></button>';
        html += '</div>';
    }

    itemsDiv.innerHTML = html;
    if (totalSpan) totalSpan.textContent = formatprice(total) + " تومان";
}

function changeQty(id, delta) {
    for (var i = 0; i < cart.length; i++) {
        if (cart[i].id === id) {
            cart[i].qty += delta;
            if (cart[i].qty <= 0) {
                cart.splice(i, 1);
            }
            break;
        }
    }
    localStorage.setItem("pGames_cart", JSON.stringify(cart));
    upbadge();
    rendercart();
}

function removeFromCart(id) {
    cart = cart.filter(function(item) { return item.id !== id; });
    localStorage.setItem("pGames_cart", JSON.stringify(cart));
    upbadge();
    rendercart();
}

function formatprice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// ========== فرم ثبت‌نام ==========
function setregform() {
    var form = document.getElementById("registerForm");
    if (!form) return;

    form.addEventListener("submit", function(e) {
        e.preventDefault();

        document.getElementById("firstNameError").textContent = "";
        document.getElementById("lastNameError").textContent = "";
        document.getElementById("phoneError").textContent = "";
var fn = document.getElementById("firstName").value.trim();
        var ln = document.getElementById("lastName").value.trim();
        var ph = document.getElementById("phone").value.trim();
        var ok = true;

        if (fn.length < 2) {
            document.getElementById("firstNameError").textContent = "نام حداقل ۲ حرف باشه";
            ok = false;
        }
        if (ln.length < 2) {
            document.getElementById("lastNameError").textContent = "نام خانوادگی حداقل ۲ حرف باشه";
            ok = false;
        }
        if (!/^09\d{9}$/.test(ph)) {
            document.getElementById("phoneError").textContent = "شماره اشتباهه (مثل 09123456789)";
            ok = false;
        }
        if (!ok) return;

        var formData = new FormData(form);
        fetch("hoop.php", {
            method: "POST",
            body: formData
        })
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (data.success) {
                document.getElementById("registerForm").style.display = "none";
                document.getElementById("successMessage").style.display = "block";
            } else {
                if (data.errors) {
                    if (data.errors.first_name) document.getElementById("firstNameError").textContent = data.errors.first_name;
                    if (data.errors.last_name) document.getElementById("lastNameError").textContent = data.errors.last_name;
                    if (data.errors.phone) document.getElementById("phoneError").textContent = data.errors.phone;
                }
                alert(data.message || "خطا");
            }
        })
        .catch(function() {
            alert("ارتباط با سرور قطع شد");
        });
    });
}

// ========== باکس ارتباط با ما ==========
function toggleContact() {
    var popup = document.getElementById("contactPopup");
    if (popup) popup.classList.toggle("show");
}

// کلیک خارج باکس بسته بشه
document.addEventListener("click", function(e) {
    var contactBtn = document.getElementById("contactBtn");
    var popup = document.getElementById("contactPopup");
    if (!contactBtn || !popup) return;
    if (!contactBtn.contains(e.target)) {
        popup.classList.remove("show");
    }
});

document.getElementById("contactBtn").addEventListener("click", toggleContact);

// ========== شروع ==========
document.addEventListener("DOMContentLoaded", function() {
    upbadge();
    if (document.getElementById("cartItems")) {
        rendercart();
    }
    if (document.getElementById("registerForm")) {
        setregform();
    }
});