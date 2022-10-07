let tbl = '';
tbl +='<table class="table table-hover">'

    //--->create table header > start
    tbl +='<thead>';
        tbl +='<tr>';
        tbl +='<th>Audios</th>';
        tbl +='<th>Transcription</th>';
        tbl +='<th>Options</th>';
        tbl +='</tr>';
    tbl +='</thead>';
    //--->create table header > end

    
    //--->create table body > start
    tbl +='<tbody>';
        tbl += '<tr row_id"' + 
        //--->create table body rows > start
        $.each(ajax_data, function(index, val) 
        {
            //you can replace with your database row id
            var row_id = random_id();

            //loop through ajax row data
            tbl +='<tr row_id="'+row_id+'">';
                tbl +='<td ><div class="row_data" edit_type="click" col_name="fname">'+val['fname']+'</div></td>';
                tbl +='<td ><div class="row_data" edit_type="click" col_name="lname">'+val['lname']+'</div></td>';
                tbl +='<td ><div class="row_data" edit_type="click" col_name="email">'+val['email']+'</div></td>';

                //--->edit options > start
                tbl +='<td>';
                 
                    tbl +='<span class="btn_edit" > <a href="#" class="btn btn-link " row_id="'+row_id+'" > Edit</a> </span>';

                    //only show this button if edit button is clicked
                    tbl +='<span class="btn_save"> <a href="#" class="btn btn-link"  row_id="'+row_id+'"> Save</a> | </span>';
                    tbl +='<span class="btn_cancel"> <a href="#" class="btn btn-link" row_id="'+row_id+'"> Cancel</a> | </span>';

                tbl +='</td>';
                //--->edit options > end
                
            tbl +='</tr>';
        });

        //--->create table body rows > end

    tbl +='</tbody>';
    //--->create table body > end

tbl +='</table>'	
//--->create data table > end

//out put table data
$(document).find('.tbl_user_data').html(tbl);

$(document).find('.btn_save').hide();
$(document).find('.btn_cancel').hide(); 


//--->make div editable > start
$(document).on('click', '.row_data', function(event) 
{
    event.preventDefault(); 

    if($(this).attr('edit_type') == 'button')
    {
        return false; 
    }

    //make div editable
    $(this).closest('div').attr('contenteditable', 'true');
    //add bg css
    $(this).addClass('bg-warning').css('padding','5px');

    $(this).focus();
})	
//--->make div editable > end


//--->save single field data > start
$(document).on('focusout', '.row_data', function(event) 
{
    event.preventDefault();

    if($(this).attr('edit_type') == 'button')
    {
        return false; 
    }

    var row_id = $(this).closest('tr').attr('row_id'); 
    
    var row_div = $(this)				
    .removeClass('bg-warning') //add bg css
    .css('padding','')

    var col_name = row_div.attr('col_name'); 
    var col_val = row_div.html(); 

    var arr = {};
    arr[col_name] = col_val;

    //use the "arr"	object for your ajax call
    $.extend(arr, {row_id:row_id});

    //out put to show
    $('.post_msg').html( '<pre class="bg-success">'+JSON.stringify(arr, null, 2) +'</pre>');
    
})	