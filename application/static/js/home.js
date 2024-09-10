//global is a global object that can be use in need.
var global={}
// Design part start from here 
pointActiveBar(document.getElementsByClassName('option chat')[0])

// Design part end here 
var cross=document.getElementsByClassName('cross')[0]
cross.addEventListener('click', (e)=>{
    let cross=e.target;
    let crossgrandparent=getGrandParent(cross);
    crossgrandparent.style.display='none';
    delete global.userMail
})

var userProfile=document.getElementsByClassName('user-profile-pic');
for (let i = 0; i < userProfile.length; i++) {
    userProfile[i].addEventListener('click', (e)=>{
        let img=e.target
        let parent=img.parentNode
        let email=getChild(parent.children, 'A').textContent.split(' ')[0]
        global.userMail=email
        showUserProfile(img.src);
    })
}

document.querySelector('.viewer > .close').addEventListener('click', (e)=>{
    let target=e.target
    console.log('Here target ', target);
    let subview=document.querySelector('.viewer > .subview')
    let children=subview.children
    target.parentNode.classList.add('hide')
    for(let i=0; i< children.length; i++){
        subview.removeChild(children[i])
    }
})

document.querySelector('.dots').addEventListener('click', (e)=>{
    let target=e.target
    let config=document.querySelector('.config')
    let selfname=document.querySelector('.self-name')
    pointActiveBar(target)
    setTimeout(()=>{
        config.style.height='100vh'
        config.style.width='100vw'
        setTimeout(()=>{
            setOpatcityVisible('visible')
            global.username=document.querySelector('.self-name').value
        }, 1000)
    }, 500)
    global.picUrl=document.querySelector('.dp').src
    if(global.name != null || global.name != undefined){
        selfname.value=global.name
    }
})

document.querySelector('.config > .close').addEventListener('click', (e)=>{
    let config=document.querySelector('.config')
    let save=document.querySelector('#save')
    let selfname=document.querySelector('.self-name')
    let dp=document.querySelector('.dp')
    setOpatcityVisible('visible', false)
    setTimeout(()=>{
        config.style.height=0
        config.style.width=0
        pointActiveBar(document.querySelector('.chat'))
    }, 600)
    if(!haveClass(save, 'hide'))
        save.classList.add('hide')
    if(selfname.value != global.username)
        selfname.value = global.username
    dp.src=global.picUrl
})

document.querySelector('.self-name').addEventListener('input', (e)=>{
    let target=document.querySelector('.self-name')
    let save=document.getElementById('save')
    if(target.value != global.username){
        save.classList.remove('hide')
        return
    }
    save.classList.add('hide')
})

var socket=io();  //stabilish connection with server using socket

attachEventtoInfo();    //attache click event to info class elements


socket.on('connect',()=>{
    let userKey=document.querySelector('#user_profile_pic').dataset.userkey;
    socket.emit('active user', userKey);
    // socket.emit('call');
    
})
socket.on('decorate_msg', (msgList)=>{
    for(let i=0;i<msgList.length; i++){
        createChatNode(msgList[i].msg, msgList[i].owner, url=msgList[i].url)
    }
    scrolltoLastMsg()
});

socket.on('receive msg', (data)=>{
    // console.log('Sender '+document.querySelector('#to').value);
    if(document.querySelector('#to').value==data.sender){
        //This if statement indicate that user looks this user messages
        //So just insert another chat
        // alert('It called.')
        createChatNode(data.msg, false, data.url);
    }else{
        let senderAnchor=lookingUserAnchor(data.sender);
        try{    //It just handle thoes case where senderAnchor haven't any child with span tag name
            let targetspan=senderAnchor.children[0];
            targetspan.textContent=Number(targetspan.textContent)+1;
            targetspan.classList.remove('hide');
        }catch(TypeError){
            let textNode=document.createTextNode(1);
            let span=document.createElement('sapn');
            span.className='number-msg';
            span.appendChild(textNode);
            senderAnchor.appendChild(span);
        }
    }
    // console.log('Here audio file location '+data.audio);
    let audio=new Audio(data.audio);
    audio.play();
})

document.getElementById('send').addEventListener('click', (e)=>{
    let msg=document.getElementById('message').value;
    document.getElementById('message').value='';
    if(msg=='')
        return '';
    let to=document.getElementById('to').value;
    if(global.file != undefined){
        let file =global.file
        delete global.file
        socket.emit('new media', msg, to, file.name, file, (data)=>{
            createChatNode(data.msg, data.owner, url=data.url)
        })
    }else{
        socket.emit('receive msg', msg, to);
    }
    document.querySelector('.folder').classList.remove('load')
})

