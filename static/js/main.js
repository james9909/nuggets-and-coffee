$.fn.serializeObject = function() {
    var a, o;
    o = {};
    a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            return o[this.name].push(this.value || "");
        } else {
            return o[this.name] = this.value || "";
        }
    });
    return o;
};

var api_call = function(method, url, data, success_callback) {
    $.ajax({
        "type": method,
        "datatype": "json",
        "data": data,
        "url": url
    }).done(function(result) {
        success_callback(result);
        setTimeout(function() {
            if (result.redirect) {
                window.location.href = result.redirect;
            }
        }, 1000);
    }).fail(function() {
        $.notify("Error contacting the server.");
    });
};

var updateType = function(o) {
    api_call("POST", "/updateType", {"type": o.value}, function(result) {
        if (result.success) {
            $.notify(result.message, "success");
        } else {
            $.notify(result.message);
        }
    });
};

$("#login-form").submit(function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    api_call("POST", "/login", data, function(result) {
        console.log(result);
        if (result.success) {
            window.location.href = "/";
        } else {
            $.notify(result.message, "error");
        }
    });
});

$("#register-form").submit(function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    api_call("POST", "/register", data, function(result) {
        console.log(result);
        if (result.success) {
            $.notify(result.message, "success");
        } else {
            $.notify(result.message, "error");
        }
    });
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    container:'body'
});
