async function register() {
    var name = document.getElementById("name").value
    var email = document.getElementById("email").value
    var password = document.getElementById("password").value
    var accountType=document.getElementById("user-type").value
    let url = `http://492readybe4go-env.eba-bt2jpjzi.eu-central-1.elasticbeanstalk.com/register?name=${name}&accountType=${accountType}&password=${password}&email=${email}`;
    let response = await fetch(url, {
        credentials: 'include'
    });
    let data = await response.json()
    if(data==false || accountType=="User Type"){
        document.getElementById("top-text").innerHTML="TRY AGAIN"
    }
    else if(data==true){
        window.location.replace("/login.html");
    }
}