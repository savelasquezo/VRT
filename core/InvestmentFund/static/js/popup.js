function openform(GIFT, xGift) {
  const xform = document.getElementById("dlog");

  xform.querySelector("#tGift").value = GIFT;
  xform.showModal();

  const tGift = document.getElementById("tGift");
  tGift.textContent = GIFT;
  const vGift = document.getElementById("vGift");
  vGift.textContent = xGift.toLocaleString() + " VRTs";


  var itGift = document.getElementById("itGift");
  itGift.value = GIFT;
  var ivGift = document.getElementById("ivGift");
  ivGift.value = xGift;

}

var back = document.getElementById('back');
back.addEventListener('click', function() {
  dlog.close();
});