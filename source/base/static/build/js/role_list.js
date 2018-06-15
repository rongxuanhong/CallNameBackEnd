var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {

         //根据窗口调整表格高度
        $(window).resize(function() {
            $('#role_table').bootstrapTable('resetView', {
                height: oTableInit.tableHeight
            });
        });
        oTableInit.operateFormatter = function (value, row, index) {//赋予的参数
                return [
          '<button class="btn btn_role_modify" type="button"><i class="fa fa-paste"></i>修改</button>',
          '<button class="btn btn_role_delete" type="button"><i class="fa fa-envelope"></i> 删除</button>',
          '<button class="btn btn_role_alloc_pms" type="button"><i class="fa fa-envelope"></i>分配权限</button>'
            ].join('');
         }

        $('#role_table').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！！！
        url:"/ajax/api/v1.0/role",//要请求数据的文件路径
        height:oTableInit.tableHeight,//高度调整
        striped: true, //是否显示行间隔色
        dataField: "result",//bootstrap table 可以前端分页也可以后端分页，这里
        pagination:false,//是否分页
        showRefresh:true,//刷新按钮
//        showColumns:true,
        queryParams:oTableInit.queryParams,

        clickToSelect: true,//是否启用点击选中行
        toolbarAlign:'right',//工具栏对齐方式
        buttonsAlign:'right',//按钮对齐方式
        toolbar:'#toolbar',//指定工作栏
        showFooter:false,
        columns:[
            {
                title:'ID',
                field:'id',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'名称',
                field:'role_name',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'备注',
                field:'role_desc',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'更新时间',
                field:'last_modify_time',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '操作',
                align: 'center',
                valign: 'middle',
                events: operateEvents,
                formatter: oTableInit.operateFormatter //自定义方法，添加操作按钮
            }
        ],
        locale:'zh-CN',//中文支持,
        responseHandler:function(res){
            //在ajax获取到数据，渲染表格之前，修改数据源
            return res.result;
        }
    });
    };
    oTableInit.tableHeight=function() {
        return $(window).height() - 140;
     }
    //请求服务数据时所传参数
    oTableInit.queryParams= function (params){
        return{
            action:'role_list',
        };
    };
        return oTableInit;
};
function addRoleValidatorForm(){

   $('#btn_add_roles').off('click').on('click',function(){
        $('#addRoleModal').modal('toggle');

        $('#addRoleForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                role_name:{
                    validators:{
                        notEmpty: {
                            message: '名称不空'
                        },
                    }
                },
                role_note:{
                    validators:{
                        notEmpty: {
                            message: '备注不空'
                        },
                    }
                    },
                },
        }).on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
//            var bv = $form.data('bootstrapValidator');

            $.ajax({
                    url:$form.attr('action'),
                    data:$form.serialize(),
                    type:'POST',
                    success:function(result){
                     $('#addRoleModal').modal('toggle');
                      if(result.success){
                    // 提示添加成功
                        refreshRoleTable();
                        toastr.success('新增角色成功');

                        ///待做 更新表格那行的数据
                        }else{
                            toastr.error('新增角色失败');
                        }
                     },
                 });
        });
   });
}

