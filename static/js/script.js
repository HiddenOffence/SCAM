// ==========================================
// Quiz Answer Selection
// ==========================================
const options =
document.querySelectorAll(
".answer-option"
);

options.forEach(option => {

    option.addEventListener(
    "click",

    () => {

        options.forEach(o =>
            o.classList.remove(
                "selected"
            )
        );

        option.classList.add(
            "selected"
        );
    });

});

// ==========================================
// Results Chart
// ==========================================

const resultsChart =
    document.getElementById("resultsChart");


if (resultsChart) {

    // Get the result data that Flask placed in the HTML
    const chartLabels =
        JSON.parse(resultsChart.dataset.labels);

    const chartScores =
        JSON.parse(resultsChart.dataset.scores);


    new Chart(resultsChart, {

        type: "bar",

        data: {

            labels: chartLabels,

            datasets: [{

                label: "Score",

                data: chartScores,

                backgroundColor: "#2946D7",

                borderRadius: 10,

                barThickness: 30

            }]

        },

        options: {

            indexAxis: "y",

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: false
                }

            },

            scales: {

                x: {

                    beginAtZero: true,

                    ticks: {
                        precision: 0
                    }

                },

                y: {

                    grid: {
                        display: false
                    }

                }

            }

        }

    });

}
