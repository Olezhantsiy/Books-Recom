document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".bookmark-btn");

    buttons.forEach(button => {
        const icon = button.querySelector(".bookmark-icon");
        const isPlanned = button.dataset.planned === "true";

        if (isPlanned) {
            icon.src = "/static/images/bookmark-fill.svg";
        }

        button.addEventListener("click", function () {
            const isbn = button.dataset.isbn;
            const planned = button.dataset.planned === "true";

            axios.post("/library/add/", { isbn: isbn })
                .then(response => {
                    if (response.data.success) {
                        button.dataset.planned = planned ? "false" : "true";
                        icon.src = planned ?
                            "/static/images/bookmark.svg" :
                            "/static/images/bookmark-fill.svg";
                    }
                })
                .catch(error => {
                    console.error("Ошибка при добавлении в библиотеку:", error);
                });
        });
    });
});
