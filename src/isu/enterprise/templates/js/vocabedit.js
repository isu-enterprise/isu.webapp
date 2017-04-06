function rowDelete(){
  $(this).parent().parent().remove();
};

function getTemplate(selector) {
  var templates = $("template");
  var contents = templates.prop("content");
  return $(contents).find(selector).clone();
}

function rowEdit(){
  var btn = $(this);
  var tdid = "";
  var tdname = "";
  var row = $("tr.selected_row");
  var form = getTemplate("#form");
  var uuid = row.attr("data-uuid");
  var place = $("#form-panel");
  place.empty();
  place.append(form);
  var cols = row.find("td");
  var inputs = $(place).find("input");
  // FIXME: Block other buttons or make it modal.
  $("#form-update-btn").click(function(){
    $.each(cols, function(i, item) {
      var inp = $(inputs[i]);
      $(item).text(inp.val());
    });
    place.empty();
  });
  $.each(cols, function(i, item) {
    var inp = $(inputs[i]);
    inp.val($(item).text());
  });
}


function showMessage(level, msg) {
  var ml = $("#message-location");
  // glyphicon-ok-sign
  var icon = "glyphicon-" + {
    "success": "ok-sign",
    "danger": "exclamation-sign"
  }[level];
  ml.addClass("alert-"+level);
  var a = getTemplate("#alert");
  a.find("#msg").text(msg);
  a.find("#icon").addClass(icon);
  ml.empty();
  ml.append(a);
};

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
  var tr=$(this);
  tr.addClass('selected_row').siblings().removeClass('selected_row');
  $("#vocabulary-editor-header").attr("data-current-uuid", tr.attr("data-uuid"));
});

$("#vocab-save-btn").click(function(){
  var request = new Object();
  var table = $("#vocabulary-editor");
  request.uuid=table.attr("data-uuid");
  var rows = table.find("tbody tr");
  request.rows=new Array(rows.length);
  $.each(rows, function(i, item){
    var row=$(item);
    var s={
      uuid: row.attr("data-uuid")
    };
    var d = row.find("td");
    d.each(function(){
      var data = $(this);
      s[data.attr("data-field-id")]=data.text();
    });
    request.rows[i]=s;
  });
  $.ajax({
    type: "POST",
    url: "/VE/api/save",
    data: JSON.stringify(request),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
      if (data.status=="OK") {
        showMessage("success", data.message);
      } else {
        showMessage("danger", data.message);
      }
    },
    failure: function(errMsg) {
        alert(errMsg);
    }
});
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
