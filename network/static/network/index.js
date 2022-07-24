document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views

    document.querySelector('#submit').addEventListener('click', () => create_post());
    let currentUser = document.querySelector('#my_profile').innerText
    let links = document.getElementsByClassName('postMaker')
    Array.from(links).forEach(element => {
        if (element.innerText == currentUser){
            element.innerText = "Me"
            element.href="personal_profile"
        }
        //element.addEventListener('click', () => user_profile(element.innerText))
        });

    let likes = document.getElementsByClassName('btn btn-success')
    Array.from(likes).forEach(element => {
        element.addEventListener('click', () => like_button(element.id))
        });

    feed_page()
});

function feed_page() {

    // Show compose view and hide other views
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#post-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';


    document.querySelector('#compose-body').value = '';
}

function create_post() {

    fetch('post', {
            method: 'POST',
            body: JSON.stringify({
                body: document.querySelector('#compose-body').value
            })
        })
        .then(response => response.json())
        .then(result => {
                console.log("done")
        });

}

// needs to take in user id and fill in correct info
function user_profile(name) {
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#post-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'block';

    let cardTitle = document.querySelector('#username')
    let cardBio = document.querySelector('#userBio')
    let followers = document.querySelector('#profile_followers')
    let following = document.querySelector('#profile_following')

    console.log(name)

    fetch(`profile/${name}`)
        .then(response => response.json())
        .then(data => {
            cardTitle.innerText = data.username
            cardBio.innerText =  data.user_bio
            followers.innerText = data.follower_count
            following.innerText = data.following_count
            console.log(data)
        });
}

function like_button(id) {

fetch(`likes/${id}`)
        .then(response => response.json())
        .then(data => {
        console.log(id)
        console.log(data)
            console.log(data)
            let button = document.getElementById(id)
            button.innerText = `${data.title}:${data.like_count}`

        });

}

function button_display(id, data) {




}