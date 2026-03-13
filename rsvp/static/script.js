document.documentElement.classList.remove("no_js");

//HANDLE SIDEBAR OPENING

const sidebar = document.querySelector(".sidebar");
const button = document.querySelector(".openbtn")
let isOpen = false;

function openNav() {
    if (!isOpen) {
        sidebar.style.width = "100vw";
        button.style.transform = "rotate(180deg)";
        isOpen = true;
    }
    else {
        sidebar.style.width = "0";
        button.style.transform = "rotate(0)";
        isOpen = false;
    }
}

//HANDLE PHOTO GRID LOADING ANIMATION + PAGE TRANSITIONS

document.addEventListener("DOMContentLoaded", () => {
    const photosGridContainer = document.querySelector('.photos_grid_container');
        
    if (photosGridContainer) {
        const images = photosGridContainer.querySelectorAll('img');

        let imagesLoaded = 0;
        const totalImages = images.length;

        if (totalImages === 0) {
            photosGridContainer.classList.add('loaded');
            return;
        }

        images.forEach((img) => {
            if (img.complete) {
                increment();
            }
            else {
                img.addEventListener("load", increment);
                img.addEventListener("error", increment);
            }
        });

        function increment() {
            imagesLoaded++;
            if (imagesLoaded === totalImages) {
                photosGridContainer.classList.add('loaded');
            }
        }
    }

    const page = document.getElementById("page");
    console.log("page: ", page);

    if (page) {
        page.classList.add("loaded");

        document.querySelectorAll("a[href]").forEach(link => {
            const url = link.getAttribute("href");

            if (
                link.target === "_blank" ||
                url.startsWith("#") ||
                url.startsWith("http")
            ) return;

            link.addEventListener("click", e => {
                e.preventDefault();
                page.classList.remove("loaded");
                page.classList.add("fade-out");

                setTimeout(() => {
                    window.location.href = url;
                }, 500);
            });
        });
    }
});

