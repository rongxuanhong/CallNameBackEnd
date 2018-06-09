$(document).ready(function(){

     $.ajax({
            url:"/ajax/api/v1.0/organization",
            type:'GET',
            success:function(result){

                   $('#organization_tree').jstree({
                      'core':{
                      'data':result.result,
                      },

                   });
                    $('#organization_tree').on("changed.jstree", function (e, data) {
                       var node=data.instance.get_node(data.selected[0]);
                        $('#organization_names').val(node.text);
                        if(node.id.endsWith('colleague')){
                            $('#organization_types').val('学院');
                         }else if(node.id.endsWith('profession')){
                            $('#organization_types').val('专业');
                         }else{
                            $('#organization_types').val('班级');
                         }
                        $('#btn_modify_organization').off('click').on('click',function(){
                              var url;
                              var name;
                                if(node.id.endsWith('colleague')){
                                    url='/ajax/api/v1.0/colleague';
                                    name='colea_name';
                                }else if(node.id.endsWith('profession')){
                                    url='/ajax/api/v1.0/profession';
                                    name='prob_name';
                                }else{
                                    url='/ajax/api/v1.0/class';
                                    name='class_name';
                                }
                                uuid=node.id.split(',')[0];
                                var text=$('#organization_names').val()
                               $.ajax({
                                url:url+'?uuid='+uuid+'&'+name+'='+text,
                                type:'PUT',
                                success:function(result){
                                    if(result.success){
                                        toastr.success('学院修改成功');
                                    }else{
                                        toastr.error('学院修改失败');
                                    }
                                },
                               });
                         });
                         $('#btn_delete_organization').off('click').on('click',function(){
                              var url;
                                if(node.id.endsWith('colleague')){
                                    url='/ajax/api/v1.0/colleague';
                                }else if(node.id.endsWith('profession')){
                                    url='/ajax/api/v1.0/profession';
                                }else{
                                    url='/ajax/api/v1.0/class';
                                }
                                uuid=node.id.split(',')[0];
                               $.ajax({
                                url:url,
                                type:'DELETE',
                                data:'uuid='+uuid,
                                success:function(result){
                                    if(result.success){
                                        if(node.id.endsWith('colleague')){
                                            toastr.success('学院删除成功');
                                        }else if(node.id.endsWith('profession')){
                                            toastr.success('专业删除成功')
                                        }else{
                                            toastr.success('班级删除成功')
                                        }
                                    }else{
                                        toastr.error('删除失败');
                                    }
                                },
                               });
                         });
                    });

                    $('#btn_add_organization').off('click').on('click',function(){

                                var organization_name=$('#organization_names').val();
                                var organization_type=$('#organization_types').val();
                                var parent_organization_names=$('#parent_organization_names').val();

                                $.ajax({
                                 url:'/ajax/api/v1.0/organization',
                                 data:'organization_names='+organization_name+'&organization_types='+organization_type+
                                 '&parent_organization_names='+parent_organization_names,
                                 type:'POST',
                                 success:function(result){
                                    if(result.success)
                                    {
                                        toastr.success('新增组织成功');
                                    }else if (result.error_msg=='20008'){
                                        toastr.error('不可重复新增组织');
                                    }else{
                                        toastr.error('新增组织失败');
                                    }
                                 },
                                });
                         });
            },
    });
});