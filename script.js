const webhookUrl = "https://mrantidata.app.n8n.cloud/webhook-test/contact-form";

fetch(webhookUrl, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value
    })
})
.then(res => res.json())
.then(data => {
    alert("Submitted successfully!");
})
.catch(err => {
    console.error(err);
});