function tableOperationEvent(){
 $(".btn_role_modify").off("click");
 $(".btn_role_alloc_pms").off("click");
   window.operateEvents = {
      'click .btn_role_modify': function (e, value, row, index) {
          $('#modify_role_name').val(row.role_name);
         $('#modify_role_note').val(row.role_desc);
         $('#modifyRoleModal').modal('toggle');

        $('#modifyRoleForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                role_name:{
                    validators:{
                        notEmpty: {
                            message: '名称不空'
                        },
                    }
                },
                role_desc:{
                    validators:{
                        notEmpty: {
                            message: '备注不空'
                        },
                    }
                    },
                },
        }).on('success.form.bv', function(e) { // 为啥多次进入。。。。。
            // Prevent form submission
            e.preventDefault();
            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            $('#btn_role_modify_sb').off('click').on('click',function(e){
//            var $form=$('#modifyRoleForm');
//            var bv = $form.data('bootstrapValidator');
//            bv.validate();
//            if(bv.isValid()){
            $.ajax({
                    url:$form.attr('action'),
                    data:$form.serialize()+'&role_id='+row.id,
                    type:'PUT',
                    success:function(result){
                     $('#modifyRoleModal').modal('toggle');
                      if(result.success){
                    // 提示添加成功
                        refreshRoleTable();
                        toastr.success('修改角色成功');

                        ///待做 更新表格那行的数据
                        }else{
                            toastr.error('修改角色失败');
                        }
                     },
                 });
            });
           });
       },
        'click .btn_role_delete': function (e, value, row, index) {

                Ewin.confirm({ message: "确认要删除选中的角色吗？" }).on(function (e) {
                    if(!e)
                        return;
                   $.ajax({
                        url:'/ajax/api/v1.0/role?role_id='+row.id,
                        type:'DELETE',
                        success:function(result){
                            console.log(result);
                            if(result.success){
                                refreshRoleTable();
                                toastr.success('删除角色成功');
                            }else{
                                toastr.error('删除角色失败');
                            }
                         },
                     });
            });
       },
       'click .btn_role_alloc_pms': function (e, value, row, index) {
            $('#allocPermissionModal').modal('toggle');
            $('#alloc_role_name').val(row.role_name);
            $('#alloc_role_note').val(row.role_desc);

            $('#menu_tree').jstree("destroy"); //单页面多次显示jstree，需要销毁实例确定更新
            $.ajax({
                 url:"/ajax/api/v1.0/role_menu?role_name="+row.role_name,
                 type:'GET',
                 success:function(result){
                     if(!result)
                        return;
                     menus=result.result;
                     var data={};
                     for(j = 0,len=menus.length; j < len; j++) {
                        menu=menus[j];
                        if(!menu.parent_id){
                            data[menu.id]={"id":menu.id,"text":menu.name,"icon":menu.icon,
                            "state" : {"opened" : true,'selected':changeState(menu.display) },"children":[]};
                        }
                     };
                        for(j = 0,len=menus.length; j < len; j++) {
                        menu=menus[j];
                        if(menu.parent_id){
                            data[menu.parent_id]["children"].push({"id":menu.id,"text":menu.name,"icon":menu.icon,
                            "state" : {"opened" : true ,'selected':changeState(menu.display)},"children":null});
                        }
                      };
                      result=[];
                      for(var key in data)
                      {
                        result.push(data[key]);
                      }
                      $('#menu_tree').jstree({
                        'core':{
                            'data':result,
                        },
                        "checkbox" : {
                            "keep_selected_style" : false,
                            "three_state":false,
                         },
                        "plugins" : [ "checkbox" ]
                        });
                        //监听jstree 选项改变
//                        var checkeds = $('#menu_tree').tree('getChecked', 'checked')

                        $('#menu_tree').on('changed.jstree',function(e,data){
                            var str='';
                            selected=data.selected;
                            for(i=0,len=selected.length;i<len;++i)
                            {
                                str+=selected[i];
                                if(i!=len-1){
                                    str+=',';
                                }
                            };
                            $('#btn_allocPermission').off('click').click(function(){
                           var $form=$('#allocPermissionForm');
                            $.ajax({
                                  url:$form.attr('action'),
                                  data:'selected='+str+'&role_name='+row.role_name,
                                  type:'PUT',
                                  success:function(result){
                                   $('#allocPermissionModal').modal('toggle');
                                       if(result.success){
                                            toastr.success('权限修改成功');
                                       }else{
                                            toastr.error('权限修改失败');
                                       }
                                   },
                                 });
                    });
                        });
                     },
                 });
       },
    };
}
function refreshRoleTable(){
    $('#role_table').bootstrapTable('refresh', {url: '/ajax/api/v1.0/role'});
}

function changeState(display)
{
    return display==1? true:false
}

$(document).ready(function(){

   tableOperationEvent();
   var tableInit=new TableInit();
   tableInit.Init();

   addRoleValidatorForm();
});