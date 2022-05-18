
let data = {
  referer: document.referrer, //previous page
  page: window.location.href, // current page
  unixSeconds: Date.now() / 1000, //time
};

function form_submit(name){
  submit_data = {
      time: Date.now() / 1000,
      domain : window.origin,
      name: name,
  }
  fetch("{{url_for('form_data',_external=True)}}", {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

}



window.addEventListener("load", (ev) => {
  data.loadTime = Math.round(performance.now()); //time after window load
  
  fetch("https://api.db-ip.com/v2/free/self") // ip and location data
    .then((r) => r.json())
    .then((d) => {
      data.ipAddress = d.ipAddress;
      data.city = d.city;
      data.state = d.stateProv;
      data.country = d.countryName;
      data.countryCode = d.countryCode;
    })
    .then(() => {
      // sending data to server
      fetch("{{url_for('data',_external=True)}}", {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
    });
});
