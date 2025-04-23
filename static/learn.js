document.addEventListener("DOMContentLoaded", () => {
    const startTime = Date.now();

    const imageBox = document.getElementById("lesson-img");
    const imageBoxContainer = document.querySelector(".image-box");

    const createExpandButton = () => {
        const expandButton = document.createElement("button");
        expandButton.id = "expand";
        expandButton.className = "btn btn-primary";
        expandButton.textContent = "Learn More";

        expandButton.addEventListener("click", () => {
            imageBox.style.display = "none";

            const expandedText = document.createElement("p");
            expandedText.innerHTML = lesson["expanded-text"];
            expandedText.id = "expanded-text";
            imageBoxContainer.appendChild(expandedText);

            const showImageBtn = document.createElement("button");
            showImageBtn.textContent = "Show Image";
            showImageBtn.className = "btn btn-secondary mt-2";
            showImageBtn.id = "show-image-btn";

            showImageBtn.addEventListener("click", () => {
                expandedText.remove();
                imageBox.style.display = "block";
                showImageBtn.remove();

                // Re-add Learn More
                createExpandButton();
            });

            imageBoxContainer.appendChild(showImageBtn);
            expandButton.remove(); // Remove original expand
        });

        imageBoxContainer.insertBefore(expandButton, imageBox);
    };

    // Only create if expanded text exists
    if (lesson["expanded-text"]) {
        createExpandButton();
    }

    // SEND BEACON WHEN PAGE IS UNLOADED
    window.addEventListener("beforeunload", () => {
        const timeSpent = Math.round((Date.now() - startTime) / 1000);

        const payload = JSON.stringify({
            lesson_id: typeof lesson_id !== 'undefined' ? lesson_id : -1,
            time_spent: timeSpent
        });

        navigator.sendBeacon("/log-time", payload);
    });
});
