let rbtnToggle = document.querySelectorAll(".toggle-right");
let sbtnToggle = document.querySelectorAll(".toggle-down");
let additionalContent = document.querySelectorAll(".widget-info");
let titlwidget = document.querySelectorAll(".title-text");

for (let i = 0; i < additionalContent.length; i++) {
    additionalContent[i].style.maxHeight = "0px";
    rbtnToggle[i].addEventListener("click", rtoggle);
    sbtnToggle[i].addEventListener("click", stoggle);
}

function rtoggle() {
    let index = Array.from(rbtnToggle).indexOf(this);
    if(additionalContent[index].style.maxHeight === "0px"){
        additionalContent[index].style.maxHeight = additionalContent[index].scrollHeight + "px";
        rbtnToggle[index].style.display = "none";
        sbtnToggle[index].style.display = "block";
        titlwidget[index].style.color = "#61CE70";
    }else{
        additionalContent[index].style.maxHeight = "0px";
        rbtnToggle[index].style.display = "block";
        sbtnToggle[index].style.display = "none";
        titlwidget[index].style.color = "#fff";
    }
}

function stoggle() {
    let index = Array.from(sbtnToggle).indexOf(this);
    if(additionalContent[index].style.maxHeight === "0px"){
        additionalContent[index].style.maxHeight = additionalContent[index].scrollHeight + "px";
        rbtnToggle[index].style.display = "none";
        sbtnToggle[index].style.display = "block";
        titlwidget[index].style.color = "#61CE70";
    }else{
        additionalContent[index].style.maxHeight = "0px";
        rbtnToggle[index].style.display = "block";
        sbtnToggle[index].style.display = "none";
        titlwidget[index].style.color = "#fff";
    }
}
