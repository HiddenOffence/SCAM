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

