     // addEventListener version
  document.addEventListener('selectionchange', () => {
   console.log(document.getSelection());
 });

 // onselectionchange version
 document.onselectionchange = () => {
   var text = getSelectedText();

   if(text)
   {
     alert(text); 

   }
 };


 function getSelectedText() {
    if (window.getSelection) {
       return window.getSelection().toString();
    } 
    else if (document.selection) {
        return document.selection.createRange().text;
    }
    return '';
 }
