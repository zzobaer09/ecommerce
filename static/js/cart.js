const allbtn = document.getElementsByClassName("update-btn")

for (let item of allbtn){
	item.addEventListener("click" , function() {
		const productId = this.dataset.productid
		const action = this.dataset.action
		if (user == "AnonymousUser"){
			addCookieItem(productId , action)
		}else{
			updateCart(productId , action)
		}
	})
}

 
function addCookieItem(productId , action) {
	if(action == "add"){
		if (cart[productId]==undefined){
			cart[productId] = {"quantity":1}
		}else{
			cart[productId]["quantity"]+=1
		}
	}
	if(action=="remove"){
		cart[productId] -= 1
		if (cart[productId]<=0){
			delete cart[productId]
		}
	}
    document.cookie = "cart=" + JSON.stringify(cart)+ ";domain=;path=/"
	location.reload()
}


function updateCart(productId , action) {
	console.log("sending data")
	const url = "/update_store/"
	fetch(url , {
		method: 'POST',
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken,
		},
		body:JSON.stringify({'productId':productId, 'action':action})
	})
	.then((request)=>{
		return request.json()
	})
	.then((data)=>{
		console.log(data);
		location.reload()
	})
}
