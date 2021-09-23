function update_like(id) {
    fetch(`/like/${id}`, {
        method: 'GET',
        credentials: 'same-origin',
        headers : { 
            "X-CSRFToken": getCookie("csrftoken")
           }
    })
    .then(response => { return response.json() }
)
    .then( data => {
        bum = document.querySelector(`#likes${id}`)
        console.log(bum)
        console.log("this is the data" + data)
        console.log("as above" + data["likescount"]["total_likes"])
        if (data["likescount"]["total_likes"] === null) {
            
            bum.innerHTML = `${0}`
        } else
         {   console.log("fired")  
             bum.innerHTML = data["likescount"]["total_likes"] 
           
          }
    
})}



document.addEventListener('DOMContentLoaded', function() { //when page has loaded do the following

    // Use buttons to toggle between views
    let formElements = document.getElementsByName("formo");
    
    console.log(formElements)

    for (let i = 0, max = formElements.length; i < max; i++) {
        formElements[i].style.display = "none";
    }
    });
   

    document.addEventListener('DOMContentLoaded', function () {

        document.querySelectorAll('.fa-heart').forEach(div => {
            console.log(div.id)
        
            let likeId = div.id.slice(18, div.id.length)
    
            div.onclick = function () {

                update_like(likeId)
                
if (document.querySelector(`#authenticatedheart${likeId}`)?.style.color == 'pink') {
    document.querySelector(`#authenticatedheart${likeId}`).style.color = 'grey'
  } else {
  document.querySelector(`#authenticatedheart${likeId}`).style.color = 'pink' }
            };
        })});
// select all edit buttons 
function show_edit(post_id) {
    let postId = post_id.slice(4, post_id.length)
     
    document.querySelector(`.tweeto_${postId}`).style.color = 'coral'
    document.querySelector(`.edit-form_${postId}`).style.display = 'block'
    document.querySelector(`#edit${postId}`).style.display = 'none'

    
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;} 
