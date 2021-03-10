//删除文章确认
function confirm_delete(){
    layer.open({
        title: '确认删除',
        content: '确认删除这篇文章吗',
        yes:function (index){
            $('form#delete button').click()
            layer.close()
        }
    })
}

//删除用户确认
    function user_delete(){
        layer.open({
            title:'删除用户',
            content:'确认删除？',
            yes: function (){
                $('form#userdelete button').click();
                layer.close()
            }
            }
        )
    }