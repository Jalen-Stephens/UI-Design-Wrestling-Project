console.log("positions.js loaded");
let lessons = {};
let currentLesson = 0;

function loadLesson(index) {
  const lesson = lessons[index];
  if (!lesson) return;

  document.getElementById("section-title").textContent = lesson.Section;
  document.getElementById("title").textContent = lesson.title;
  document.getElementById("main-text").textContent = lesson["main-text"];

  const subTextEl = document.getElementById("sub-text");
  subTextEl.innerHTML = "";
  lesson["sub-text"].forEach(text => {
    const li = document.createElement("li");
    li.textContent = text;
    subTextEl.appendChild(li);
  });

  document.getElementById("lesson-img").src = lesson.image;
  console.log("Image source:", lesson.image);
}

function nextLesson() {
  currentLesson = (currentLesson + 1) % Object.keys(lessons).length;
  loadLesson(currentLesson);
}

function prevLesson() {
  currentLesson = (currentLesson - 1 + Object.keys(lessons).length) % Object.keys(lessons).length;
  loadLesson(currentLesson);
}

window.onload = () => {
  fetch("/api/positions")
    .then(res => res.json())
    .then(data => {
      lessons = data;
      loadLesson(currentLesson);
    })
    .catch(err => console.error("Failed to load lessons:", err));
};

console.log("positions.js loaded Bottom");
