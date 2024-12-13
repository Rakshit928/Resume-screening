document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("resume-form");
    const loadingDiv = document.getElementById("loading");
    const responseDiv = document.getElementById("response");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Show loading spinner
        loadingDiv.style.display = "block";
        responseDiv.innerHTML = ""; // Clear previous response

        const formData = new FormData(form);
        try {
            const response = await fetch("/evaluate", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            loadingDiv.style.display = "none";

            if (result.error) {
                responseDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
            } else {
                responseDiv.innerHTML = `<pre>${result.response}</pre>`;
            }
        } catch (err) {
            loadingDiv.style.display = "none";
            responseDiv.innerHTML = `<p style="color: red;">An error occurred: ${err.message}</p>`;
        }
    });
});
