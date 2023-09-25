var updatedBtns = document.getElementsByClassName('update-cart')

for(i=0; i< updatedBtns.length; i++){
    updatedBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productId, 'action:', action)

        console.log('USER: ', user)
        if(user === 'AnonymousUser'){
            console.log('Not authenticated')
        }else{
           updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action){
    console.log('User is logged in, Sending data...')

    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({'productId': productId, 'action:': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data: ', data)
    })
}