<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
 <!-- Js Plugins -->
    <script src="resources/js/jquery-3.3.1.min.js"></script>
    <script src="resources/js/bootstrap.min.js"></script>
    <script src="resources/js/player.js"></script>
    <script src="resources/js/jquery.nice-select.min.js"></script>
    <script src="resources/js/mixitup.min.js"></script>
    <script src="resources/js/jquery.slicknav.js"></script>
    <script src="resources/js/owl.carousel.min.js"></script>
    <script src="resources/js/main.js"></script>
    <script src="resources/js/jquery-ui.js"></script>
    
	<script type="text/javascript">
			$(document).ready(function(){
				$("#mb_pw").keydown(function (key){
					if(key.keyCode == 13){
						ajaxLoginCheck();
					}
	
				});
			});
	
			function ajaxLoginCheck(){
				var mb_id = $("#mb_id").val();
				var mb_pw = $("#mb_pw").val();
	
				var param = {};
	
				param["mb_id"] = mb_id;
				param["mb_pw"] = mb_pw;
				 $.ajax({
					url:"${context}/ajaxLoginCheck.do",
					contentType:"application/json",
					dataType:"json",
					data:param,
					success:function(result){
						if(result['loginYn'] == 'success'){
							alert("로그인에 성공하였습니다.");
							$("#loginFrm").submit();
						}  else{
							alert('아아디와 패스워드 [한번 더!] 확인을 해주십시오.');
							$("#mb_id").val('');
							$("#mb_pw").val('');
						}
					}
				});
			}
	
	
		</script>