document.querySelector('.add-container').addEventListener('click', (e)=>{
    let searchBox=document.querySelector('#search-box');
    let searchIcon=document.querySelector('.search-icon-container');
    if(searchBox.style.opacity==0){
        searchBox.style.opacity=1;
        searchIcon.style.opacity=1;
    }else{
        searchBox.style.opacity=0;
        // searchIcon.classList.add('hide');   
        searchIcon.style.opacity=0;
    }
});

document.querySelector('#search-box').addEventListener('keyup', (e)=>{
    // console.log('You just enter. '+e.keyCo);
    let value=e.target.value; //value of #search-box inputfield
    let matchEles=searchMatchedUser(value);
    // console.log('Here mathcList '+matchList);
    let parent=document.querySelector('.users');
    removeChildren(parent, matchEles);
    insertElementsBeforeEle(parent, matchEles, parent.children[0]);
})

document.querySelector('.search-icon-container').addEventListener('click', (e)=>{
    let searchBox=document.querySelector('#search-box');
    if(searchBox.value=='' || searchBox.value==' ')         //input box empty
        return null
    let serachInput=searchBox.value;
    let userKey=document.querySelector('#user_profile_pic').dataset.userkey;   
    socket.emit('search user', serachInput);
    
})

document.querySelector('.update').addEventListener('click', (e)=>{
    e.preventDefault();
    pointActiveBar(document.querySelector('.update'))
    showUpdates()
    socket.emit('update user', (data)=>{
        data.forEach(element => {
            if(!isExitsUpdateUser(element.user)){
                insertUpdateUser(element.user, element.img)
                if(sessionStorage.getItem(element.user)===null){
                    sessionStorage.setItem(element.user, element.updates)
                }else{
                    let value=sessionStorage.getItem(element.user)
                    sessionStorage.setItem(element.user, value+','+element.updates)
                    value=''
                }
            }
        });
        addEventToUserUpdates()
    })
})

socket.on('set user', (user)=>{
    /**This will call after search by user for any other user
     * and server send data based on that
    */

    if(!user.found){
        return showFlashMsg("No result found !");
    }
    if(!wasUserFriend)
        insertUser(user.profile, user.email);
})

document.querySelector('#update-input').addEventListener('change', (e)=>{
    let file=e.target.files[0]
    if(file===null)
        return false
    if (file.size > 5*1024*1024) {
        //It will check that file is not larger than 5MB
        showFlashMsg('File was too large')
        console.log(`file size ${file.size} expected size ${5*1024*1024}`);
        return false
    }
    let target=isValidMedia(file)

    document.querySelector('.update-container').classList.remove('hide')
    let reader=new FileReader()
    reader.addEventListener('load', (e)=>{
        target.el.src=reader.result
        if(target.isvideo){
            target.el.play()
        }
        document.querySelector('#submit').classList.remove('hide')
    })
    reader.readAsDataURL(file)
})

document.querySelector('#video').addEventListener('click', (e)=>{
    let video=e.target
    if(video.paused)
        video.play()
    else
        video.pause()
})
document.querySelector('.update-container > .close').addEventListener('click', (e)=>{
    let target=e.target
    let active=document.querySelector('.update-container > .active')
    // active.src=''
    if(active.tagName.toLowerCase()==='video'){
        active.pause()
    }
    active.classList.remove('active')
    active.classList.add('hide')
    document.querySelector('form').reset()
    target.parentElement.classList.add('hide')
}, true)

document.querySelector('#submit').addEventListener('click', (e)=>{
    e.preventDefault()
    let input=document.querySelector('#update-input')
    let file=input.files[0]
    if(file==''){
        console.log('File was empty.');
        return false
    }
    document.querySelector('.update-container').classList.add('hide')
    let active=document.querySelector('.update-container > .active')
    if(active.tagName.toLowerCase()=='video'){
        active.pause()
    }
    socket.emit('upload', file, file.name, ()=>{
        active.classList.add('hide')
        active.classList.remove('active')
    })
})

