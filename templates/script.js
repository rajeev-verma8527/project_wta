window.addEventListener("load", (ev) => {
  let data = {
    loadTime: Math.round(performance.now()), //time after window load
    unixSeconds: Date.now() / 1000, //time
    referer: document.referrer, //previous page
    page: window.location.href, // current page
  };

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

  for (form of document.querySelectorAll("[tracking-name]")) {
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      let d = {
        unixSeconds: Date.now() / 1000,
        page: window.location.href,
        name: ev.target.getAttribute("tracking-name"),
      };
      fetch("{{url_for('form_data',_external=True)}}", {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(d),
      }).then(() => {
        ev.target.submit();
      });
    });
  }
});
