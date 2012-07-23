$(function(){

    var $story_list = $('#story_list ul');
    var lat;
    var lon;

    function getCoords(){
        //do geolcation here, then send the coords
        //This could be a js deferred thingy, right TDawg? Like get coords, then go on to getList
        lat = parseFloat($('input[name="lat"]')[0].value);
        lon = parseFloat($('input[name="lon"]')[0].value);
    }

    function getList(){
        $.ajax({
            url:'/stories?lat='+lat+'&lon='+lon,
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
                line += '<img class="story_image" src="/image/'+file._id+'?thumb=1" />'
            }
        });
        line += '</li>'
        markup += line;
        $story_list.html(markup);
    }

    getCoords();
    getList();

})