socket.on('new update', (data)=>{
    let value=sessionStorage.getItem(data.user)  
    if(value==null){
        sessionStorage.setItem(data.user, data.update)
        insertUpdateUser(data.user, data.img)
        addEventToUserUpdates()
    }else{
        sessionStorage.setItem(data.user, value+','+data.update)
        value=''
    }
    if(data.user != 'My Update'){   //My Update was user self
        showFlashMsg('A new update from '+data.user)
    }
})

document.querySelector('.bottom-part > .icon').addEventListener('click', async (e)=>{
    let target=e.target
    let file= await getFile()
    let extensions=['txt', 'jpg', 'jpeg', 'png', 'webp', 'gif', 'mp4', 'mp3', 'avi', 'pdf']
    if(extensions.indexOf(getFileExtension(file.name)) == -1){
        showFlashMsg('Unvalid file .')
        return
    }
    if(file.size > 10*1024*1024){
        showFlashMsg('File was too large. It should be less than  10MB')
        return
    }
    document.querySelector('.folder').classList.add('load')
    global.file=file
    // socket.emit('new media', file, file.name, (msg)=>{
    //     console.log(msg);
    // })
})

document.querySelector('#save').addEventListener('click', (e)=>{
    let save=e.target
    let selfname=document.querySelector('.self-name')
    let dp=document.querySelector('.dp')
    if(selfname.value == global.name)
        return
    global.name=selfname.value
    socket.emit('change name', selfname.value, (data)=>{
        global.name=data.name
        showFlashMsg(data.msg)
    })
    if(Number(save.dataset.profile)==1){
        socket.emit('update profile', global.file.filename, global.file.data, (data)=>{
            dp.src=data.url
            showFlashMsg(data.msg11)
            save.dataset.profile=0
            delete global.file
            global.url=data.url
            document.querySelector('#user-update').src=data.url
        })
    }
    document.querySelector('.config > .close').click()
})
socket.on('successfull', (msg)=>{
    showFlashMsg(msg)
})

document.querySelector('.dp').addEventListener('click', async (e)=>{
    let dp=document.querySelector('.dp')
    let save=document.querySelector('#save')
    let file
    try{
        file= await getFile()
        if(file.type.indexOf('image') > -1){
            if(checkFileSize(file.size, 10)){
                save.dataset.profile=1
                save.classList.remove('hide')
                global.file={filename:file.name,
                    data: file
                }
                let reader=new FileReader()
                reader.addEventListener('load', (e)=>{
                    dp.src=reader.result
                })
                reader.readAsDataURL(file)
            }
        }else{
            showFlashMsg('Unsupported media.')
        }
    }catch(DOMException){
        console.log("You just decline request.");
    }
})

socket.on('disconnect', ()=>{
    // let userKey=document.querySelector('#user_profile_pic').dataset.userkey;
    // socket.emit('deactive user', userKey);
    console.log('Here disconnect.');
    socket.emit('call');
});


        //*****************Fuctions are there *************************\\
function getGrandParent(el) {
    //It will return grandparent of any element
    return el.parentNode.parentNode;
}

function showUserProfile(src) {
    // This will change display property of pic-container for make user 
    // profile visible 
    let picContainer=document.getElementsByClassName('pic-container')[0]
    picContainer.style.display='flex';
    let img=document.getElementById('profile-picture');
    img.src=src;
}

function createChatNode(msg, owner=true, url=null) {
    //true mean that msg send current user to another user
    //and false means vice versa
    let parentofMsg=document.getElementsByClassName('chat-container')[0];    
    let div=document.createElement('div');
    let tooltip=document.createElement('p');
    addClass(tooltip, 'tooltip');
    let typeofMsgClass=null;
    let pText=document.createTextNode(msg);
    let ptag=document.createElement('p');
    if(owner){
        addClass(div, 'user-chat');
        typeofMsgClass='user-data';
        ptag.appendChild(pText);
        div.appendChild(ptag);
        div.appendChild(tooltip)
    }else{
        addClass(div, 'subuser-chat');
        typeofMsgClass='subuser-data';
        ptag.appendChild(pText);
        div.appendChild(tooltip)
        div.appendChild(ptag)
    }
    if(url != null){
        let fileTagName=getFileType(url)    //base.js
        let mediaTag=document.createElement(fileTagName)
        // mediaTag.src=file.value
        let br=document.createElement('br')
        ptag.prepend(br)
        ptag.prepend(mediaTag)
        if(mediaTag.tagName.toLowerCase()=='video' || mediaTag.tagName.toLowerCase()=='img'){
            mediaTag.classList.add('media')
            mediaTag.src=url
            addClickEventMediaClass(mediaTag)
        }else if(mediaTag.tagName.toLowerCase()=='audio'){
            mediaTag.classList.add('audio')
            mediaTag.src=url
            mediaTag.setAttribute('controls', '')
        }
        else{      //It was anchor tag just download it
            mediaTag.href=url
            mediaTag.classList.add('download')
            mediaTag.appendChild(document.createTextNode(getFileName(url)))
        }
    }
    addClass(ptag, typeofMsgClass)
    parentofMsg.appendChild(div);
}

