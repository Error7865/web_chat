//This page only for style purpose ------------------------------------------------------------------------------
var gStyle={}

document.querySelector('.info-icon').addEventListener('click', (e)=>{
        if(document.querySelector('.miniprofile-pic')==null)
            setPicDiv(reverse=false)
        else
            console.log('You call already.');
})


            /*****Function start from here ****** */
function setPicDiv(reverse=true) {
    let pic=document.querySelector('.pic-container > .pic')
    let profilePicture=document.querySelector('#profile-picture')
    let close=document.querySelector('.pic > .cross')
    let infoCircle=document.querySelector('.bi-info-circle')
    if(reverse){
        createInfo('', true)
        setTimeout(()=>{
            infoCircle.style.display='block'
            infoCircle.style.opacity=1
            close.style.display='block'
            profilePicture.style.left='0vw'
            profilePicture.style.top='-2.3em'
            profilePicture.style.position='relative'
            width(pic, '30vw')
            height(pic, '30vw')
            profilePicture.style.borderRadius='2%'
            profilePicture.style.marginTop='0em'
            width(profilePicture, '')
            height(profilePicture, '')
        }, 500)
    }else{
        gStyle.pic={width: '30vw',
            height: '30vw'}      //default width mention in home.css
        infoCircle.style.opacity=0
        // profilePicture.style.opacity=0
        close.style.display='none'
        profilePicture.style.left='40vw'
        width(profilePicture, '20vw')
        height(profilePicture, '20vw')
        profilePicture.style.position='absolute'
        profilePicture.style.top=+pic.offsetTop+'px'
        // profilePic.style.left=pic.offsetLeft+'px'
        width(pic, '100vw')
        height(pic,'100vh')
        setTimeout(()=>{
            infoCircle.style.display='none'
            pos(profilePicture, 'absolute')
            profilePicture.style.borderRadius='50%'
            // profilePicture.style.opacity=1
            profilePicture.style.marginTop='1em'
            profilePicture.style.top='2em'
            filename=profilePicture.src.split('/').reverse()[0]
            getUserInfo()
            // createInfo(profilePicture.src)
        }, 500)
        // profilePicture.style.left='40vw'
    }
}

function hideWithOpacity(target, opaValue, rev=false, display='none', timeout=500) {
    if(rev){
        target.style.display=display
        target.style.opacity=opaValue
        return
    }
    target.style.opacity=opaValue
    setTimeout(()=>{
        target.style.display=display
    }, timeout)    
}

function width(target, width=null){
    if(width==null){
        return target.style.width
    }
    return target.style.width=width
}

function height(target, height=null){
    if(height==null){
        return target.style.height
    }
    return target.style.height=height
}

function pos(target, position=null) {
    if(position==null){
        return target.style.position
    }
    return target.style.position=position
}

function createInfo(user, rev=false){
    let parent=document.querySelector('.pic')
    let div=document.createElement('div')
    if(rev){
        div=document.querySelector('.pic > .miniprofile-info')
        div.style.marginTop='100vw'
        setTimeout(()=>{
            div.remove()
        }, 500)
        return
    }
    let h3=document.createElement('h3')
    let usermail=document.createElement('h3')
    let close=document.createElement('p')
    let textNode=document.createTextNode(`Name: ${user.name}`)
    let mailNode=document.createTextNode(`Email: ${user.mail}`)
    div.classList.add('miniprofile-info')
    close.classList.add('close')
    h3.appendChild(textNode)
    usermail.appendChild(mailNode)
    close.innerHTML='&times;'
    div.appendChild(h3)
    div.appendChild(usermail)
    div.appendChild(close)
    parent.appendChild(div)
    
    setTimeout(()=>{
        div.style.marginTop='30vw'
        document.querySelector('.miniprofile-info > .close').style.bottom='2vw'
    }, 500)
    close.addEventListener('click', (e)=>{
        setPicDiv(true)
    })
}
