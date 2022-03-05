function getOutput(){
	return document.getElementById("Input").value;
}

function calculate() {
    isOutput = true;
}

function getFormattedNumber(num){
	if(num=="-"){
		return "";
	}
	var n = Number(num);
	var value = n.toLocaleString("en");
	return value;
}

function printOutput(num){
	if(num==""){
		document.getElementById("Input").value=num;
	}
	else{
		document.getElementById("Input").value=num;
	}	
}

document.getElementsByName("clear")[0].addEventListener('click', function() {
	console.log("clear called")
	document.getElementById("Input").value = " ";
	document.getElementById("Input").innerText = "";
	isCleared = true;
})

var isCleared = false;
var isOutput = false;
var button = document.getElementsByClassName("num");
for(var i =0;i<button.length;i++){
	console.log(button[i].id);
    if (button[i].name == "clear") {
        continue;
    }

	button[i].addEventListener('click', function(){
		if (isCleared) {
			output = ""
		}
		var output=getOutput();
		if(output!=NaN){ //if output is a button
            if (isOutput) {
                output = this.id;
            } else {
			    output = output+this.id;
            }
			console.log(output);
			printOutput(output);
		}
	});
}