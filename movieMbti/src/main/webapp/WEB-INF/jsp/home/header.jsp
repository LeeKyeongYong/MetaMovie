<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
 <!-- Header Section Begin -->
    <header class="header">
        <div class="container">
            <div class="row">
                <div class="col-lg-2">
                    <div class="header__logo" style="width:250px">
                        <a href="index.do">
                            <img src="img/logo.png" alt="">
                        </a>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="header__nav">
                        <nav class="header__menu mobile-menu">
                            <ul>
                                <li class="active"><a href="index.do">Home</a></li>
                                <li><a href="categories.do">애니 <span class="arrow_carrot-down"></span></a>
                                    <ul class="dropdown">
                                        <li><a href="categories.do?movie_type=다큐멘터리">16+애니</a></li>
                                        <li><a href="categories.do?movie_type=드라마">BD.Ver</a></li>
                                        <li><a href="categories.do?movie_type=다큐멘터리">CN Animation</a></li>
                                        <li><a href="categories.do?movie_type=다큐멘터리">OVA-Special</a></li>
                                        <li><a href="categories.do?movie_type=다큐멘터리">WebToon</a></li>
                                    </ul>
                                </li>
                                <li><a href="categories.do">TV시리즈 <span class="arrow_carrot-down"></span></a>
                                    <ul class="dropdown">
                                        <li><a href="categories.do?movie_type=다큐멘터리">다큐멘터리</a></li>
                                        <li><a href="categories.do?movie_type=드라마">드라마</a></li>
                                        <li><a href="categories.do?movie_type=로맨스">로맨스</a></li>
                                        <li><a href="categories.do?movie_type=스릴러">스릴러</a></li>
                                        <li><a href="categories.do?movie_type=SF">SF</a></li>
                                        <li><a href="categories.do?movie_type=애니메이션">애니메이션</a></li>
                                        <li><a href="categories.do?movie_type=액션">액션</a></li>
                                        <li><a href="categories.do?movie_type=코미디">코미디</a></li>
                                        <li><a href="categories.do?movie_type=판타지">판타지</a></li>
                                    </ul>
                                </li>
                                <li><a href="categories.do">영화 <span class="arrow_carrot-down"></span></a>
                                    <ul class="dropdown">
                                        <li><a href="categories.do?movie_type=다큐멘터리">다큐멘터리</a></li>
                                        <li><a href="categories.do?movie_type=드라마">드라마</a></li>
                                        <li><a href="categories.do?movie_type=로맨스">로맨스</a></li>
                                        <li><a href="categories.do?movie_type=스릴러">스릴러</a></li>
                                        <li><a href="categories.do?movie_type=SF">SF</a></li>
                                        <li><a href="categories.do?movie_type=액션">액션</a></li>
                                        <li><a href="categories.do?movie_type=코미디">코미디</a></li>
                                        <li><a href="categories.do?movie_type=판타지">판타지</a></li>
                                        <li> <a href="categories.do?movie_type=애니메이션">애니메이션</a></li>
                                    </ul>
                                </li>
                                <li><a href="categories.do"> NeTupidia <span class="arrow_carrot-down"></span></a>
                                    <ul class="dropdown">
                                        <li><a href="categories.do?movie_type=다큐멘터리">공지사항</a></li>
                                        <li><a href="categories.do?movie_type=드라마">Q&A</a></li>
                                        <li><a href="categories.do?movie_type=로맨스">상영 요청</a></li>
                                        <li><a href="categories.do?movie_type=다큐멘터리">상영추천</a></li>
                                        <li><a href="categories.do?movie_type=드라마">박스오피스</a></li>
                                        <li><a href="categories.do?movie_type=드라마">애니Trailer</a></li>
                                    </ul>
                                </li>
                            </ul>
                        </nav>
                    </div>
                </div>
                <div class="col-lg-2">
                    <div class="header__right">
                    	<a href="#" class="search-switch"><span class="icon_search"></span></a>
                        	<c:choose>
								<c:when test = "${sessionScope.mb_id != null}">
                                    <a href="myinfoMember.do"><span class="icon_profile"></span></a>
                                    <a href="logout.do"><span class="icon_close"></span></a>
                                </c:when>
                                <c:otherwise>
                                     <a href="login.do"><span class="icon_profile"></span></a>
                                </c:otherwise>
                             </c:choose>
                       </div>
                </div>
            </div>
            <div id="mobile-menu-wrap"></div>
        </div>
    </header>
    <!-- Header End -->