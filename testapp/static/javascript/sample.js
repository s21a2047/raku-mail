window.onload = function() {
    var changeColor = function() {
        var e = document.getElementById('test');
        e.style.color = 'red';
        console.log("書き換えテスト")
    }
    setTimeout(changeColor, 5000);
}

var selecterBox = document.getElementById('sentence');

    function formExplanation() {
        check = document.getElementsByClassName('Explanation')
        if (check[0].checked) {
            selecterBox.style.display = "none";

        } else if (check[1].checked) {
            selecterBox.style.display = "block";

        } else {
            selecterBox.style.display = "none";
        }
    }
    window.addEventListener('load', formExplanation());

function entryChange2(){
    if(document.getElementById('changeSelect')){
    id = document.getElementById('changeSelect').value;
}
}