const canvas = document.getElementById('pizzaCanvas');
const ctx = canvas.getContext('2d');


let pizza = {
    sauce: { name: 'None', color: '#f5deb3' }, // Default to crust color
    toppings: [] // This will store {id: 1, name: 'Pepperoni', x: 50, y: 50}
};

let currentTool = null;

function drawPizza() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

}

function setSauce(name, color) {
}

function setTool(id, name) {
}


canvas.addEventListener('mousedown', (e) => {
    if (!currentTool) return; // do nothing if no topping selected

    // xycoordinates relative to canvas
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    pizza.toppings.push({
        id: currentTool.id,
        name: currentTool.name,
        x: x,
        y: y
    });

    drawPizza();
});

drawPizza();