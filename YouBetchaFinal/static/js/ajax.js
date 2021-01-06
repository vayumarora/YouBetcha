$(document).ready(function(){

    function removeMessageBar(){
            setTimeout(function(){
                $('.friend-alert').slideUp();
            }, 2500)
        }

        $(document).on('click', '.add-friend', function(){
            clickedBtn = $(this);
            url = clickedBtn.attr('data');
            OKBtn = '<span class="glyphicon glyphicon-ok"></span> ';
            removeBtn = '<a href="javascript:void(0)" data="' + url.replace("add", "remove") + '" class="remove-friend" ><span class="glyphicon glyphicon-trash"></span></a>';

            $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(result){
                if (result.status == 'success'){
                    clickedBtn.parent().append(OKBtn);
                    clickedBtn.parent().append(removeBtn);
                    clickedBtn.remove();
                    $('.friend-alert').html('Friend added').slideDown();
                    removeMessageBar();
                }
            }
        });
        });


        $(document).on('click', '.remove-friend', function(){
            clickedBtn = $(this);
            url = clickedBtn.attr('data');
            addBtn = '<a href="javascript:void(0)" data="'+ url.replace("remove", "add") +'" class="btn btn-primary add-friend">Add</a>';

            $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(result){
                if (result.status == 'success'){
                    clickedBtn.parent().append(addBtn);
                    clickedBtn.prev().remove();
                    clickedBtn.remove();
                    $('.friend-alert').html('Friend removed').slideDown();
                    removeMessageBar();
                }

            }
        });
        });
});