var numpad = {
  
  selector : null, 
  display : null, 
  zero : null,
  dot : null, 
  init : function () {
   
    numpad.selector = document.createElement("div");
    numpad.selector.id = "numpad-back";
    var wrap = document.createElement("div");
    wrap.id = "numpad-wrap";
    numpad.selector.appendChild(wrap);

    numpad.display = document.createElement("input");
    numpad.display.id = "numpad-display";
    numpad.display.type = "text";
    numpad.display.readOnly = true;
    wrap.appendChild(numpad.display);

 
    var buttons = document.createElement("div"),
        button = null,
        append = function (txt, fn, css) {
          button = document.createElement("div");
          button.innerHTML = txt;
          button.classList.add("numpad-btn");
          if (css) {
            button.classList.add(css);
          }
          button.addEventListener("click", fn);
          buttons.appendChild(button);
        };
    buttons.id = "numpad-btns";
    
    for (var i=7; i<=9; i++) {
      append(i, numpad.digit);
    }
    append("&#10502;", numpad.delete, "ng");
    
    for (var i=4; i<=6; i++) {
      append(i, numpad.digit);
    }
    append("C", numpad.reset, "ng");
    
    for (var i=1; i<=3; i++) {
      append(i, numpad.digit);
    }
    append("&#10006;", numpad.hide, "cx");
   
    append(0, numpad.digit, "zero");
    numpad.zero = button;
    append(".", numpad.dot);
    numpad.dot = button;
    append("&#10004;", numpad.select, "ok");

    wrap.appendChild(buttons);
    document.body.appendChild(numpad.selector);
  },


  attach : function (opt) {
  

    var target = document.getElementById(opt.id);
    if (target!=null) {

      if (opt.readonly==undefined || typeof opt.readonly!="boolean") { opt.readonly = true; }
      if (opt.decimal==undefined || typeof opt.decimal!="boolean") { opt.decimal = true; }
      if (opt.max==undefined || typeof opt.max!="number") { opt.max = 16; }

     
      if (opt.readonly) { target.readOnly = true; }

    
      target.dataset.decimal = opt.decimal ? 1 : 0;


      target.dataset.max = opt.max;

    
      target.addEventListener("click", numpad.show);
    } else {
      console.log(opt.id + " NOT FOUND!");
    }
  },

  target : null, 
  dec : true, 
  max : 16, 
  show : function (evt) {
  


    numpad.target = evt.target;

 
    numpad.dec = numpad.target.dataset.decimal==1;
    if (numpad.dec) {
      numpad.zero.classList.remove("zeroN");
      numpad.dot.classList.remove("ninja");
    } else {
      numpad.zero.classList.add("zeroN");
      numpad.dot.classList.add("ninja");
    }

    numpad.max = parseInt(numpad.target.dataset.max);

    
    var dv = evt.target.value;
    if (!isNaN(parseFloat(dv)) && isFinite(dv)) {
      numpad.display.value = dv;
    } else {
      numpad.display.value = "";
    }

    
    numpad.selector.classList.add("show");
  },

  hide : function () {
  
    numpad.selector.classList.remove("show");
  },

  
  delete : function () {
  

    var length = numpad.display.value.length;
    if (length > 0) {
      numpad.display.value = numpad.display.value.substring(0, length-1);
    }
  },

  reset : function () {
  

    numpad.display.value = "";
  },

  digit : function (evt) {
  

    var current = numpad.display.value,
        append = evt.target.innerHTML;

    if (current.length < numpad.max) {
      if (current=="0") {
        numpad.display.value = append;
      } else {
        numpad.display.value += append;
      }
    }
  },

  dot : function () {


    if (numpad.display.value.indexOf(".") == -1) {
      if (numpad.display.value=="") {
        numpad.display.value = "0.";
      } else {
        numpad.display.value += ".";
      }
    }
  },

  select : function () {
  

    var value = numpad.display.value;

    
    if (!numpad.dec && value%1!=0) {
      value = parseInt(value);
    }

    
    numpad.target.value = value;
    numpad.hide();
  }
};


window.addEventListener("load", numpad.init);