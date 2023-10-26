function toggle(source) {
      checkboxes = document.getElementsByName('checkboxes_dict');
      for (var i = 0, n = checkboxes.length; i < n; i++) {
          checkboxes[i].checked = source.checked;
      }
  }

function taskDivCreate(task_id) {
    if (task_id) {
        var task_div = document.getElementById(task_id);
        if (!task_div) {
            var msgdiv = document.createElement("div");
            msgdiv.id = task_id;
            msgdiv.style = "height:200px; overflow-y:scroll; margin: 10px;";
            msgdiv.className = "card-body";
            document.getElementById("task-messages").appendChild(msgdiv);
            var listtiem = document.createElement("li");
            listtiem.innerText = 'The Task ' + task_id + ' has been submitted.';
            document.getElementById(task_id).appendChild(listtiem);
            var divider = document.createElement("hr");
            document.getElementById(task_id).appendChild(divider);
        }
    }
}

function runTask() {
    $("#runTask").attr("disabled",true);
    $.ajax({
        type: "Post",
        url: "/runAsyncTaskF",
        data: $("#runTaskForm").serialize(),
        //success: taskDivCreate(data.taskid)
        success: function(data) {
            var msgdiv = document.createElement("div");
            msgdiv.id = data.taskid
            msgdiv.style = "height:200px; overflow-y:scroll; margin: 10px;"
            msgdiv.className = "card-body"
            document.getElementById("task-messages").appendChild(msgdiv);
            var listtiem = document.createElement("li");
            listtiem.innerText = 'Запуск операции ' + data.taskid
            document.getElementById(data.taskid).appendChild(listtiem);
            var divider = document.createElement("hr")
            document.getElementById(data.taskid).appendChild(divider);
        }
    });
}

function validateme(data) {
var task_arguments = "";
var dict_list_len = document.getElementById("checkboxes_dict").getElementsByTagName("li").length;
var dict_list = [];
var oper_list_len = document.getElementById("operation_dict").getElementsByTagName("li").length;
var oper_list = [];
for (var i = 0; i < dict_list_len; i++) {
$(document).find("#checkboxes_dict-"+i.toString()+":checked").each(function(){
dict_list.push($(this).val());
});
}

for (var i = 0; i < oper_list_len; i++) {
    $(document).find("#operation_dict-" + i.toString() + ":checked").each(function () {
        oper_list.push($(this).val());
        });
    }
    if (dict_list.length == 0) {
        alert('Выберите как минимум один словарь для обработки');
        return false;
    }
else {
    if (oper_list.indexOf('download') > -1 || oper_list.indexOf('update') > -1 || oper_list.indexOf('check') > -1 || oper_list.indexOf('rollback') > -1) {
    if (oper_list.indexOf('download') > -1 && oper_list.indexOf('update') > -1 && oper_list.indexOf('differ') > -1) {
        task_arguments = "--mode full-diff";
    } else if (oper_list.indexOf('download') > -1 && oper_list.indexOf('update') < 0) {
        task_arguments = "--mode download";
    } else if (oper_list.indexOf('download') < 0 && oper_list.indexOf('update') > -1 && oper_list.indexOf('differ') > -1) {
        task_arguments = "--mode update-diff";
    } else if (oper_list.indexOf('download') < 0 && oper_list.indexOf('update') > -1 && oper_list.indexOf('differ') < 0) {
        task_arguments = "--mode update";
    } else if (oper_list.indexOf('download') > -1 && oper_list.indexOf('update') > -1 && oper_list.indexOf('differ') < 0) {
        task_arguments = "--mode full";
    } else if (oper_list.indexOf('check') > -1) {
        task_arguments = "--mode check";
    } else if (oper_list.indexOf('rollback') > -1) {
        task_arguments = "--mode rollback";
    }
    if (oper_list.indexOf('notify') > -1) {
        task_arguments = task_arguments + " --tables " + dict_list.toString() + " --notify yes";
    } else {
        task_arguments = task_arguments + " --tables " + dict_list.toString() + " --notify no";
    }
    if (document.getElementById("master_mode").value == 'True') {
        task_arguments = task_arguments + " --mastermode yes";
    }
    document.getElementById("task_args").value = task_arguments;
    document.getElementById("task_start").value = 'start';
    return true;
    }
    else {
        alert('Выберите как минимум одну операцию: загрузка, обновление, сравнение или откат');
        return false;
        }
    }
}


$(document).ready(function(){
    var task_var = document.getElementById("task_start");
    if (task_var && task_var.value == "start") {
        runTask();
        $("#runTask").attr("disabled",true);
        var stop_button = document.getElementById('stopTask');
        stop_button.style.display = 'block';
    }
    var namespace='/runAsyncTaskF';
    var url = 'http://' + document.domain + ':' + location.port + namespace;
    var socket = io.connect(url);
    socket.on('connect', function() {
        socket.emit('join_room');
    });
    socket.on('msg' , function(data) {
        var listtiem = document.createElement("li");
        listtiem.innerText = data.msg;
        var mesreceiver = document.getElementById(data.taskid);
        if (mesreceiver != null) {
            mesreceiver.appendChild(listtiem);
            var div_selector = document.getElementById(data.taskid);
            div_selector.scrollTop = div_selector.scrollHeight;
        }
    });
    socket.on('status', function(data) {
        if (data.msg == 'End') {
            $("#runTask").attr("disabled",false);
            var stop_button = document.getElementById('stopTask');
            stop_button.style.display = 'none';
        }
    });
    var task_id_value = document.getElementById("task_id");
    if (task_id_value && task_id_value.value) {
        taskDivCreate(document.getElementById("task_id").value);
    }

});

