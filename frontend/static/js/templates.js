var templates = {};

templates.story_cell = ' \
                        <li class="story">\
                            <strong class="uploader"><%= uploader%></strong> \
                            <span class="desc"><%= description%></span> \
                            <%= filelist %> \
                        </li>\
                        ';

templates.file_list = {};

templates.file_list.image = '<img src="/image/<%= _id %>?thumb=1">';

templates.file_list.audio = '<audio controls src="/audio/<%= _id %>">';

