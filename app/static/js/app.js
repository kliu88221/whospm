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
let mouse = { x: 0, y: 0, isOver: false };
let isSaved = true;

function drawPizza() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.arc(250, 250, 250, Math.PI, -Math.PI)
    ctx.fillStyle = "#f5deb3"
    ctx.fill()

    if(pizza.sauce.name != "None"){
      ctx.beginPath();
      ctx.arc(250, 250, 225, Math.PI, -Math.PI)
      ctx.fillStyle = pizza.sauce.color
      ctx.fill()
    }

    pizza.toppings.forEach(top =>{
      const img = toppingImgs[top.name];
      if(img){
        let size = 75
        ctx.drawImage(img, top.x - size/2, top.y - size/2, size, size);
      }else{
        ctx.beginPath()
        ctx.arc(top.x, top.y, 10, 0, Math.PI * 2);
          ctx.fillStyle = "red";
          ctx.fill();
      }
    })

    if (currentTool && mouse.isOver) {
      const ghostImg = toppingImgs[currentTool.name];
      
      if(ghostImg && ghostImg.complete) {
        ctx.save();
        ctx.globalAlpha = 0.5;
        let size = 75;

        ctx.drawImage(ghostImg, mouse.x - size/2, mouse.y - size/2, size, size);
        
        ctx.restore(); 
      }
    }

}

function uiSetActive(element, groupClass) {
  document.querySelectorAll('.' + groupClass).forEach(btn => {
    btn.classList.remove('-translate-y-4', 'scale-110', 'ring-4', 'ring-orange-200', 'rounded-full');
  });
  if(element) {
    element.classList.add('-translate-y-4', 'scale-110', 'ring-4', 'ring-orange-200', 'rounded-full');
  }
}


function setSauce(name, color, el) {
  // set using button, sauce name and then color in hex?. pushing to pizza
  pizza.sauce = {name: name, color: color}
  uiSetActive(el, 'sauce-btn');
  currentTool = null;
  uiSetActive(null, 'topping-btn');
  isSaved = false;
  drawPizza()
}

function setTool(id, name, el) {
  // set using button, id should be incremental int, and then name just ingredient name
  currentTool = {id: id, name: name}
  uiSetActive(el, 'topping-btn');
  console.log("Selected: " + name)
}

async function savePizza() {
  if (isSaved) {
    alert("No changes to save!");
    return;
  }
  const saveButton = document.getElementById('saveBtn');
  const originalText = saveButton.innerText; 
  const payload = JSON.stringify(pizza);

  saveBtn.innerText = "Saving...";
  saveBtn.disabled = true;

  try {
    const response = await fetch('/db/save_pizza', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload
    });

    const ret = await response.json();

    if (response.ok && ret.status === "success") {
      isSaved = true;
      // window.location.href = "/profile";
      setTimeout(() => {
        saveBtn.innerText = originalText;
        saveBtn.disabled = false;
        saveBtn.classList.remove("bg-blue-500", "hover:bg-blue-600");
        saveBtn.classList.add("bg-green-500", "hover:bg-green-600");
      }, 2000);
      console.log("Success:", ret);
    } else {
      alert("Failed to save: " + (ret.message || "Unknown error"));
    }

  } catch (error) {
    // network crashes
    console.error("save error:", error);
    saveBtn.innerText = "Error saving!!";
    saveBtn.classList.remove("bg-green-500");
    saveBtn.classList.add("bg-red-500");

    setTimeout(() => {
      saveBtn.innerText = originalText;
      saveBtn.disabled = false;
      saveBtn.classList.remove("bg-red-500");
      saveBtn.classList.add("bg-green-500");
    }, 2000);
    console.error("Network Error:", error);
    alert("network error, check terminal, is server up?");
  }
}

canvas.addEventListener('mousemove', (evt) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = evt.clientX - rect.left;
    mouse.y = evt.clientY - rect.top;
    mouse.isOver = true;
    
    drawPizza();
});

canvas.addEventListener('mouseleave', () => {
    mouse.isOver = false;
    drawPizza();
});

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

    isSaved = false;
    drawPizza();
});



drawPizza();
