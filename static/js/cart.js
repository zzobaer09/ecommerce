const allbtn = document.getElementsByClassName("update-btn")

for (let item of allbtn){
	item.addEventListener("click" , function() {
		if (user == "AnonymousUser"){
			addCookieItem(1,2)
		}else{
			const productId = this.dataset.productid
			const action = this.dataset.action
			updateCart(productId , action)
		}
	})
}

 
function addCookieItem(productId , action) {
	console.log("you are not loged in");
	console.log("USER:" , user);
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
