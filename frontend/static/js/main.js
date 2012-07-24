$(function(){

    var $story_list = $('#story_list ul');
    var lat;
    var lon;

    function geoLocate(){
        navigator.geolocation.getCurrentPosition(getCoords,locationDenied)
    }

    function locationDenied(){
        window.location.href='/location_fail';
    }

    function getCoords(position){
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
        markup = ''
        $.each(d['stories'],function(ind){
            story = d['stories'][ind];
            var fileListMarkup = ''
            $.each(story['file_data'],function(ind){
                file = story['file_data'][ind];
                if(file.mimetype == 'image/jpeg' || file.mimetype == 'image/png'){
                    var parsedFileTemplate = _.template(templates.file_list.image,file);
                }else if(file.mimetype == 'audio/mpeg'){
                    var parsedFileTemplate = _.template(templates.file_list.audio,file);
                }
                fileListMarkup+=parsedFileTemplate;
            });

            story.filelist = fileListMarkup;

            var parsedTemplate = _.template(templates.story_cell,story);
            markup += parsedTemplate;
        });
        $story_list.html(markup);
    }
    geoLocate();
})