function resetUserandSubuser() {
    deleteElements(document.querySelectorAll('.user-chat'));
    deleteElements(document.querySelectorAll('.subuser-chat'));
}

function deleteElements(elements) {
    let el=null;
    let parent=null;
    for (let index = 0; index < elements.length; index++) {
        el=elements[index];
        
        parent=el.parentElement;
        parent.removeChild(el);
    }   
}

function insertUser(imgLink, email) {
    let li=document.createElement('li');
    li.classList.add('user')
    let img=document.createElement('img')
    img.setAttribute('src', imgLink);
    img.classList.add('user-profile-pic');
    li.appendChild(img);
    let anchor=document.createElement('a');
    anchor.setAttribute('href', '');
    anchor.classList.add('info');
    let anchorTextNode=document.createTextNode(email);
    anchor.appendChild(anchorTextNode);
    li.appendChild(anchor);
    let parent=document.querySelector('.users');
    parent.appendChild(li);
    attachEventtoInfo();
}

function attachEventtoInfo() {
    var info=document.getElementsByClassName('info')
    for(let index=0;index<info.length; index++){
        info[index].addEventListener('click', (e)=>{
            //This will remove camel image and show chats.
            e.preventDefault();
            resetUserandSubuser();  //Delete all user-chat and subuser-chat 
            let target=e.target;
            // console.log("You just click info "+target.textContent);
            let targetEmail=target.textContent.split(" ")[0]
            let input=document.getElementById('to');
            input.value=targetEmail;
            // alert(targetEmail);
            let emptyBox=document.getElementsByClassName('empty-box')[0]
            emptyBox.classList.add('hide')
            let chat=document.getElementsByClassName('chat-info')[0]
            chat.classList.remove('hide');
            //number of seen Messages 
            //set it display property to none
            try{
                target.children[0].textContent=0;
                target.children[0].classList.add('hide');
            }catch(TypeError){
                console.log('No child found.');
            }
            // let userKey=document.getElementById('user_profile_pic').dataset.userkey
            socket.emit('user', targetEmail);
            // scrolltoLastMsg();
        })
    }
}

function searchMatchedUser(value) {
    /**This function will select thoes element which textcontent
     * match with value and return a array with index number of
     * thoes elements
     */

    let listofInfo=document.querySelectorAll('.info');
    let listofMatchEles=new Array();
    // let listofMatchElesIndex=new Array();
    for (let index = 0; index < listofInfo.length; index++) {
        if(listofInfo[index].textContent.indexOf(value)>-1){
            listofMatchEles.push(listofInfo[index].parentNode);
            // listofMatchElesIndex.push(index);
        }
    }
    return listofMatchEles;
}

function lookingUserAnchor(email) {
    /**This function will return the anchor tag which textContent
     * match with email
     */
    let anchors=document.querySelectorAll('.info');
    for(let i=0; i<anchors.length; i++){
        if(anchors[i].textContent.split(' ')[0]==email){ //textContent contain many thing so just take first thing whidh was email
        return anchors[i];
        }
    }
}

function scrolltoLastMsg() {
    let parent=document.querySelector('.chat-container');
    let targetElement=parent.children[parent.children.length-1];
    try{
        parent.scroll({
            top: targetElement.offsetTop,
            left: 0,
            behavior: 'smooth'
        })
    }catch(TypeError){
        console.log('Yes got it.')
    }
}

function pointActiveBar(el){
    /**el was the element under which the active bar point
     * by first it will 'option chat' class
     * there have predefine top value in css file
     */
    let activeBar=document.querySelector('.active-bar');
    activeBar.style.left=el.offsetLeft+'px';
    activeBar.style.top=el.offsetHeight+'px';
    activeBar.style.width=el.offsetWidth+'px';
    // console.log(`here was el ${el} \n widht of el ${el.offsetWidth}`);
}

