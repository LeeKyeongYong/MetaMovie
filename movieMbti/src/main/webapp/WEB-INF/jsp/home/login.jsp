<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<c:set var ="context"><%=request.getContextPath()%></c:set>
<c:set var ="imgUrl"><%="http://gjaischool-b.ddns.net:8086/crawlingImage"%></c:set>
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
	<%@ include file="./include/Breadcrumb.jsp"%>
    <!-- Normal Breadcrumb End -->
    <!-- Login Section Begin -->
    <section class="login spad">
        <div class="container">
            <div class="row">
                <div class="col-lg-6">
                    <div class="login__form">
                        <h3>로그인 하기</h3>
                        <form action="login_ok.do"  method="post" role="form" id="loginFrm">
                            <div class="input__item">
                                <input type="text" placeholder="아이디를 입력해주세요" id="mb_id" name="mb_id" class="mb_id">
                                <span class="icon_id"></span>
                            </div>
                            <div class="input__item">
                                <input type="password" placeholder="비밀번호 입력해주세요" id="mb_pw" name="mb_pw" class="mb_pw">
                                <span class="icon_lock"></span>
                            </div>
                            <div class="loginsite-btn">
	                            <button type="button" class="site-btn" onclick="ajaxLoginCheck();">로그인</button>
                            </div>
                        </form>
                        
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="login__register">
                        <h3>재미있는 영화를 찾으시나요?<br/>회원가입하시고 혜택을 누리세요!</h3>
                        <a href="${context}/signup.do" class="primary-btn">회원 가입</a>
                    </div>
                </div>
            </div>
            <div class="login__social">
                <div class="row d-flex justify-content-center">
                    <div class="col-lg-6">
                        <div class="login__social__links">

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Login Section End -->

<!-- footer section -->
		<%@ include file="./footer.jsp"%>
      <!-- Search model Begin -->
       <%@ include file="./search.jsp"%>
    <!-- Search model end -->
	<%@ include file="./include/jsscript.jsp"%>
</body>
</html>