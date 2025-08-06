async function generateEmail() {
    const prompt = document.getElementById("prompt").value;

    fetch("/generate-email/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("emailBody").value = data.email;
    });
}




 async function sendEmail() {
    const recipients = document.getElementById("recipients").value;
    const emailBody = document.getElementById("emailBody").value;

    fetch('/send-email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            recipients: recipients,
            email: emailBody
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

