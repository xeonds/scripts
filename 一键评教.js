let inputs = document.querySelectorAll(".bh-radio-label")
for( let i=0; i<inputs.length; i++)
	if (inputs[i].innerText == '完全符合 '||inputs[i].innerText == '非常满意 ')
		inputs[i].click()