function showUpdates() {
    let users=document.querySelectorAll('.users > li.user')
    hideAll(users)
    let myUpdate=document.querySelector('.users >li.my-updates')
    myUpdate.classList.remove('hide')
}

function getFileExtension(filename) {
    let reverseFilename=reverseStr(filename)
    let extension=reverseFilename.split('.')[0]
    return reverseStr(extension)
}

function isValidMedia(file) {
    /**It check the file is video or image and return tag of document
    *based on it
    */
    let video=document.querySelector('#video')
    let img=document.querySelector('#image')
    if (file.type.search('video')>-1) {
               video.classList.remove('hide')
               video.classList.add('active')
               if(video.duration>60){
                throw MediaError('Video to too lengthy.')
               }
               return {isvideo: true, el: video}
    }
    else if (file.type.search('image')>-1) {
        img.classList.remove('hide')
        img.classList.add('active')
        return {isvideo: false, el: img}
    }
    showFlashMsg('Unsupported media type.')   
    console.log(`Media type was ${file.type}`)
    throw TypeError('Unsupported media type.')
}

function insertUpdateUser(username,imageSrc) {
    /**Here was desire format--------
     * <li class="user-update">
            <img src=".." alt="user-pic" class="user-profile-pic">
            <a href="" class="update-user">...</a>
        </li>
     */
    let li=document.createElement('li')
    li.className='user-update'
    let img=document.createElement('img')
    img.src=imageSrc
    img.className='user-profile-pic'
    let anchor=document.createElement('a')
    anchor.className='update-user'
    anchor.textContent=username
    li.appendChild(img)
    li.appendChild(anchor)
    document.querySelector('ul.users').appendChild(li)
}

function isExitsUpdateUser(username) {
    /**This function will check li.user-update with username exits or not
     * and return boolean value base on it
    */
    let updateUsers=document.querySelectorAll('li.user-update')
    for(let i=0; i< updateUsers.length; i++){
        let target=getChild(updateUsers[i].children, 'A')
        if(target.textContent==username)
            return true
    }
    return false
}

function mediaType(mediaName) {
    /**This function will return tag base on media extension
     * .update-container > #video
     * or 
     * .update-container > #image
     */
    let videoExten=['mp4', 'avi', 'm4v', 'webm', 'ogg']
    let audioExten=['png', 'jpg', 'jpeg', 'webp']
    let extension=getFileExtension(mediaName)
    if (videoExten.indexOf(extension)!=-1) {
        return {isVideo: true, el: document.querySelector('#video')}
    }
    return {isVideo: false, el: document.querySelector('#image')}
}
function addEventToUserUpdates() {
    let userUpdates=document.querySelectorAll('li.user-update')
    if(userUpdates==null)   //no user-update class exists
        return false
    for(let i=0; i<userUpdates.length; i++){
        userUpdates[i].addEventListener('click', (e)=>{
            let anchor=getChild(userUpdates[i].children, 'A')
            let name=anchor.textContent
            let updateContainer=document.querySelector('.update-container')           
            updateContainer.classList.remove('hide')
            let updates=getUserUpdateUrls(name)
            console.log(name);
            getUserUpdateUrls(name)
            console.log('Update length ', updates);

            document.querySelector('#submit').classList.add('hide')
            let index=0
            function manageUpdate(){
                /**This function just show updates one by one
                 * here use function instead of loop
                 */
                let media=mediaType(updates[index])
                let mediaTag=media.el
                mediaTag.classList.remove('hide')
                mediaTag.classList.add('active')
                mediaTag.src=updates[index]
                // console.log('From addEventToUserUpdates ', mediaTag);
                if(media.isVideo){
                    hideActive('#image')
                    mediaTag.play()
                    socket.emit('viewing', updates[index], name)
                    mediaTag.addEventListener('ended', e=>{
                        index+=1
                        let updateContainer=document.querySelector('.update-container') 
                        if(index < updates.length && !haveClass(updateContainer, 'hide')){
                            manageUpdate()
                        }
                        else{
                            try{
                                document.querySelector('.update-container > .close').click()
                            }catch(TypeError){
                                console.error('Here an error occure from 514 but any problem wasn\'t found.')
                            }
                        }
                    })
                }else{
                    hideActive('#video')
                    socket.emit('viewing', updates[index], name)
                    setTimeout(()=>{
                        index+=1
                        console.log('Here from 534 line index ', index);
                        let updateContainer=document.querySelector('.update-container') 
                        if(index < updates.length && !haveClass(updateContainer, 'hide'))
                            manageUpdate()
                        else{
                            try{
                                document.querySelector('.update-container > .close').click()
                            }catch(TypeError){
                                console.error('Here an error occure from 523 but any problem wasn\'t found.')
                            }
                        }
                    }, 5000)
                }
                // if (index < updates.length) {
                //     manageUpdate() 
                // }
            }
            manageUpdate()
            // for(let i=0; i<updates.length; i++){
                // console.log(`${0} was occure.`);

            // }
        })
    }
}

