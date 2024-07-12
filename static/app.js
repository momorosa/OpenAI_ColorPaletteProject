// Add event listener for form submission
const form = document.querySelector("#form");
form.addEventListener("submit", async function(e) {
    e.preventDefault();
    await getColors();
});

async function getColors() {
    const query = form.elements.query.value;
    try {
        const response = await fetch("/palette", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                query: query
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const colors = data.colors;
        // console.log(colors);
        const container = document.querySelector(".container");
        createColorBlocks(colors, container);
    } catch (error) {
        console.error('Error fetching color palette:', error);
    }
}

function createColorBlocks(colors, parent) {
    parent.innerHTML = ""; // Clear existing color blocks
    colors.forEach(color => {
        const colorBlock = createColorBlock(color);
        parent.appendChild(colorBlock);
    });
}

function createColorBlock(color) {
    const div = document.createElement("div");
    div.classList.add("color");
    div.style.backgroundColor = color;
    div.style.width = `calc(100% / ${colors.length})`;

    // Copy color code to clipboard on click
    div.addEventListener("click", function() {
        navigator.clipboard.writeText(color);
    });

    const span = document.createElement("span");
    span.innerText = color;
    div.appendChild(span);
    return div;
}