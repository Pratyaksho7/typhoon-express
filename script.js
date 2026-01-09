async function checkNews() {
    const headline = document.getElementById("headline").value;
    const imageInput = document.getElementById("image");
    const output = document.getElementById("output");

    if (!headline.trim()) {
        output.innerHTML = "<p style='color:red;'>Please enter a headline.</p>";
        return;
    }

    output.innerHTML = "<p>Checking credibility...</p>";

    const formData = new FormData();
    formData.append("headline", headline);

    if (imageInput.files.length > 0) {
        formData.append("image", imageInput.files[0]);
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/check", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const color =
            data.credibility_score >= 0.7 ? "green" :
            data.credibility_score >= 0.4 ? "orange" :
            "red";

        output.innerHTML = `
            <div style="border:1px solid #ddd; padding:15px; border-radius:8px;">
                <h3 style="color:${color};">Verdict: ${data.verdict}</h3>
                <p><strong>Credibility Score:</strong> ${(data.credibility_score * 100).toFixed(0)}%</p>

                <progress value="${data.credibility_score}" max="1" style="width:100%;"></progress>

                <h4>Reasons</h4>
                <ul>
                    ${data.reasons.map(r => `<li>${r}</li>`).join("")}
                </ul>

                <small style="color:#666;">${data.disclaimer}</small>
            </div>
        `;
    } catch (error) {
        output.innerHTML = "<p style='color:red;'>Server error. Is FastAPI running?</p>";
        console.error(error);
    }
}
