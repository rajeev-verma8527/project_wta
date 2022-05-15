data = {
    "referer" : document.referrer,
    "location" : window.location.href
}

window.addEventListener("load",(ev)=>{

    data["time"] = performance.now()

    fetch("http://127.0.0.1:5000/post",{
        method:"POST",
        mode: 'cors',
        headers: {
            "Content-Type" : "application/json",
          },
        body: JSON.stringify(data)
    })
    // let req = new XMLHttpRequest()
    // req.open("POST", "http://127.0.0.1:5000/post")
    // req.setRequestHeader("Content-Type", "application/json");
    // req.send(JSON.stringify(data))

})