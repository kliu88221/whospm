const ingredients = ['Pepperoni', 'Pineapple', 'Ham']
const ASSETS = {};


let loaded = 0
ingredients.forEach(item => {
  const img = new Image()
  const path = '/static/img/' + item.toLowerCase() + '.png';
  img.src = path
  img.onload = () =>{
    ASSETS[path] = img;
    loaded++;
    if(loaded == ingredients.length) {
      render()
    }
  }
})

function render(){
  const containers = document.querySelectorAll('.pizza-container')
  containers.forEach(container => {
      const data = container.dataset.pizza;
      if (data) {
        const pizza = JSON.parse(rawData);
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
    }else{
      print("where sauce")
    }

    if(pizza.toppings){
      pizza.toppings.forEach(t => {
        const img = ASSETS[t.image_url];
        if (img) {
          ctx.drawImage(img, t.x - 37.5, t.y - 37.5, 75, 75);
        } else {
          // fall back
          ctx.fillStyle = "red";
          ctx.beginPath(); 
          ctx.arc(t.x, t.y, 10, 0, Math.PI*2); 
          ctx.fill();
        }
      });
    }

}

