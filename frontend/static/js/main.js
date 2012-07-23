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
        var line = '<li>Uploader: '+story.uploader+'</li>';
        markup += line;
        $story_list.html(markup);
    }

    getList();

})
