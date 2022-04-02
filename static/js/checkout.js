var form = document.getElementById('form')
var button = document.getElementById('make-payment')
csrftoken = form.getElementsByTagName("input")[0].value

console.log("New token", csrftoken)

function submitFormData() {
    console.log("Payment Button Clicked")

    var userFormData = {
        'name': null,
        'email': null,
        'total': totalPrice,
    }

    var shippingInfo = {
        'address': null,
        'city': null,
        'state': null,
        'zipcode': null,
    }

    if (shipping != 'False') {
        shippingInfo.address = form.address.value
        shippingInfo.city = form.city.value
        shippingInfo.state = form.state.value
        shippingInfo.zipcode = form.zipcode.value
    }

    if (user == "AnonymousUser") {
        userFormData.name = form.name.value
        userFormData.email = form.email.value
    }// problem here 

    var url = '/process_order/'


    const xhr = new XMLHttpRequest();
    xhr.onload = function () {
        console.log("Process order successfully..")
        alert("Processing your order..")
        cart = {}
        // clear cookies after successfully process order
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        window.location.href = storeURL
    }
    xhr.open("POST", url)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.send(JSON.stringify({ 'userFormData': userFormData, 'shippingInfo': shippingInfo }))


}

if (user != "AnonymousUser")
    document.getElementById("user-info").innerHTML = ""
// console.log(shipping)
if (shipping == 'False') {
    document.getElementById("form-wrapper").style.display = "none"
    document.getElementById('payment-info').classList.remove("hidden")
    if (quantity == 0) {
        document.getElementById("form-wrapper").style.display = "none"
        document.getElementById('payment-info').classList.add("hidden")
    }
}

form.addEventListener('submit', function (event) {
    // stop form submission
    event.preventDefault()
    console.log('Form Submitted...')
    document.getElementById("form-button").classList.add("hidden")
    document.getElementById('payment-info').classList.remove("hidden")
})


