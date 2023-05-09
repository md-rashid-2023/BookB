function add_item(ele){
    let id = ele.getAttribute('book');

   fetch(cart_url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'pk_book':id}) //JavaScript object of data to POST
    })
    .then(response => {
            return response.json() //Convert response to JSON
    })
    .then(data => {
        console.log(data)
        if (data.message=='success') {
            ele.innerHTML='Added To Cart';
            ele.style.background="yellow";
            ele.style.color="black";
            ele.setAttribute('disabled','true')
            ele.style.cursor="not-allowed";

            document.getElementById('temp-cart-count').innerText = data.total_cart;
        }
    })


}