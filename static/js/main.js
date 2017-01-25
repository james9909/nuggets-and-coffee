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

String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
        ;
    });
};

var apiCall = function(method, url, data, success) {
    $.ajax({
        "type": method,
        "datatype": "json",
        "data": data,
        "url": url
    }).done(function(result) {
        success(result);
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
    apiCall("POST", "/api/user/updateType", {"type": o.value}, function(result) {
        if (result.success) {
            $.notify(result.message, "success");
        } else {
            $.notify(result.message, "error");
        }
    });
};

var login = function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    apiCall("POST", "/api/user/login", data, function(result) {
        if (result.success) {
            window.location.href = "/";
        } else {
            $.notify(result.message, "error");
        }
    });
};

var register = function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    apiCall("POST", "/api/user/register", data, function(result) {
        if (result.success) {
            $.notify(result.message, "success");
        } else {
            $.notify(result.message, "error");
        }
    });
};

var createPost = function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    apiCall("POST", "/api/post/create", data, function(result) {
        if (!result.success) {
            $.notify(result.message, "error");
        }
    });
}

var reply = function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    apiCall("POST", "/api/post/reply", data, function(result) {
        if (!result.success) {
            $.notify(result.message, "error");
        }
    });
}

var recipeTemplate = `
<div class="card">
    <div class="card-image">
        <center>
            <img class="img-responsive" src="{0}" height=50px>
        </center>
    </div>

    <div class="card-content">
        <span class="card-title">{1}</span>
        <button type="button" id="show" class="btn btn-custom pull-right" aria-label="Left Align">
            <i class="fa fa-ellipsis-v"></i>
        </button>
    </div>
    <div class="card-action">
        <a href={2} target="new_blank" style="!font-family: 'Amatic SC';"><span class="glyphicon glyphicon-bookmark"> Visit recipe source</a>
        <a href={3} target="new_blank" style="!font-family: 'Amatic SC';"><span class="glyphicon glyphicon-cutlery"> Find recipe online</a>
    </div>
    <div class="card-reveal">
        <span class="card-title">Recipe Information</span> <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
        <p>Ranking: {4}<br>Publisher: {5}<br>Publisher URL: {6}</p>
    </div>
</div>
`;

var addRecipe = function(recipe) {
    $("#recipes").append(recipeTemplate.format(
        recipe["image"],
        recipe["title"],
        recipe["recipeUrl"],
        recipe["f2fUrl"],
        recipe["ranking"],
        recipe["publisher"],
        recipe["publisherUrl"]
    ));
    $("#recipes").append("<br>");
};

var getRecipes = function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    apiCall("POST", "/api/recipes", data, function(result) {
        if (result.success) {
            var recipes = result.recipes;
            $("#recipes").html("");
            $.notify(result.message, "success");
            for (var i = 0; i < recipes.length; i++) {
                addRecipe(recipes[i]);
            }
            $('#show').on("click",function(){
                $(".card-reveal").slideToggle("slow");
            });

            $(".card-reveal .close").on("click",function(){
                $(".card-reveal").slideToggle("slow");
            });
        } else {
            $.notify(result.message, "error");
        }
    });
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    $("#login-form").submit(login);
    $("#register-form").submit(register);
    $("#new-post-form").submit(createPost);
    $("#reply-form").submit(reply);
    $("#recipe-form").submit(getRecipes);
});