function hideOterActiveElement(el) {
    /**This function just remove active class from
     * other one element not targetEl and add hide class
     */
    let activeEls=document.querySelectorAll('.update-container > .active')
    for(let i=0; i< activeEls.length; i++){
        if (activeEls[i]!=el) {
            el.classList.remove('active')
            el.classList.add('hide')
        }
    }
}

function hideActive(selector) {
    let target=document.querySelector(selector)
    if(target.className.indexOf('active')>-1){
        target.classList.remove('active')
        target.classList.add('hide')
    }
}

function haveUpdateInSession(key, url){
    /**This function check whether any url with a name exists or not
     * and return boolean value
     */
    let value=sessionStorage.getItem(key)
    if(value != null){
        let urls=value.split(',')
        if(urls.indexOf(url) > -1)
            return true
    }
    return false
}

function getUserUpdateUrls(name) {
    let urls=sessionStorage.getItem(name)
    let list=new Array()
    let listOfUrl=urls.split(',')   
    console.log('Here before update list ', listOfUrl);
    for(let i=0; i< listOfUrl.length; i++){
        if(list.indexOf(listOfUrl[i]) == -1){
            list.push(listOfUrl[i])
        }
    }
    return list
}

async function getFile() {
    
    let [fileHandler] =await window.showOpenFilePicker()
    return fileHandler.getFile()
}

function addClickEventMediaClass(media){
    /**This function will add click event to 
     * media class tag
     */
    media.addEventListener('click', (e)=>{
        let type=getFileType(media.src)
        console.log('You just clicked. ', type);
        // let updateContainer=document.querySelector('.update-container')
        // updateContainer.classList.remove('hide')
        let isVideo=true
        if(type=='img')
            isVideo=false
        enableMediaTag(media.src, isVideo)
    })
}

function enableMediaTag(src, isVideo=true){
    let viewer=document.querySelector('.viewer')
    viewer.classList.remove('hide')
    let media=document.createElement('video')
    if(!isVideo)
        media=document.createElement('img')
    let parent=document.querySelector('.subview')
    parent.appendChild(media)
    media.classList.add('view-content')
    media.src=src
    if(isVideo){
        media.play()
        media.dataset.play=1
        media.addEventListener('click', (e)=>{
            if(Number(media.dataset.play)==1){
                media.pause()
                media.dataset.play=0
            }else{
                media.play()
                media.dataset.play=1
            }
        })
    }
}

function setOpatcityVisible(className, show=true){
    let els=document.querySelectorAll('.'+className)
    for(let i=0; i< els.length; i++){
        if(show)
            els[i].style.opacity=1
        else
        els[i].style.opacity=0
    }
}

function wasUserFriend(useremail){
    /**This function check that user already have or not 
     * of current user friend list and return boolean value
     * base on it
     */
    let infos=document.querySelectorAll('.info')   
    for(let i=0; i< infos.length; i++){
        let text=infos[i].textContent.split(' ')[0]
        if(text===useremail)
            return true
    }
    return false
}

function checkFileSize(fileSize, limit, msg=null) {
    /**limit must be in MB */
    if (fileSize > limit*1024*1024) {
        //It will check that file is not larger than 5MB
        showFlashMsg('File was too large')
        if(msg==null)
            console.log(`file size ${file.size} expected size ${limit}MB`);
        else
            console.log(msg);
        return false
    }
    return true
}

function getUserInfo(){
    socket.emit('user info', global.userMail, (data)=>{
        createInfo(data)

    })
    // return global.user

}

//7975685079        -Avinash Rathod -5000 -8/8/2024
//9732271920        -Tanmoy nayek -5000 -undefined