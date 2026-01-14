const canvas = document.getElementById('pizzaCanvas');
const ctx = canvas.getContext('2d');
const toppingImgs = {};
const toppings = ['Pepperoni', 'Pineapple', 'Ham'];

toppings.forEach(item => {
  const img = new Image()
  img.src = '/static/img/' + item.toLowerCase() +'.png'
  toppingImgs[item] = img
})

let pizza = {
    sauce: { name: 'None', color: '#f5deb3' }, // Default to crust color
    toppings: [] // This will store {id: 1, name: 'Pepperoni', x: 50, y: 50}
};

let currentTool = null;

function drawPizza() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.arc(250, 250, 200, Math.PI, -Math.PI)
    ctx.lineWidth = 5
    ctx.stroke()
    ctx.fillStyle = "#f5deb3"
    ctx.fill()

    if(pizza.sauce.name != "None"){
      ctx.beginPath();
      ctx.arc(250, 250, 180, Math.PI, -Math.PI)
      ctx.fillStyle = pizza.sauce.color
      ctx.fill()
    }

    pizza.toppings.forEach(top =>{
      const img = toppingImgs[top.name];
      if(img){
        let size = 50
        ctx.drawImage(img, top.x - size/2, top.y - size/2, size, size);
      }else{
        ctx.beginPath()
        ctx.arc(top.x, top.y, 10, 0, Math.PI * 2);
          ctx.fillStyle = "red";
          ctx.fill();
      }
    })

}

function setSauce(name, color) {
  // set using button, sauce name and then color in hex?. pushing to pizza
  pizza.sauce = {name: name, color: color}
  currentTool = null;
  drawPizza()
}

function setTool(id, name) {
  // set using button, id should be incremental int, and then name just ingredient name
  currentTool = {id: id, name: name}
  console.log("Selected: " + name)
}


canvas.addEventListener('mousedown', (evt) => {
    if (!currentTool) return; // do nothing if no topping selected

    // xycoordinates relative to canvas
    const rect = canvas.getBoundingClientRect();
    const x = evt.clientX - rect.left;
    const y = evt.clientY - rect.top;

    pizza.toppings.push({
        id: currentTool.id,
        name: currentTool.name,
        x: x,
        y: y
    });

    drawPizza();
});

drawPizza();
