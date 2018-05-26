
var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {

         //根据窗口调整表格高度
        $(window).resize(function() {
            $('#student_tab').bootstrapTable('resetView', {
                height: oTableInit.tableHeight
            });
        });

        $('#student_tab').bootstrapTable({
        method: 'get',
        contentType: "application/json",//必须要有！！！！
        url:"/ajax/api/v1.0/student-query/",//要请求数据的文件路径
        height:oTableInit.tableHeight,//高度调整
//        toolbar: '#toolbar',//指定工具栏
        striped: true, //是否显示行间隔色
        dataField: "students",//bootstrap table 可以前端分页也可以后端分页，这里
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
        showColumns:true,
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
                title:'姓名',
                field:'user_name',
                sortable:true,
                align: 'center',
            },
            {
                title:'学号',
                field:'job_number',
                sortable:true,
                align: 'center',
            },
            {
                title:'班级',
                field:'class_name',
                sortable:true,
                align: 'center',
            },
            {
                title:'专业',
                field:'profession_name',
                sortable:true,
                align: 'center',
            },
            {
                title:'学院',
                field:'colleague_name',
                align: 'center',
            },
            {
                title:'更新时间',
                field:'last_modify_time',
                align: 'center',
            },
            {
                title:'uuid',
                field:'student_uuid',
                visible: false
            },
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
            //每页多少条数据
            limit: params.limit,
            //请求第几页
            offset:params.offset,
            sort:params.sort,
            sortOrder:params.order,
            colleague_name:$('#colleague_btn').text().trim(),
            profession_name:$('#profession_btn').text().trim(),
            class_name:$('#classes_btn').text().trim(),
        };
    };
        return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
//    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
            //查询按钮事件
        $('#student-query').click(function(){
            $('#student_tab').bootstrapTable('refresh', {url: '/ajax/api/v1.0/student-query/'});
        });

        //必须导入当前学院当前专业当前班级的学生信息
         $('.inputfile').change(function(obj){
                var wb;//读取完成的数据
                var rABS = true; //是否将文件读取为二进制字符串
                if(!obj.target.files) {
                    return;
                }
                var f = obj.target.files[0];
                if(!f.name.endsWith("xlsx"))
                {
                    alert('请导入xlsx格式的Excel文件');
                    return;
                }
                //读取文件
                var reader = new FileReader();
                //当文件读取完成后，回调
                reader.onload = function(e) {
                    var data = e.target.result;
                    if(rABS) {
                        wb = XLSX.read(btoa(fixdata(data)), {//手动转化
                            type: 'base64'
                        });
                    } else {
                        wb = XLSX.read(data, {
                            type: 'binary'
                        });
                    }
                    //wb.SheetNames[0]是获取Sheets中第一个Sheet的名字
                    //wb.Sheets[Sheet名]获取第一个Sheet的数据
                    var data= JSON.stringify(XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]));
                    $.post('/ajax/api/v1.0/post_students_from_excel/',{'student_data':data},function(result){
                            if(result=='1')
                            {
                             //刷新表格
                             $('#student_tab').bootstrapTable('refresh', {url: '/ajax/api/v1.0/student-query/'});
                                toastr.success('导入学生信息成功');
                            }else{
                                toastr.error('导入学生信息失败');
                            }
                        });
                };
                if(rABS) {
                    reader.readAsArrayBuffer(f);
                } else {
                    reader.readAsBinaryString(f);
                }
            function fixdata(data) { //文件流转BinaryString
                var o = "",
                    l = 0,
                    w = 10240;
                for(; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
                o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
                return o;
            }

        });

    };
    return oInit;
};

   function addStudentValidatorForm()
   {
        $('#btn_add_student').click(function(){
             var class_name=$('#classes_btn').text();
             class_name=class_name.trim();
             if(class_name=='全部'){
                  toastr.warning('至少确定新增学生的班级');
             }else{
                $('#addStudentModal').modal('toggle');
             }
        });
        $('#addStudentForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                username:{
                    validators:{
                        notEmpty: {
                            message: '姓名不空'
                        },
                    }
                },
                jobnumber:{
                    validators:{
                        notEmpty: {
                            message: '学号不空'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9]+$/,
                            message: '姓名只能含字母、数字'
                        }
                    }
                    },
                },

        }).on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            var class_name=$('#classes_btn').text();
             class_name=class_name.trim();
