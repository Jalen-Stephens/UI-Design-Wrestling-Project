$(document).ready(function () {
    let currentLessonId = lesson.id; // Use the lesson ID passed from the server
    let lesson_expanded = lesson["expanded-text"]; // Use the lesson expanded text passed from the server
    let isExpanded = false; // Track the state of the button

    // Function to toggle the image and text
    $("#expand").click(function () {
        if (!isExpanded) {
            // Replace the image with expanded text
            const expandedText = `
                <ul id="expanded-text">
                    ${lesson_expanded.map(text => `<li>${text}</li>`).join("")}
                </ul>`;
            $("#lesson-img").hide(); // Hide the image
            $(".image-box").append(expandedText); // Add the expanded text
            $(this).text("Show Image"); // Update button text
        } else {
            // Restore the image and remove the expanded text
            $("#lesson-img").show(); // Show the image
            $("#expanded-text").remove(); // Remove the expanded text
            $(this).text("Learn More"); // Reset button text
        }
        isExpanded = !isExpanded; // Toggle the state
    });

    // Function to load the next lesson
    function nextLesson() {
        currentLessonId = (currentLessonId + 1) % Object.keys(lessons).length;
        loadLesson(currentLessonId);
    }

    // Function to load the previous lesson
    function prevLesson() {
        currentLessonId = (currentLessonId - 1 + Object.keys(lessons).length) % Object.keys(lessons).length;
        loadLesson(currentLessonId);
    }
});