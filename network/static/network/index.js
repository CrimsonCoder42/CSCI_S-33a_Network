document.addEventListener('DOMContentLoaded', function () {

 const elem = document.getElementById('submit');


elem.addEventListener('click', make_post)
});


function make_post() {
document.body.style.backgroundColor = "red";
//    fetch('/post', {
//            method: 'POST',
//            body: JSON.stringify({
//                body: document.querySelector('#compose-body').value
//            })
//        })
//        .then(response => response.json())
//        .then(result => {
//           console.log("result", result)
//        });

}