

var cross=document.getElementsByClassName('flash-cross')

for(let i=0; i<cross.length; i++){
    cross[i].addEventListener('click',
        (e)=>{
            let target=e.target;
            let parent=target.parentNode;
            parent.style.display="none";
        }
    )
}

function getGrandparent(el) {
    return el.parentNode.parentNode;
}

function addClass(el, className) {
    el.classList.add(className)    
}
function haveClass(el, className) {
    if(el.className.indexOf(className)>-1)    
        return  true
    return false
}
function removeClass(el, className) {
    el.classList.remove(className)    
}

function showFlashMsg(msg) {
    let flashMsgContainer=document.createElement('p');
    flashMsgContainer.classList.add('flash-msg');
    let flashMsg=document.createTextNode(msg);
    flashMsgContainer.appendChild(flashMsg);
    flashMsgContainer.style.opacity=1;
    flashMsgContainer.style.transition="opacity 0.5s linear";
    let parent=document.querySelector('.flash-container');
    parent.appendChild(flashMsgContainer);
    setTimeout(()=>{
        flashMsgContainer.style.opacity=0;
        setTimeout(()=>{
            parent.removeChild(flashMsgContainer);
        },1000);
    }, 4000);
}

function removeChildren(parent, children) {
    for(let i=0; i<children.length; i++)    {
        parent.removeChild(children[i])
    }
}

function insertElementsBeforeEle(parent, elements, beforeEle) {
    for (let i = 0; i < elements.length; i++) {
        parent.insertBefore(elements[i], beforeEle);
    }    
}

function haveChildren(el) {
    if(el.childElementCount==0)
        return false
    return true
}

function hideAll(elements){
    elements.forEach((element, index)=>{
        element.classList.add('hide')
    })
}

function reverseStr(str) {
    let array=str.split('')
    return  array.reverse().join('')
}

function getChild(children, tagname, textcontent=null) {
    for(let i=0; i<children.length; i++){
        if(children[i].tagName==tagname){
            if (textcontent==null || textcontent==el.textContent) {
                return children[i]
            }
        }
    }
}

function getFileType(url){
    let video=['mp4', 'avi']
    let img=['jpg', 'jpeg', 'png', 'gif']
    let audio=['mp3', 'ogg']
    let doc=['pdf']
    let extension=getFileExtension(url)
    if(video.indexOf(extension) > -1 )
        return 'video'
    else if(img.indexOf(extension) > -1 )
        return 'img'
    else if(audio.indexOf(extension) > -1 )
        return 'audio'
    else
        return 'a'
}

function getFileName(url){
    /**This function return file name with extension
     * from an url
     */
    let list=url.split('/')
    return list.reverse()[0]
}