//            // Use Ajax to submit form data
            params=$form.serialize()+'&class_name='+class_name
            $.post($form.attr('action'), params, function(result) {
                console.log(result);
                if(result=='1'){
                    //提示添加成功
                    $('#addStudentModal').modal('toggle');
                    toastr.success('提交数据成功');
                }else{
                    toastr.error('提交数据失败');
                }
            }, 'json');
        });
   }
   function changeStudentModifyOrDeleteStatus(){

       $('.bootstrap-table').change(function(){//监听表格变化
    	var dataArr=$('#student_tab .selected');
    	if(dataArr.length==1){//当前只有一个选择 显示修改
    		$('#btn_student_edit').css('display','block').removeClass('fadeOutRight').addClass('animated fadeInRight');
    	}else{
    		$('#btn_student_edit').addClass('fadeOutRight');
    		setTimeout(function(){
    			$('#btn_student_edit').css('display','none');
    		},400);
    	}
    	if(dataArr.length>=1){//当前选中大于1条显示删除按钮
    		$('#btn_student_delete').css('display','block').removeClass('fadeOutRight').addClass('animated fadeInRight');
    	}else{
    		$('#btn_student_delete').addClass('fadeOutRight');
    		setTimeout(function(){
    			$('#btn_student_delete').css('display','none');
    		},400);
    	}
    });
   }

  function modifyStudentValidatorForm(){
        $('#btn_student_edit').click(function(){
            $('#modifyStudentModal').modal('toggle'); //打开修改学生模态窗
            var dataArr=$('#student_tab').bootstrapTable('getSelections');
            $('#modify_UserName').val(dataArr[0].user_name);
            $('#modify_JobNumber').val(dataArr[0].job_number);

            $('#modifyStudentForm').bootstrapValidator({
            message:'',
             feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:{
                username:{
                    validators:{
                        notEmpty: {
                            message: '姓名不空'
                        },
                    }
                },
                jobnumber:{
                    validators:{
                        notEmpty: {
                            message: '学号不空'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9]+$/,
                            message: '姓名只能含字母、数字'
                        }
                    }
                    },
                },
        }).on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            var class_name=$('#modify_classes_btn').text();
            class_name=class_name.trim();
//            // Use Ajax to submit form data
            username=$('#modify_UserName').val();
            jobnumber=$('#modify_JobNumber').val();
            var params={'username':username,'jobnumber':jobnumber,'class_name':class_name,'uid':dataArr[0].student_uuid};
            $.ajax({
                    url:$form.attr('action'),
                    data:params,
                    type:'PUT',
                    success:function(result){
                      if(result=='1'){
                    // 提示添加成功
                        $('#modifyStudentModal').modal('toggle');
                        refreshStudentTable();
                        toastr.success('提交数据成功');

                        ///待做 更新表格那行的数据
                        }else{
                            toastr.error('提交数据失败');
                        }
                     },
                 });
            });
        });
  }
 function controlModifyModalClass(){

    var dropdown=$('#modify_classes');
        dropdown.children().each(function(){
         $(this).click(function(event){
             var btn3=$('#modify_classes_btn');
             btn3.text(event.target.innerText);
             btn3.append(' <span class="caret"></span>');
         });
        });
 }
 function deleteStudent(){

    $('#btn_student_delete').click(function(){

       var uids='';
       var dataArr=$('#student_tab').bootstrapTable('getSelections');
       $.each(dataArr,function(index,item){
            uids+=dataArr[index].student_uuid;
            uids+=',';
       });
       Ewin.confirm({ message: "确认要删除选中的学生吗？" }).on(function (e) {
                    if(!e)
                        return;
                   $.ajax({
                        url:'/ajax/api/v1.0/student-delete/?uids='+uids,
                        type:'DELETE',
                        success:function(result){
                            console.log(result);
                            if(result=='1'){
                                refreshStudentTable();
                                toastr.success('删除学生成功');
                            }else{
                                toastr.error('删除学生失败');
                            }
                         },
                     });
            });
    });
 }
 //刷新学生表
 function refreshStudentTable(){
    $('#student_tab').bootstrapTable('refresh', {url: '/ajax/api/v1.0/student-query/'});
 }

$(document).ready(function(){

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

    addStudentValidatorForm();
    //配置toast的展示位置
    toastr.options.positionClass = 'toast-bottom-right';

    changeStudentModifyOrDeleteStatus();//切换修改和删除按钮

    modifyStudentValidatorForm();//修改学生的表单验证

    controlModifyModalClass();//控制修改学生班级的切换

    deleteStudent();
});