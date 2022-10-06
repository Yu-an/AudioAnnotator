/*
This script turns on editing mode for certain cells in a html table
In the html table, divs that are of class "editable_data", e.g.
<div class="editable_data" edit_type="click" col_name="transcript">
are turned editable (bg change to color yellow) by clicking the "Edit" button
*/

$(document).ready(function(){

    $(document).on('click', '.editable_data', function(event) 
        {
            event.preventDefault(); 

            if($(this).attr('edit_type') == 'button')
            {
                return false; 
            }

            //make the closest div with the class ".editable_data" editable (but should change)
            $(this).closest('div').attr('contenteditable', 'true');
            //add bg css
            $(this).addClass('bg-warning').css('padding','5px');
            //refocus on the cell
            $(this).focus();
        })

    // $(document).on('focusout', '.row_data', function(event) 
    // 	{
    // 		event.preventDefault();

    // 		if($(this).attr('edit_type') == 'button')
    // 		{
    // 			return false; 
    // 		}

    // 		var row_id = $(this).closest('tr').attr('row_id'); 
            
    // 		var row_div = $(this)				
    // 		.removeClass('bg-warning') //add bg css
    // 		.css('padding','')

    // 		var col_name = row_div.attr('col_name'); 
    // 		var col_val = row_div.html(); 

    // 		var arr = {};
    // 		arr[col_name] = col_val;

    // 		//use the "arr"	object for your ajax call
    // 		$.extend(arr, {row_id:row_id});

    // 		//out put to show
    // 		$('.post_msg').html( '<pre class="bg-success">'+JSON.stringify(arr, null, 2) +'</pre>');
            
    /* 
    Click on "edit" will make the Save and Cancel button show up
    */
    $(document).on('click', '.btn_edit', function(event) 
        {
            event.preventDefault();
            var tbl_row = $(this).closest('tr');

            var row_id = tbl_row.attr('row_id');

            tbl_row.find('.btn_save').show();
            tbl_row.find('.btn_cancel').show();

            //hide edit button
            tbl_row.find('.btn_edit').hide(); 

            //make the editable data in the row editable
            tbl_row.find('.editable_data')
            .attr('contenteditable', 'true')
            .attr('edit_type', 'button')
            .addClass('bg-warning')
            .css('padding','3px')

            //--->add the original entry > start
            tbl_row.find('.editable_data').each(function(index, val) 
            {  
                //this will help in case user decided to click on cancel button
                $(this).attr('original_entry', $(this).html());
            }); 		
            //--->add the original entry > end

        });
        //--->button > edit > end


        //--->button > cancel > start	
    $(document).on('click', '.btn_cancel', function(event) 
        {
            event.preventDefault();

            var tbl_row = $(this).closest('tr');

            var row_id = tbl_row.attr('row_id');

            //hide save and cacel buttons
            tbl_row.find('.btn_save').hide();
            tbl_row.find('.btn_cancel').hide();

            //show edit button
            tbl_row.find('.btn_edit').show();

            // //make the whole row editable
            // tbl_row.find('.editable_data')
            // .attr('edit_type', 'click')
            // .removeClass('bg-warning')
            // .css('padding','') 

            tbl_row.find('.editable_data').each(function(index, val) 
            {   
                $(this).html( $(this).attr('original_entry') ); 
            });  
        });
        //--->button > cancel > end

        
        //--->save whole row entery > start	
    $(document).on('click', '.btn_save', function(event) 
        {
            event.preventDefault();
            var tbl_row = $(this).closest('tr');

            var row_id = tbl_row.attr('row_id');

            
            //hide save and cacel buttons
            tbl_row.find('.btn_save').hide();
            tbl_row.find('.btn_cancel').hide();

            //show edit button
            tbl_row.find('.btn_edit').show();


            //make the whole row editable
            tbl_row.find('.editable_data')
            .attr('edit_type', 'click')
            .removeClass('bg-warning')
            .css('padding','') 

            //--->get row data > start
            var arr = {}; 
            tbl_row.find('.editable_data').each(function(index, val) 
            {   
                var col_name = $(this).attr('col_name');  
                var col_val  =  $(this).html();
                arr[col_name] = col_val;
            });
            //--->get row data > end
            // // --> post message after save > start
            // //use the "arr"	object for your ajax call
            // $.extend(arr, {row_id:row_id});

            // //out put to show
            // $('.post_msg').html( '<pre class="bg-success">'+JSON.stringify(arr, null, 2) +'</pre>')
            // // --> post message after save > end

        });
        //--->save whole row entery > end
})

