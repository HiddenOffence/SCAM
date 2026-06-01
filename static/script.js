function updateProgress(){

let totalQuestions = 30;

let answered = document.querySelectorAll("input[type=radio]:checked").length;

let percentage = (answered/totalQuestions)*100;

let bar = document.getElementById("progress-bar");

bar.style.width = percentage + "%";

}