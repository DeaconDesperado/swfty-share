$(function(){

    var $story_list = $('#story_list ul');
    var lat;
    var lon;

    function geoLocate(){
        navigator.geolocation.getCurrentPosition(getCoords)
    }

    function getCoords(position){
        //do geolcation here, then send the coords
        //This could be a js deferred thingy, right TDawg? Like get coords, then go on to getList
        lat = position.coords.latitude;
        lon = position.coords.longitude;
        $('input[name="lat"]').val(lat)
        $('input[name="lon"]').val(lon)
        $('#lat_display').html(lat)
        $('#lon_display').html(lon)
        getList();
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
            var line = '<li>Uploader: '+story.uploader;
            line += 'Description: '+story.description;
            $.each(story['file_data'],function(ind){
                file = story['file_data'][ind];
                if(file.mimetype == 'image/jpeg' || file.mimetype == 'image/png'){
                    line += '<img class="story_image" src="/image/'+file._id+'?thumb=1" />'
                }
            });
            line += '</li>'
            markup += line;
        });
        $story_list.html(markup);
    }

    geoLocate();
})
