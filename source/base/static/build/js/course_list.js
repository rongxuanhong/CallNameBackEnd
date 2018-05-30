var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {

         //根据窗口调整表格高度
        $(window).resize(function() {
            $('#course_table').bootstrapTable('resetView', {
                height: oTableInit.tableHeight
            });
        });
        oTableInit.operateFormatter = function (value, row, index) {//赋予的参数
                return [
          '<button class="btn btn_course_modify" type="button"><i class="fa fa-paste"></i>修改</button>',
          '<button class="btn btn_course_delete" type="button"><i class="fa fa-envelope"></i> 删除</button>',
            ].join('');
         }

        $('#course_table').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！！！
        url:"/ajax/api/v1.0/course",//要请求数据的文件路径
        height:oTableInit.tableHeight,//高度调整
//        toolbar: '#toolbar',//指定工具栏
        striped: true, //是否显示行间隔色
        dataField: "result",//bootstrap table 可以前端分页也可以后端分页，这里
        //我们使用的是后端分页，后端分页时需返回含有total：总记录数,这个键值好像是固定的
        //rows： 记录集合 键值可以修改  dataField 自己定义成自己想要的就好
        pageNumber: 1, //初始化加载第一页，默认第一页
        pagination:true,//是否分页
        queryParamsType:'limit',//查询参数组织方式
        queryParams:oTableInit.queryParams,//请求服务器时所传的参数
        sidePagination:'server',//指定服务器端分页
        pageSize:10,//单页记录数
        pageList:[5,10,20,30],//分页步进值
        showRefresh:true,//刷新按钮
//        showColumns:true,
        clickToSelect: true,//是否启用点击选中行
        toolbarAlign:'right',//工具栏对齐方式
        buttonsAlign:'right',//按钮对齐方式
        toolbar:'#toolbar',//指定工作栏
        sortable: true,      //是否启用排序
        sortOrder: 'asc',
        showFooter:false,
        columns:[
            {
                title:'全选',
                field:'select',
                //复选框
                checkbox:true,
                width:25,
            },
            {
                title:'课程编号',
                field:'course_number',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'课程名称',
                field:'course_name',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'课程周次',
                field:'course_week_times',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'所在学期',
                field:'semester',
                align: 'center',
                valign: 'middle',
                sortable:true,
            },
            {
                title:'课程地点',
                field:'position',
                align: 'center',
                valign: 'middle',
            },
            {
                title:'更新日期',
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
            return res;
        }
    });
    };
    oTableInit.tableHeight=function() {
        return $(window).height() - 140;
     }
    //请求服务数据时所传参数
    oTableInit.queryParams= function (params){
        return{
            action:'course_list',
            //每页多少条数据
            limit: params.limit,
            //请求第几页
            offset:params.offset,
            sort:params.sort,
            sortOrder:params.order,
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
                      if(result=='1'){
                    // 提示添加成功
                        $('#addRoleModal').modal('toggle');
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
        })
//        .on('success.form.bv', function(e) { // 为啥多次进入。。。。。
//            // Prevent form submission
//            e.preventDefault();
//            // Get the form instance
//            var $form = $(e.target);

            // Get the BootstrapValidator instance
            $('#btn_role_modify_sb').off('click').on('click',function(){
             var $form=$('#modifyRoleForm');
            var bv = $form.data('bootstrapValidator');
            bv.validate();
            if(bv.isValid()){
                console.log('11');
            $.ajax({
                    url:$form.attr('action'),
                    data:$form.serialize()+'&role_id='+row.id,
                    type:'PUT',
                    success:function(result){
                      if(result=='1'){
                    // 提示添加成功
                        $('#modifyRoleModal').modal('toggle');
                        refreshRoleTable();
                        toastr.success('修改角色成功');

                        ///待做 更新表格那行的数据
                        }else{
                            toastr.error('修改角色失败');
                        }
                     },
                 });
            }
            });
       },
        'click .btn_role_delete': function (e, value, row, index) {

                Ewin.confirm({ message: "确认要删除选中的角色吗？" }).on(function (e) {
                    if(!e)
                        return;
                   $.ajax({
                        url:'/ajax/api/v1.0/role-delete/?role_id='+row.id,
                        type:'DELETE',
                        success:function(result){
                            console.log(result);
                            if(result=='1'){
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
            $('#permission_tree').jstree({

                "checkbox" : {
                    "keep_selected_style" : false
                 },
                "plugins" : [ "checkbox" ]
            });
       },
    };
}
function refreshRoleTable(){
    $('#role_table').bootstrapTable('refresh', {url: '/ajax/api/v1.0/get_role_list/'});
}

$(document).ready(function(){

   tableOperationEvent();
   var tableInit=new TableInit();
   tableInit.Init();

   addRoleValidatorForm();
});