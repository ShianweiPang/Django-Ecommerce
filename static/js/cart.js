var updateButtons = document.getElementsByClassName("update-cart")
var cartTotalNav = document.getElementById("cart-totalnav")
var cartTotalItem = document.getElementById("cart-totalItem")
var cartTotalPrice = document.getElementById("cart-totalPrice")

var url = '/update_item/'


for (const updateButton of updateButtons) {
    updateButton.addEventListener("click", function () {
        var productId = this.getAttribute("data-product")
        var action = this.getAttribute("data-action")
        console.log('productId', productId, 'Action', action)
        console.log('User', user)

        if (user == "AnonymousUser") {
            addCookieItem(productId, action)
        } else {
            UpdateUserItem(this, productId, action)
        }
    })
}


// For non-login user
function addCookieItem(productId, action) {
    console.log("Not logged in")
    if (action == "add") {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        } else {
            cart[productId]['quantity'] += 1
        }
    }
    else if (action == "remove") {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            console.log("Remove item")
            delete cart[productId]
        }
    }
    console.log("Cart", cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

// function UpdateUserItem(productId, action) {
//     console.log("User logged in. Item to be added:", productId, "\nAction: ", action)

//     var url = '/update_item/'
//     var options = {
//         method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken, },
//         body: JSON.stringify({ 'productId': productId, 'action': action })
//     }

//     fetch(url, options = options)
//         .then((response) => response.json()) //return the promise
//         .then((data) => console.log('Data: ', data));

// }

// AJAX from W3schools
function UpdateUserItem(button, productId, action) {
    let xhr = new XMLHttpRequest();
    xhr.onload = function () {
        console.log("Perform success")
        let res_dict = JSON.parse(xhr.responseText)
        cartTotalNav.innerHTML = res_dict.cart_total
        // currently inefficient way of dealing with update in AJAX
        // TODO
        try {
            cartTotalItem.innerHTML = "Items: " + res_dict.cart_total
            cartTotalPrice.innerHTML = "$ " + (res_dict.cart_totalPrice).toFixed(2)
            button.parentElement.parentElement.children[0].innerHTML = res_dict.quantity
            button.parentElement.parentElement.parentElement.children[4].innerHTML = (res_dict.quantity * res_dict.unitprice).toFixed(2)
        } catch (error) {
            console.log("Catch", error)
        }

        if (res_dict.quantity == 0) {
            location.reload()
        }

    }
    xhr.open("POST", url)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.send(JSON.stringify({ 'productId': productId, 'action': action }))
}

