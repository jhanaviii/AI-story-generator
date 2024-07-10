document.getElementById('story-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const prompt = document.getElementById('prompt').value;
    const useLm1b = document.getElementById('use-lm1b').checked;

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt, use_lm1b: useLm1b })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('story-output').innerText = data.story;
    })
    .catch(error => console.error('Error:', error));
});

document.addEventListener('DOMContentLoaded', function() {
    var coll = document.getElementsByClassName("collapsible");
    for (var i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
});
