

function graph(content){
    content.forEach(function (expr){
        calculator.setExpression({latex: expr, color: '#ff0000' });
    })
    calculator.setExpression({id: 'a', latex: 'a=0', color: '#ff0000' });
    var a = 0
    const ticker = setInterval(() => {
        a += 0.1;  // Increment 'a' by 0.1 every tick
        calculator.setExpression({ id: 'a', latex: `a=${a}` });
    }, 100); 
}


document.getElementById('file')
            .addEventListener('change', (event) => {
                const file = event.target.files[0];
                const reader = new FileReader();
 
                reader.onload = function () {
                    var content = reader.result;
                    content = content.split('\n');
                    graph(content);
                };
 
                reader.onerror = function () {
                    console.error('Error reading the file');
                };
 
                reader.readAsText(file, 'utf-8');
            });