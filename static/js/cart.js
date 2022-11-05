const allbtn = document.getElementsByClassName("update-btn")

for (let item of allbtn){
	item.addEventListener("click" , function() {
		if (user == "AnonymousUser"){
			console.log("log in");
		}else{
			const productId = this.dataset.productid
			const action = this.dataset.action
			updateCart(productId , action)
		}
	})
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
