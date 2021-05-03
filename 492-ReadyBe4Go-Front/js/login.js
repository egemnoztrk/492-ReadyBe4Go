async function login() {
    var email = document.getElementById("email").value
    var password = document.getElementById("password").value
    let url = `http://492readybe4go-env.eba-bt2jpjzi.eu-central-1.elasticbeanstalk.com/login?password=${password}&email=${email}`;
    let response = await fetch(url, {
        credentials: 'include'
    });
    let data = await response.json()
    console.log(data)
    if(data=="Restaurant"){
        window.location.replace("/restaurant.html");
    }
    else if(data=="User"){
        window.location.replace("/user.html");
    }
}