const btn = document.getElementById("run-scraper");
const loader = document.getElementById("loader")

btn.addEventListener("click", function () {
    loader.style.display = "block";

    fetch(btn.dataset.runUrl)
        .then(() => {
            window.location.href = btn.dataset.homeUrl;
        });
})
