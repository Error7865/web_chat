
var btn=document.getElementsByClassName('btn');
for(let i=0;i<btn.length; i++){
    btn[i].addEventListener('click', (e)=>{
        e.preventDefault();
        let target=e.target;
        // target.classList.add('click-btn');
        target.style.opacity=0;
        let expand=null;    //declare a variable which contain .left or .right base on which user click
        if(target.textContent.indexOf('Sign') != -1){
            expand=document.getElementsByClassName('left')[0];
        }else{
            expand=document.getElementsByClassName('right')[0];
        }
        expand.style.width="100vw";
    })
}

var arrows=document.getElementsByClassName('arrow-container');
for (let index = 0; index < arrows.length; index++) {
    arrows[index].addEventListener('click', (e)=>{
        let target=e.target;
        let invisible=null;
        //sometime user can click svg icon of div element
        if (target.tagName.toLowerCase()=='div') {//User click on svg icon 
            target=target.children[0];
        }
        if(target.classList.contains('left-arrow')){    //it denote sign up click
            target=document.getElementsByClassName('left')[0];
            invisible=document.getElementById('sign');
        }else{
            target=document.getElementsByClassName('right')[0];
            invisible=document.getElementById('log');
        }
        target.style.width="0";
        invisible.style.opacity='1';
    })
}

function getGrandParent(el) {
    return el.parendNode.parentNode;
}

function hello() {
    console.log('Hello World.')
}