document.getElementById('upload-btn').addEventListener('click', async function() {
    const form = document.getElementById('upload-form');
    const formData = new FormData(form);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();

        const reviewList = document.getElementById('cv-review-list');
        reviewList.innerHTML = '';  // Clear any existing review points

        // Render all review points as a single block of text
        data.review.forEach(point => {
            const p = document.createElement('p');
            // Remove unnecessary characters and make keywords bold
            p.innerHTML = point.replace(/\*+/g, '').replace(/(Strengths|Weaknesses|Areas for improvement)/gi, '<strong>$1</strong>');
            reviewList.appendChild(p);
        });

        document.getElementById('results-container').style.display = 'block';
    } else {
        console.error('Error uploading file');
    }
});

document.getElementById('optimize-btn').addEventListener('click', async function() {
    const resumeText = document.getElementById('cv-review-list').textContent;

    const response = await fetch('/optimize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ 'resume_text': resumeText })
    });

    if (response.ok) {
        const data = await response.json();

        const tipsList = document.getElementById('tips-list');
        tipsList.innerHTML = '';  // Clear any existing tips

        // Render optimization tips as paragraphs with bolded keywords
        data.tips.forEach(tip => {
            const p = document.createElement('p');
            p.innerHTML = tip.replace(/\*+/g, '').replace(/(Strengths|Weaknesses|Areas for improvement)/gi, '<strong>$1</strong>');
            tipsList.appendChild(p);
        });

        document.getElementById('optimization-tips').style.display = 'block';
    } else {
        console.error('Error fetching optimization tips');
    }
});

document.getElementById('reset-btn').addEventListener('click', function() {
    window.location.reload();  // Reload the page to reset the application
});
