document.addEventListener("DOMContentLoaded", () => {
    const startTime = Date.now();

    const imageBox = document.getElementById("lesson-img");
    const imageBoxContainer = document.querySelector(".image-box");

    const createExpandButton = () => {
        const expandButton = document.createElement("button");
        expandButton.id = "expand";
        expandButton.className = "btn btn-primary mt-3";
        expandButton.textContent = "Learn More";

        expandButton.addEventListener("click", () => {
            imageBox.style.display = "none";

            // Build a bullet list from expanded-text array
            const expandedList = document.createElement("ul");
            expandedList.id = "expanded-text";

            lesson["expanded-text"].forEach(sentence => {
                const li = document.createElement("li");
                li.textContent = sentence;
                expandedList.appendChild(li);
            });

            imageBoxContainer.appendChild(expandedList);

            // Button to show image again
            const showImageBtn = document.createElement("button");
            showImageBtn.textContent = "Show Image";
            showImageBtn.className = "btn btn-secondary mt-2";
            showImageBtn.id = "show-image-btn";

            showImageBtn.addEventListener("click", () => {
                expandedList.remove();
                imageBox.style.display = "block";
                showImageBtn.remove();

                // Re-add Learn More
                createExpandButton();
            });

            imageBoxContainer.appendChild(showImageBtn);
            expandButton.remove(); // Remove original Learn More button
        });

        // Insert the button below the image
        imageBoxContainer.appendChild(expandButton);
    };

    // Only create button if there's expanded text
    if (lesson["expanded-text"] && lesson["expanded-text"].length) {
        createExpandButton();
    }

    // SEND BEACON WHEN PAGE IS UNLOADED
    window.addEventListener("beforeunload", () => {
        const timeSpent = Math.round((Date.now() - startTime) / 1000);

        const payload = JSON.stringify({
            type: "lesson",
            id: lesson_id,
            time_spent: timeSpent
        });

        navigator.sendBeacon("/log-time", payload);
    });
});
