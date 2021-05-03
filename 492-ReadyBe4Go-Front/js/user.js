async function userInfo() {
    let url = `http://492readybe4go-env.eba-bt2jpjzi.eu-central-1.elasticbeanstalk.com/user`;
    let response = await fetch(url, {
        credentials: 'include'
    });
    let data = await response.json();
    console.log(data)
}

userInfo();