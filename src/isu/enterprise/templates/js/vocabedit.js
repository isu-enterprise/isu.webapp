function rowDelete(){
  $(this).parent().parent().remove();
};

function rowEdit(){
  var btn = $(this);
  var tdid = "";
  var tdname = "";
  var row = btn.parent().parent();
  var form = $("#form-template").clone();
  var uuid = row.attr("data-uuid");
  var place = $("#form-panel");
  place.empty();
  place.append(form);
  $("#form-update-btn").click(function(){
    alert("Saving");
    place.empty();
  });
}

$("#add-button").click(function(){
  var ip = $("#insertion-point");
  uuid = generateUUID();
  ip.append(`
            <tr id="${uuid}" data-uuid="${uuid}">
                <td class="hidden">&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>
            `);

  var rows=$("#"+uuid);
  var btndel=rows.find(".isu-delete-btn");
  var btnedit=rows.find(".isu-edit-btn");
  btndel.click(rowDelete);
  btnedit.click(rowEdit);
});

$(".isu-delete-btn").click(rowDelete);
$(".isu-edit-btn").click(rowEdit);
$('#vocabulary-editor').on('click', 'tr', function(event) {
  $(this).addClass('active').siblings().removeClass('active');
});


function generateUUID () { // Public Domain/MIT
  var d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
    d += performance.now(); //use high-precision timer if available
  }
  return 'xxxxxxxx-xxxx-8xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}
