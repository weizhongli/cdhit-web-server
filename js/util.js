function toggle(input){
    var x = document.getElementById(input);
    if (x.style.display == "none"){
        x.style.display = "block";
		} else {
        x.style.display = "none";
    }
}
function openwin(){
    window.open("example.htm","newwindow");
}
function load()
{
    document.forms[0].reset();
	SetIden();
}
function SetIden() {
	var Current = document.forms[0].elements["level"].selectedIndex;
	for (var  i=0; i<= Current; i++){
		document.forms[0].elements["lc"+(i+1)].disabled=false;
		document.forms[0].elements["y"+(i+1)].checked=true;
	}
	for (var  i=Current+1; i<= 2; i++){
		document.forms[0].elements["lc"+(i+1)].disabled=true;
		document.forms[0].elements["y"+(i+1)].checked=false;
	}
}



  function hideShow(ident) {
    if (document.getElementById(ident).style.display=='none') {
        document.getElementById(ident).style.display='';
        document.images["i" + ident].src = "../css/images/minus.png";
    }
    else {
        document.getElementById(ident).style.display='none';
        document.images["i" + ident].src = "../css/images/plus.png";
    }
  }

  function change_checkbox(mode, target_form, input_name) {
    var tform = document.famform;
    for (j=0; j<tform.elements.length; j++) {
        var telement = tform.elements[j];
        if (telement.type != "checkbox") continue;
        var len1 = input_name.length+1;
        var input_name1 = input_name + ".";
        var id1         = telement.id.substring(0,len1);
        if(id1 == input_name1) {
          if (mode == "select") {
             telement.checked=true;
          }
          else if (mode == "clear") {
             telement.checked=false;
          }
        }
    }
  }


function OnNewPageNum(pageNum)
{
  if(pageNum == "" || pageNum == null)
      {
         pageNum = 1;
      }
      else
      {
         pageNum = parseInt(pageNum, 10);
      }
      if (g_bIsDumpster)
      {
         NavigateTo(g_Base + g_szFolderName + "/?Cmd=showdeleted&Page=" + pageNum + "&View=Messages");
      }
      else
      {
         NavigateTo(g_Base + g_szFolderName + "/?Cmd=contents&Page=" + pageNum + "&View=Messages");
      }
   }
