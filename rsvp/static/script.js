//HANDLE SIDEBAR OPENING

const sidebar = document.querySelector(".sidebar");
const button = document.querySelector(".openbtn")
let isOpen = false;

function openNav() {
    if (!isOpen) {
        sidebar.style.width = "100vw"
        button.style.transform = "rotate(180deg)" 
        isOpen = true;
    }
    else {
        sidebar.style.width = "0"
        button.style.transform = "rotate(0)"
        isOpen = false;
    }
}