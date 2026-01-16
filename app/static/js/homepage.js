
const ingredients = ['Pepperoni', 'Pineapple', 'Ham', 'Mushroom', 'Demon', 'Cheese'];
const ASSETS = {};

let loaded = 0;

ingredients.forEach(item => {
  const img = new Image();

  const path = '/static/img/' + item.toLowerCase() + '.png';
  img.src = path;

  img.onload = () => {
    ASSETS[path] = img;
    checkLoad();
  }
})

function checkLoad() {
  loaded++;
  if(loaded === ingredients.length) {
    render();
  }
}

function render(){
  const containers = document.querySelectorAll('.pizza-container')

  containers.forEach(container => {
    const dataStr = container.dataset.pizza; 
    if (dataStr) {
      const pizza = JSON.parse(dataStr); 
      const canvas = container.querySelector('canvas');
      drawPizza(canvas, pizza);
    }
  })
}

function drawPizza(canvas, pizza) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.arc(250, 250, 250, Math.PI, -Math.PI)
    ctx.fillStyle = "#f5deb3"
    ctx.fill()


    if(pizza.sauce_name && pizza.sauce_name !== "None"){
      ctx.beginPath();
      ctx.arc(250, 250, 225, Math.PI, -Math.PI)
      ctx.fillStyle = pizza.sauce_color
      ctx.fill()
    }

    if(pizza.toppings){
    pizza.toppings.forEach(t => {
      const img = ASSETS[t.image_url];

      if (img) {
        ctx.drawImage(img, t.x - 37.5, t.y - 37.5, 75, 75);
      } else {
        console.warn("Missing asset for:", t.name);
        ctx.fillStyle = "red";
        ctx.beginPath(); 
        ctx.arc(x, y, 10, 0, Math.PI*2); 
        ctx.fill();
      }
    });
    }
}