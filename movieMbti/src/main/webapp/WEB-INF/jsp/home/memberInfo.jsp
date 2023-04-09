<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<c:set var="context"><%=request.getContextPath()%></c:set>
<c:set var="userPhoto"><%="resources/memberPhoto"%></c:set>
<c:set var="memberProfile"><%="http://gjaischool-b.ddns.net:8086/memberProfile"%></c:set>
<c:set var="imgUrl"><%="http://gjaischool-b.ddns.net:8086/crawlingImage"%></c:set>


<!DOCTYPE html>
<html lang="ko">
<%@ include file="./include/head.jsp"%>
<body>
	<!-- Page Preloder -->
	<div id="preloder">
		<div class="loader"></div>
	</div>

	<!-- header -->
	<%@ include file="./header.jsp"%>

	<!-- Normal Breadcrumb Begin -->
	<%@ include file="./include/BreadcrumbSignUp.jsp"%>
	<!-- Normal Breadcrumb End -->

	<!-- Signup Section Begin -->
	<section class="signup spad">
		<div class="container">
			<div class="row">
				<div class="col-lg-7">
					<div class="login__form">
						<h3>어서오세요!! &nbsp; NeTupidia</h3>
						<form id="joinFrm" method="post"
							action="${context}/updateMember.do" role="form">
							<div class="input__item">
								<input type="text" name="mb_id" id="mb_id" class="mb_id" placeholder="아이디를 입력해주세요" required="required" autofocus="autofocus" readonly="readonly" value="${userBean.mb_id}"> 
								<span class="icon_id"></span>
								<p id="message"></p>
							</div>
							<div class="input__item">
								<input class="form-control" type="text" id="mb_name" name="mb_name" placeholder="이름을 입력해주세요" autofocus="autofocus" required="required" readonly="readonly" value="${userBean.mb_name}" />
								<span class="icon_profile"></span>
							</div>
							<div class="input__item">
								<input class="form-control" type="password" name="mb_pw" id="mb_pw" required="required" placeholder="비밀번호를 입력해주세요"><span class="icon_lock"></span>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="fan" <c:if test="${fn:contains(userBean.mb_genre, 'fan')}" > checked</c:if>> 
								<label class="mb_genre_text" id="mb_genre_text">판타지</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="dra" <c:if test="${fn:contains(userBean.mb_genre, 'dra')}" > checked</c:if>>
								<label class="mb_genre_text" id="mb_genre_text">드라마</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="rom" <c:if test="${fn:contains(userBean.mb_genre, 'rom')}" > checked</c:if>>
								<label class="mb_genre_text" id="mb_genre_text">로맨스</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="com" <c:if test="${fn:contains(userBean.mb_genre, 'com')}" > checked</c:if>> 
									<label class="mb_genre_text" id="mb_genre_text">코미디</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="thr" <c:if test="${fn:contains(userBean.mb_genre, 'thr')}" > checked</c:if>> 
								<label class="mb_genre_text" id="mb_genre_text">스릴러</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="rom" <c:if test="${fn:contains(userBean.mb_genre, 'rom')}" > checked</c:if>> 
								<label class="mb_genre_text" id="mb_genre_text">액션</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="sf" <c:if test="${fn:contains(userBean.mb_genre, 'sf')}" > checked</c:if>>
								<label class="mb_genre_text" id="mb_genre_text">SF</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="ani" <c:if test="${fn:contains(userBean.mb_genre, 'ani')}" > checked</c:if>> 
								<label class="mb_genre_text" id="mb_genre_text">애니메이션</label>
							</div>
							<div class="blog__details__tags2" id="blog__details__tags2">
								<input type="checkbox" class="mb_genre" name="mb_genre" id="mb_genre" required="required" value="doc" <c:if test="${fn:contains(userBean.mb_genre, 'doc')}" > checked</c:if>> 
								<label class="mb_genre_text" id="mb_genre_text">다큐멘터리</label>
							</div>
							<input type="hidden" id="userImage" name="mb_profile" required="required">
						</form>
						<br />
						<br />
						<button type="button" id="delete-btn" class="btn btn-warning" onclick="fn_back()">취소하기</button>
						<button type="button" id="ok-btn" class="btn btn-success" onclick="fn_update()">등록하기</button>
						<button type="button" class="site-btn " onclick="fn_Delete()">삭제하기</button>
					</div>
				</div>
				<div class="col-lg-3">
					<div class="login__social__links">
						<h3>사진</h3>
						<img id="pic" style="margin-left: 15px;" height="180px" width="200px" src="${memberProfile}/memberProfile.jpg"><br />
						<div class="col-md-6"></div>
					</div>
					<input type="hidden" id="flag" name="flag" value="false">
					<form id="ajaxform" action="${context}/saveFile.do" method="post" enctype="multipart/form-data" role="form">
						<label class="control-label col-md-2 col-xs-12"></label>
						<div class="col-md-6">
						<label for="imageFile">
							<div class="btn-upload btn btn-success" id="btn-upload">파일 업로드하기</div>
						</label> 
							<input class="form-control" type="file" id="imageFile" name="imageFile" onchange="fn_upload()" /> 
							<input type="hidden" id="imageFolder" name="imageFolder" value="userImg">
						</div>
					</form>
				</div>
			</div>
		</div>
	</section>
	<!-- Signup Section End -->

	<!-- footer section -->
	<%@ include file="./footer.jsp"%>

	<!-- Search model Begin -->
	<%@ include file="./search.jsp"%>
	<!-- Search model end -->

	<!-- Js Plugins -->
	<%@ include file="./include/jsscript.jsp"%>
	<script src="resources/js/jquery.form.js"></script>
	<script type="text/javascript">
		$(document).ready(function() {
			// 		$('#dataTables-example').dataTable();
			//fn_init();

			fn_setDetailInfo();

		});

		function fn_setDetailInfo() {

			var userImage = '${userBean.mb_profile}';
			userImage = userImage.replace(/"/gi, "");
			
			$("#pic").attr("src",'${context}/resources/memberPhoto/' + userImage);
			$("#userImage").val(userImage);

		}

		function fn_Delete() {
			if (confirm("삭제를 하면 모든 이력이 사라집니다.\n괜찮으시겠습니까?")) {
				location.href = '${context}/deleteMember.do';
			}
		}

		function fn_update() {
			if (confirm("수정하시겠습니까?")) {
				alert("회원정보가 성공적으로 수정되었습니다.");
				$("#joinFrm").submit();
			}
		}

		function idCheck() {
			var mb_id = $("#mb_id").val();
			var access = $("#message");
			$.ajax({
				url : "${context}/idCheck.do?mb_id=" + mb_id,
				success : function(result) {
					result2 = result.replace(/"/gi, "");
					var splResult = result2.split("@");
					access.html(splResult[0]);
					$("#flag").val(splResult[1]);
				}
			});
		}

		function fn_upload() {
			$("#ajaxform").ajaxSubmit({
				type : "POST",
				dataType : 'text',
				url : $("#ajaxform").attr("action"),
				data : $("#ajaxform").serialize(),
				success : function(data) {
					data = data.replace(/"/gi, "");
					var imageUrl = "${context}/resources/memberPhoto/" + data;
					
					if(checkFileName(data) == false ){
						$("#pic").attr("src", imageUrl);
						$("#userImage").val(data);
					} else {
						imageUrl="${memberProfile}/memberProfile.jpg";
						$("#pic").attr("src", imageUrl);
						$("#userImage").val("memberProfile.jpg");
					} 
					
				},
				error : function(xhr, status, error) {
					alert(error);
				}
			});
		}

		function fn_back() {
			history.back();
		}
		
		function checkFileName(str){
			var pattern =   /[\{\}\/?,;:|*~`!^\+<>@\#$%&\\\=\'\"]/gi;
		    return pattern.test(str);
		}
		
	</script>

	<style>
.mb_genre {
	display: inline;
	height: calc(1.5em + .75rem + 1px);
	padding: .975rem .375rem;
	line-height: 1.5;
	color: #495057;
	background-color: #fff;
	background-clip: padding-box;
	border: 1px solid #ced4da;
	border-radius: .25rem;
	transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out
}

#cancle-btn {
	font-size: 13px;
	color: #ffffff;
	font-weight: 700px;
	border: none;
	border-radius: 2px;
	letter-spacing: 2px;
	text-transform: uppercase;
	display: inline-block;
	padding: 12px 30px;
}

#btn-upload {
  width: 200px;
  height: 50px;
  color: #ffffff;
  border: 1px solid rgb(77,77,77);
  text-transform: uppercase;
  border-radius: 2px;
  letter-spacing: 2px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left:10px;

}
#btn-upload:hover{
    background: rgb(77,77,77);
    color: #fff;
}

}
@media ( prefers-reduced-motion :reduce) {
	.form-control {
		transition: none
	}
}

.blog__details__tags2 {
	display: inline-flex;
	color: white;
	font-size: 12px;
	font-weight: 700;
	letter-spacing: 2px;
	text-transform: uppercase;
	background: rgba(255, 255, 255, 0.1);
	border-radius: 2px;
	margin-right: 6px;
	padding: 6px 15px;
	margin-bottom: 10px;
}

#mb_genre_text {
	margin-top: 6px;
	margin-left: 10px;
	zoom: 1.5;
}

input[type=checkbox] {
	zoom: 1.5;
	background: #fff;
	border-radius: 4px;
	cursor: pointer;
	outline: 0;
}

input[type="checkbox"]::after {
	border-width: 0 2px 2px 0;
	content: '';
	display: none;
	height: 40%;
	left: 40%;
	position: relative;
	top: 20%;
	transform: rotate(45deg);
	width: 15%;
}

input[type="checkbox"]:checked {
	background: #505bf0;
}

input[type="checkbox"]:checked::after {
	display: block;
}

#ajaxform {
	margin-left: 28px;
	width: 100%;
}

#imageFile {
	background: #0b0c2a;
	border: none;
	border-radius: 2px;
	letter-spacing: 2px;
	text-transform: uppercase;
	display: none;
}
</style>
</body>

</html>