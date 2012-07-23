$(function(){

    var $story_list = $('#story_list ul');

    function getList(){
        $.ajax({
            url:'/stories',
            dataType:'json',
            success:buildList
        })
    }

    function buildList(d,s,jqXHR){
        var markup = '';
        $.each(d['stories'],function(ind){
            story = d['stories'][ind];
        });
        var line = '<li>Uploader: '+story.uploader;
        line += 'Description: '+story.description;
        $.each(story['file_data'],function(ind){
            file = story['file_data'][ind];
            console.log(file)
            if(file.mimetype == 'image/jpeg' || file.mimetype == 'image/png'){
                line += '<img class="story_image" src="/image/'+file._id+'" />'
            }
        });
        line += '</li>'
        markup += line;
        $story_list.html(markup);
    }

    getList();

})
